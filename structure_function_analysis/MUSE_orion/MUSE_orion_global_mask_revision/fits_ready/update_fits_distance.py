"""Update DIST, PC, and BOX_SIZE in FITS primary headers."""

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


# Define reusable FITS samples here. The .fits extension is optional.
FITS_H = (
    "MUSE-M42-H-bin0",
    "MUSE-M42-H-bin0_06",
    "MUSE-M42-H-bin0_05",
    "MUSE-M42-H-bin0_04",
    "MUSE-M42-H-bin1",
    "MUSE-M42-H-bin1_06",
    "MUSE-M42-H-bin1_05",
    "MUSE-M42-H-bin1_04",
    "MUSE-M42-H-bin2",
    "MUSE-M42-H-bin2_06",
    "MUSE-M42-H-bin2_05",
    "MUSE-M42-H-bin2_04",
    "MUSE-M42-H-bin3",
    "MUSE-M42-H-bin3_06",
    "MUSE-M42-H-bin3_05",
    "MUSE-M42-H-bin3_04",
    "MUSE-M42-H-bin4",
    "MUSE-M42-H-bin4_06",
    "MUSE-M42-H-bin4_05",
    "MUSE-M42-H-bin4_04",
)

FITS_AR = (
    "MUSE-M42-Ar-bin0",
    "MUSE-M42-Ar-bin0_06",
    "MUSE-M42-Ar-bin0_05",
    "MUSE-M42-Ar-bin0_04",
    "MUSE-M42-Ar-bin1",
    "MUSE-M42-Ar-bin1_06",
    "MUSE-M42-Ar-bin1_05",
    "MUSE-M42-Ar-bin1_04",
    "MUSE-M42-Ar-bin2",
    "MUSE-M42-Ar-bin2_06",
    "MUSE-M42-Ar-bin2_05",
    "MUSE-M42-Ar-bin2_04",
    "MUSE-M42-Ar-bin3",
    "MUSE-M42-Ar-bin3_06",
    "MUSE-M42-Ar-bin3_05",
    "MUSE-M42-Ar-bin3_04",
    "MUSE-M42-Ar-bin4",
    "MUSE-M42-Ar-bin4_06",
    "MUSE-M42-Ar-bin4_05",
    "MUSE-M42-Ar-bin4_04",
)

FITS_N = (
    "MUSE-M42-N-bin0",
    "MUSE-M42-N-bin0_06",
    "MUSE-M42-N-bin0_05",
    "MUSE-M42-N-bin0_04",
    "MUSE-M42-N-bin1",
    "MUSE-M42-N-bin1_06",
    "MUSE-M42-N-bin1_05",
    "MUSE-M42-N-bin1_04",
    "MUSE-M42-N-bin2",
    "MUSE-M42-N-bin2_06",
    "MUSE-M42-N-bin2_05",
    "MUSE-M42-N-bin2_04",
    "MUSE-M42-N-bin3",
    "MUSE-M42-N-bin3_06",
    "MUSE-M42-N-bin3_05",
    "MUSE-M42-N-bin3_04",
    "MUSE-M42-N-bin4",
    "MUSE-M42-N-bin4_06",
    "MUSE-M42-N-bin4_05",
    "MUSE-M42-N-bin4_04",
)

FITS_O = (
    "MUSE-M42-O-bin0",
    "MUSE-M42-O-bin0_06",
    "MUSE-M42-O-bin0_05",
    "MUSE-M42-O-bin0_04",
    "MUSE-M42-O-bin1",
    "MUSE-M42-O-bin1_06",
    "MUSE-M42-O-bin1_05",
    "MUSE-M42-O-bin1_04",
    "MUSE-M42-O-bin2",
    "MUSE-M42-O-bin2_06",
    "MUSE-M42-O-bin2_05",
    "MUSE-M42-O-bin2_04",
    "MUSE-M42-O-bin3",
    "MUSE-M42-O-bin3_06",
    "MUSE-M42-O-bin3_05",
    "MUSE-M42-O-bin3_04",
    "MUSE-M42-O-bin4",
    "MUSE-M42-O-bin4_06",
    "MUSE-M42-O-bin4_05",
    "MUSE-M42-O-bin4_04",
)

