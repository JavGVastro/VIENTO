"""Update the PIX header value only for the KPNO M42 sulfur FITS files."""

from __future__ import annotations

import argparse
import math
import os
import shutil
import sys
import tempfile
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from astropy.io import fits


# The unsuffixed file is the source used by the exec_fit notebooks. Updating it
# prevents regenerated _04, _05, and _06 products from recovering the old PIX.
KPNO_S_FITS = (
    "KPNO-M42-S-bin0",
    "KPNO-M42-S-bin0_04",
    "KPNO-M42-S-bin0_05",
    "KPNO-M42-S-bin0_06",
)

DEFAULT_NEW_PIX = 0.64
DEFAULT_EXPECTED_OLD_PIX = 0.534


@dataclass(frozen=True)
class PixUpdatePlan:
    path: Path
    old_pix: float
    new_pix: float
    already_updated: bool


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Update only the PIX primary-header keyword for the KPNO M42 "
            "sulfur source and fit-product FITS files."
        )
    )
    parser.add_argument(
        "--pix",
        type=float,
        default=DEFAULT_NEW_PIX,
        help=f"New PIX value (default: {DEFAULT_NEW_PIX}).",
    )
    parser.add_argument(
        "--expected-old-pix",
        type=float,
        default=DEFAULT_EXPECTED_OLD_PIX,
        help=(
            "Expected original PIX value. A different value causes the "
            f"preflight to stop (default: {DEFAULT_EXPECTED_OLD_PIX})."
        ),
    )
    parser.add_argument(
        "--fits-dir",
        type=Path,
        default=Path.cwd(),
        help="Directory containing the FITS files (default: current directory).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show the proposed changes without modifying any files.",
    )
    parser.add_argument(
        "--no-backup",
        action="store_true",
        help="Do not create one-time .before_pix_update.fits backups.",
    )
    return parser.parse_args()


def validate_positive(value: float, name: str) -> None:
    if not math.isfinite(value) or value <= 0:
        raise ValueError(f"{name} must be a finite number greater than zero.")


def resolve_paths(fits_dir: Path) -> list[Path]:
    directory = fits_dir.resolve()
    if not directory.is_dir():
        raise FileNotFoundError(f"FITS directory not found: {directory}")

    paths = [directory / f"{name}.fits" for name in KPNO_S_FITS]
    missing = [path for path in paths if not path.is_file()]
    if missing:
        missing_text = "\n".join(f"  {path}" for path in missing)
        raise FileNotFoundError(f"Required FITS files not found:\n{missing_text}")
    return paths


def build_plan(
    path: Path,
    *,
    new_pix: float,
    expected_old_pix: float,
) -> PixUpdatePlan:
    with fits.open(path, memmap=False) as hdul:
        header = hdul[0].header
        if "PIX" not in header:
            raise KeyError(f"{path}: missing primary-header keyword 'PIX'")
        old_pix = float(header["PIX"])

    validate_positive(old_pix, f"{path}: PIX")
    already_updated = math.isclose(
        old_pix, new_pix, rel_tol=0.0, abs_tol=1e-12
    )
    has_expected_original = math.isclose(
        old_pix, expected_old_pix, rel_tol=0.0, abs_tol=1e-12
    )
    if not already_updated and not has_expected_original:
        raise ValueError(
            f"{path}: PIX={old_pix!r}; expected either the original "
            f"{expected_old_pix!r} or the new value {new_pix!r}."
        )

    return PixUpdatePlan(
        path=path,
        old_pix=old_pix,
        new_pix=new_pix,
        already_updated=already_updated,
    )


def backup_path_for(path: Path) -> Path:
    return path.with_name(f"{path.stem}.before_pix_update{path.suffix}")


def apply_plan(plan: PixUpdatePlan, *, create_backup: bool) -> None:
    if plan.already_updated:
        print(f"Already updated: {plan.path}")
        return

    backup_path = backup_path_for(plan.path)
    if create_backup and not backup_path.exists():
        shutil.copy2(plan.path, backup_path)
        print(f"Backup: {backup_path}")

    with fits.open(plan.path, memmap=False) as source_hdul:
        copied_hdus = [hdu.copy() for hdu in source_hdul]

    header = copied_hdus[0].header
    original_comment = header.comments["PIX"]
    if "PIX_ORIG" not in header:
        header["PIX_ORIG"] = (plan.old_pix, "PIX before first scale update")
    header["PIX"] = (
        plan.new_pix,
        original_comment or "Instrument pixel scale [arcsec / pix]",
    )
    timestamp = datetime.now(timezone.utc).isoformat(timespec="seconds")
    header.add_history(
        f"PIX updated {timestamp}: {plan.old_pix:.12g} -> "
        f"{plan.new_pix:.12g}."
    )

    temporary_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            dir=plan.path.parent,
            prefix=f".{plan.path.stem}.",
            suffix=plan.path.suffix,
            delete=False,
        ) as stream:
            temporary_path = Path(stream.name)

        fits.HDUList(copied_hdus).writeto(temporary_path, overwrite=True)
        shutil.copystat(plan.path, temporary_path)
        os.replace(temporary_path, plan.path)
    except PermissionError as exc:
        raise PermissionError(
            f"Windows could not replace {plan.path}. Close it in Jupyter "
            "and any FITS viewer, then retry."
        ) from exc
    finally:
        if temporary_path is not None and temporary_path.exists():
            temporary_path.unlink()

    with fits.open(plan.path, memmap=False) as hdul:
        written_pix = float(hdul[0].header["PIX"])
    if not math.isclose(
        written_pix, plan.new_pix, rel_tol=0.0, abs_tol=1e-12
    ):
        raise RuntimeError(f"PIX verification failed after writing {plan.path}")

    print(f"Updated: {plan.path}")


def main() -> int:
    args = parse_arguments()

    try:
        validate_positive(args.pix, "--pix")
        validate_positive(args.expected_old_pix, "--expected-old-pix")
        paths = resolve_paths(args.fits_dir)
        plans = [
            build_plan(
                path,
                new_pix=args.pix,
                expected_old_pix=args.expected_old_pix,
            )
            for path in paths
        ]
    except (FileNotFoundError, KeyError, ValueError, OSError) as exc:
        print(f"Preflight failed: {exc}", file=sys.stderr)
        print("No FITS files were modified.", file=sys.stderr)
        return 1

    print(f"\nKPNO sulfur PIX value: {args.pix:g}\n")
    for plan in plans:
        state = "already updated" if plan.already_updated else "will update"
        print(f"{plan.path.name} [{state}]")
        print(f"  PIX: {plan.old_pix:.15g} -> {plan.new_pix:.15g}")

    if args.dry_run:
        print("\nDry run only. No FITS files were modified.")
        return 0

    failures: list[tuple[Path, str]] = []
    for plan in plans:
        try:
            apply_plan(plan, create_backup=not args.no_backup)
        except (OSError, RuntimeError) as exc:
            failures.append((plan.path, str(exc)))
            print(f"Failed: {exc}", file=sys.stderr)

    if failures:
        print("\nThe following FITS files failed:", file=sys.stderr)
        for path, message in failures:
            print(f"  {path}: {message}", file=sys.stderr)
        return 1

    print("\nAll KPNO sulfur PIX headers were updated and verified.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