FITS_S = (
    "MUSE-M42-S-bin0",
    "MUSE-M42-S-bin0_06",
    "MUSE-M42-S-bin0_05",
    "MUSE-M42-S-bin0_04",
    "MUSE-M42-S-bin1",
    "MUSE-M42-S-bin1_06",
    "MUSE-M42-S-bin1_05",
    "MUSE-M42-S-bin1_04",
    "MUSE-M42-S-bin2",
    "MUSE-M42-S-bin2_06",
    "MUSE-M42-S-bin2_05",
    "MUSE-M42-S-bin2_04",
    "MUSE-M42-S-bin3",
    "MUSE-M42-S-bin3_06",
    "MUSE-M42-S-bin3_05",
    "MUSE-M42-S-bin3_04",
    "MUSE-M42-S-bin4",
    "MUSE-M42-S-bin4_06",
    "MUSE-M42-S-bin4_05",
    "MUSE-M42-S-bin4_04",
)

FITS_TRIM = (
    "MUSE-M42-H-bin2_trim",
    "MUSE-M42-H-bin2_trim_04",
    "MUSE-M42-H-bin2_trim_05",
    "MUSE-M42-H-bin2_trim_06",

    "MUSE-M42-N-bin2_trim",
    "MUSE-M42-N-bin2_trim_04",
    "MUSE-M42-N-bin2_trim_05",
    "MUSE-M42-N-bin2_trim_06",

    "MUSE-M42-O-bin2_trim",
    "MUSE-M42-O-bin2_trim_04",
    "MUSE-M42-O-bin2_trim_05",
    "MUSE-M42-O-bin2_trim_06",
)

FITS_KPNO = (
    "KPNO-M42-H-bin0",
    "KPNO-M42-H-bin0_04",
    "KPNO-M42-H-bin0_05",
    "KPNO-M42-H-bin0_06",
    "KPNO-M42-N-bin0",
    "KPNO-M42-N-bin0_04",
    "KPNO-M42-N-bin0_05",
    "KPNO-M42-N-bin0_06",
    "KPNO-M42-O-bin0",
    "KPNO-M42-O-bin0_04",
    "KPNO-M42-O-bin0_05",
    "KPNO-M42-O-bin0_06",
    "KPNO-M42-S-bin0",
    "KPNO-M42-S-bin0_04",
    "KPNO-M42-S-bin0_05",
    "KPNO-M42-S-bin0_06",
)

DEFAULT_FITS = (
#    *FITS_H,
#    *FITS_AR,
#    *FITS_N,
#    *FITS_O,
#    *FITS_S,
    *FITS_TRIM,
#    *FITS_KPNO,
)



@dataclass(frozen=True)
class UpdatePlan:
    path: Path
    old_distance: float
    new_distance: float
    old_pc: float
    new_pc: float
    old_box_size: float
    new_box_size: float
    already_updated: bool


def pc_per_arcsec(distance_pc: float) -> float:
    """Return the physical scale in pc per arcsec at ``distance_pc``."""
    if not math.isfinite(distance_pc) or distance_pc <= 0:
        raise ValueError("Distance must be a finite number greater than zero.")
    return distance_pc * math.pi / (180.0 * 3600.0)


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Update DIST and rescale PC and BOX_SIZE in FITS headers for a new "
            "distance. Original FITS files are backed up by default."
        )
    )
    parser.add_argument(
        "fits_files",
        nargs="*",
        help=(
            "FITS paths. The .fits extension is optional. If omitted, "
            "DEFAULT_FITS is used unless --file-list is supplied."
        ),
    )
    parser.add_argument(
        "--distance",
        type=float,
        required=True,
        help="New adopted distance in parsecs, for example 388.",
    )
    parser.add_argument(
        "--file-list",
        type=Path,
        help=(
            "Optional text file containing one FITS path per line. Blank "
            "lines and lines beginning with # are ignored."
        ),
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show the proposed changes without modifying any files.",
    )
    parser.add_argument(
        "--no-backup",
        action="store_true",
        help="Do not create .before_distance_update.fits backups.",
    )
    return parser.parse_args()


def names_from_file_list(file_list: Path) -> list[Path]:
    file_list = file_list.resolve()
    if not file_list.is_file():
        raise FileNotFoundError(f"File list not found: {file_list}")

    paths: list[Path] = []
    for raw_line in file_list.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        path = Path(line)
        if not path.is_absolute():
            path = file_list.parent / path
        paths.append(path)
    return paths


def resolve_fits_paths(args: argparse.Namespace) -> list[Path]:
    if args.fits_files:
        candidates = [Path(name) for name in args.fits_files]
    elif args.file_list is None:
        candidates = [Path(name) for name in DEFAULT_FITS]
    else:
        candidates = []

    if args.file_list is not None:
        candidates.extend(names_from_file_list(args.file_list))

    if not candidates:
        raise ValueError(
            "No FITS files were supplied and DEFAULT_FITS is empty."
        )

    resolved: list[Path] = []
    seen: set[Path] = set()
    for candidate in candidates:
        if not candidate.suffix:
            candidate = candidate.with_suffix(".fits")
        path = candidate.resolve()
        if not path.is_file():
            raise FileNotFoundError(f"FITS file not found: {path}")
        if path not in seen:
            resolved.append(path)
            seen.add(path)
    return resolved


def build_plan(path: Path, distance_pc: float) -> UpdatePlan:
    new_pc = pc_per_arcsec(distance_pc)

    with fits.open(path, memmap=False) as hdul:
        header = hdul[0].header
        missing = [
            key for key in ("DIST", "PC", "BOX_SIZE") if key not in header
        ]
        if missing:
            raise KeyError(f"{path}: missing header keywords: {missing}")

        old_distance = float(header["DIST"])
        old_pc = float(header["PC"])
        old_box_size = float(header["BOX_SIZE"])

    if not math.isfinite(old_distance) or old_distance <= 0:
        raise ValueError(f"{path}: invalid DIST value {old_distance!r}")
    if not math.isfinite(old_pc) or old_pc <= 0:
        raise ValueError(f"{path}: invalid PC value {old_pc!r}")
    if not math.isfinite(old_box_size) or old_box_size <= 0:
        raise ValueError(f"{path}: invalid BOX_SIZE value {old_box_size!r}")

    expected_old_pc = pc_per_arcsec(old_distance)
    if not math.isclose(old_pc, expected_old_pc, rel_tol=1e-5, abs_tol=1e-12):
        raise ValueError(
            f"{path}: DIST={old_distance!r} pc and PC={old_pc!r} pc/arcsec "
            "are inconsistent. The header must be reviewed before rescaling."
        )

    same_scale = math.isclose(old_pc, new_pc, rel_tol=0.0, abs_tol=1e-12)
    same_distance = math.isclose(
        old_distance, distance_pc, rel_tol=0.0, abs_tol=1e-9
    )

    if same_scale != same_distance:
        raise ValueError(
            f"{path}: DIST and PC are only partially updated for the requested "
            "distance. The header must be reviewed before changing BOX_SIZE."
        )

    already_updated = same_scale and same_distance
    new_box_size = (
        old_box_size
        if already_updated
        else old_box_size * new_pc / old_pc
    )

    return UpdatePlan(
        path=path,
        old_distance=old_distance,
        new_distance=distance_pc,
        old_pc=old_pc,
        new_pc=new_pc,
        old_box_size=old_box_size,
        new_box_size=new_box_size,
        already_updated=already_updated,
    )


def backup_path_for(path: Path) -> Path:
    return path.with_name(f"{path.stem}.before_distance_update{path.suffix}")


def apply_plan(
    plan: UpdatePlan,
    *,
    distance_pc: float,
    create_backup: bool,
) -> None:
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
    if "DIST_ORG" not in header:
        header["DIST_ORG"] = (
            plan.old_distance,
            "DIST before first distance update",
        )
    if "PC_ORIG" not in header:
        header["PC_ORIG"] = (plan.old_pc, "PC before first distance update")
    if "BOX_ORIG" not in header:
        header["BOX_ORIG"] = (
            plan.old_box_size,
            "BOX_SIZE before first distance update",
        )

    header["DIST"] = (distance_pc, "Distance in parsecs")
    header["PC"] = (plan.new_pc, "Physical scale [pc / arcsec]")
    header["BOX_SIZE"] = (plan.new_box_size, "Physical box size [pc]")
    timestamp = datetime.now(timezone.utc).isoformat(timespec="seconds")
    header.add_history(
        f"Distance metadata updated {timestamp}: "
        f"DIST {plan.old_distance:.12g} -> {distance_pc:.12g}; "
        f"PC {plan.old_pc:.12g} -> {plan.new_pc:.12g}; "
        f"BOX_SIZE {plan.old_box_size:.12g} -> {plan.new_box_size:.12g}."
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
            f"Windows could not replace {plan.path}. Close the file in "
            "Jupyter and any FITS viewer, then retry."
        ) from exc
    finally:
        if temporary_path is not None and temporary_path.exists():
            temporary_path.unlink()

    with fits.open(plan.path, memmap=False) as hdul:
        written_pc = float(hdul[0].header["PC"])
        written_box = float(hdul[0].header["BOX_SIZE"])
        written_distance = float(hdul[0].header["DIST"])

    if not (
        math.isclose(written_pc, plan.new_pc, rel_tol=0.0, abs_tol=1e-12)
        and math.isclose(
            written_box, plan.new_box_size, rel_tol=0.0, abs_tol=1e-12
        )
        and math.isclose(
            written_distance, distance_pc, rel_tol=0.0, abs_tol=1e-9
        )
    ):
        raise RuntimeError(f"Verification failed after writing {plan.path}")

    print(f"Updated: {plan.path}")


def main() -> int:
    args = parse_arguments()

    try:
        paths = resolve_fits_paths(args)
        plans = [build_plan(path, args.distance) for path in paths]
    except (FileNotFoundError, KeyError, ValueError, OSError) as exc:
        print(f"Preflight failed: {exc}", file=sys.stderr)
        print("No FITS files were modified.", file=sys.stderr)
        return 1

    print(f"\nAdopted distance: {args.distance:g} pc")
    print(f"New PC scale:     {pc_per_arcsec(args.distance):.15g} pc/arcsec\n")
    for plan in plans:
        state = "already updated" if plan.already_updated else "will update"
        print(f"{plan.path.name} [{state}]")
        print(
            f"  DIST:     {plan.old_distance:.15g} -> "
            f"{plan.new_distance:.15g}"
        )
        print(f"  PC:       {plan.old_pc:.15g} -> {plan.new_pc:.15g}")
        print(
            f"  BOX_SIZE: {plan.old_box_size:.15g} -> "
            f"{plan.new_box_size:.15g}"
        )

    if args.dry_run:
        print("\nDry run only. No FITS files were modified.")
        return 0

    failures: list[tuple[Path, str]] = []
    for plan in plans:
        try:
            apply_plan(
                plan,
                distance_pc=args.distance,
                create_backup=not args.no_backup,
            )
        except (OSError, RuntimeError) as exc:
            failures.append((plan.path, str(exc)))
            print(f"Failed: {exc}", file=sys.stderr)

    if failures:
        print("\nThe following FITS files failed:", file=sys.stderr)
        for path, message in failures:
            print(f"  {path}: {message}", file=sys.stderr)
        return 1

    print("\nAll selected FITS headers were updated and verified.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
