"""Execute selected Jupyter notebooks without modifying their source code."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path


NOTEBOOKS_H = (
    "exec_fit_MUSE-M42-H-bin0",
    "exec_fit_MUSE-M42-H-bin0_06",
    "exec_fit_MUSE-M42-H-bin0_05",
    "exec_fit_MUSE-M42-H-bin0_04",
    "exec_fit_MUSE-M42-H-bin1",
    "exec_fit_MUSE-M42-H-bin1_06",
    "exec_fit_MUSE-M42-H-bin1_05",
    "exec_fit_MUSE-M42-H-bin1_04",
    "exec_fit_MUSE-M42-H-bin2",
    "exec_fit_MUSE-M42-H-bin2_06",
    "exec_fit_MUSE-M42-H-bin2_05",
    "exec_fit_MUSE-M42-H-bin2_04",
    "exec_fit_MUSE-M42-H-bin3",
    "exec_fit_MUSE-M42-H-bin3_06",
    "exec_fit_MUSE-M42-H-bin3_05",
    "exec_fit_MUSE-M42-H-bin3_04",
    "exec_fit_MUSE-M42-H-bin4",
    "exec_fit_MUSE-M42-H-bin4_06",
    "exec_fit_MUSE-M42-H-bin4_05",
    "exec_fit_MUSE-M42-H-bin4_04",
)

NOTEBOOKS_AR = (
    "exec_fit_MUSE-M42-Ar-bin0",
    "exec_fit_MUSE-M42-Ar-bin0_06",
    "exec_fit_MUSE-M42-Ar-bin0_05",
    "exec_fit_MUSE-M42-Ar-bin0_04",
    "exec_fit_MUSE-M42-Ar-bin1",
    "exec_fit_MUSE-M42-Ar-bin1_06",
    "exec_fit_MUSE-M42-Ar-bin1_05",
    "exec_fit_MUSE-M42-Ar-bin1_04",
    "exec_fit_MUSE-M42-Ar-bin2",
    "exec_fit_MUSE-M42-Ar-bin2_06",
    "exec_fit_MUSE-M42-Ar-bin2_05",
    "exec_fit_MUSE-M42-Ar-bin2_04",
    "exec_fit_MUSE-M42-Ar-bin3",
    "exec_fit_MUSE-M42-Ar-bin3_06",
    "exec_fit_MUSE-M42-Ar-bin3_05",
    "exec_fit_MUSE-M42-Ar-bin3_04",
    "exec_fit_MUSE-M42-Ar-bin4",
    "exec_fit_MUSE-M42-Ar-bin4_06",
    "exec_fit_MUSE-M42-Ar-bin4_05",
    "exec_fit_MUSE-M42-Ar-bin4_04",
)

NOTEBOOKS_N = (
    "exec_fit_MUSE-M42-N-bin0",
    "exec_fit_MUSE-M42-N-bin0_06",
    "exec_fit_MUSE-M42-N-bin0_05",
    "exec_fit_MUSE-M42-N-bin0_04",
    "exec_fit_MUSE-M42-N-bin1",
    "exec_fit_MUSE-M42-N-bin1_06",
    "exec_fit_MUSE-M42-N-bin1_05",
    "exec_fit_MUSE-M42-N-bin1_04",
    "exec_fit_MUSE-M42-N-bin2",
    "exec_fit_MUSE-M42-N-bin2_06",
    "exec_fit_MUSE-M42-N-bin2_05",
    "exec_fit_MUSE-M42-N-bin2_04",
    "exec_fit_MUSE-M42-N-bin3",
    "exec_fit_MUSE-M42-N-bin3_06",
    "exec_fit_MUSE-M42-N-bin3_05",
    "exec_fit_MUSE-M42-N-bin3_04",
    "exec_fit_MUSE-M42-N-bin4",
    "exec_fit_MUSE-M42-N-bin4_06",
    "exec_fit_MUSE-M42-N-bin4_05",
    "exec_fit_MUSE-M42-N-bin4_04",
)

NOTEBOOKS_O = (
    "exec_fit_MUSE-M42-O-bin0",
    "exec_fit_MUSE-M42-O-bin0_06",
    "exec_fit_MUSE-M42-O-bin0_05",
    "exec_fit_MUSE-M42-O-bin0_04",
    "exec_fit_MUSE-M42-O-bin1",
    "exec_fit_MUSE-M42-O-bin1_06",
    "exec_fit_MUSE-M42-O-bin1_05",
    "exec_fit_MUSE-M42-O-bin1_04",
    "exec_fit_MUSE-M42-O-bin2",
    "exec_fit_MUSE-M42-O-bin2_06",
    "exec_fit_MUSE-M42-O-bin2_05",
    "exec_fit_MUSE-M42-O-bin2_04",
    "exec_fit_MUSE-M42-O-bin3",
    "exec_fit_MUSE-M42-O-bin3_06",
    "exec_fit_MUSE-M42-O-bin3_05",
    "exec_fit_MUSE-M42-O-bin3_04",
    "exec_fit_MUSE-M42-O-bin4",
    "exec_fit_MUSE-M42-O-bin4_06",
    "exec_fit_MUSE-M42-O-bin4_05",
    "exec_fit_MUSE-M42-O-bin4_04",
)

NOTEBOOKS_S = (
    "exec_fit_MUSE-M42-S-bin0",
    "exec_fit_MUSE-M42-S-bin0_06",
    "exec_fit_MUSE-M42-S-bin0_05",
    "exec_fit_MUSE-M42-S-bin0_04",
    "exec_fit_MUSE-M42-S-bin1",
    "exec_fit_MUSE-M42-S-bin1_06",
    "exec_fit_MUSE-M42-S-bin1_05",
    "exec_fit_MUSE-M42-S-bin1_04",
    "exec_fit_MUSE-M42-S-bin2",
    "exec_fit_MUSE-M42-S-bin2_06",
    "exec_fit_MUSE-M42-S-bin2_05",
    "exec_fit_MUSE-M42-S-bin2_04",
    "exec_fit_MUSE-M42-S-bin3",
    "exec_fit_MUSE-M42-S-bin3_06",
    "exec_fit_MUSE-M42-S-bin3_05",
    "exec_fit_MUSE-M42-S-bin3_04",
    "exec_fit_MUSE-M42-S-bin4",
    "exec_fit_MUSE-M42-S-bin4_06",
    "exec_fit_MUSE-M42-S-bin4_05",
    "exec_fit_MUSE-M42-S-bin4_04",
)

NOTEBOOKS_TRIM = (
 #   "exec_fit_MUSE-M42-H-bin2_trim_04",
    "exec_fit_MUSE-M42-H-bin2_trim_05",
    "exec_fit_MUSE-M42-H-bin2_trim_06",
    "exec_fit_MUSE-M42-N-bin2_trim_04",
    "exec_fit_MUSE-M42-N-bin2_trim_05",
    "exec_fit_MUSE-M42-N-bin2_trim_06",
    "exec_fit_MUSE-M42-O-bin2_trim_04",
    "exec_fit_MUSE-M42-O-bin2_trim_05",
    "exec_fit_MUSE-M42-O-bin2_trim_06",
)

NOTEBOOKS_KPNO = (
#    "exec_fit_KPNO-M42-H-bin0",
#    "exec_fit_KPNO-M42-H-bin0_04",
#    "exec_fit_KPNO-M42-H-bin0_05",
#    "exec_fit_KPNO-M42-H-bin0_06",
#    "exec_fit_KPNO-M42-N-bin0",
#    "exec_fit_KPNO-M42-N-bin0_04",
#    "exec_fit_KPNO-M42-N-bin0_05",
#    "exec_fit_KPNO-M42-N-bin0_06",
#    "exec_fit_KPNO-M42-O-bin0",
#    "exec_fit_KPNO-M42-O-bin0_04",
#    "exec_fit_KPNO-M42-O-bin0_05",
#    "exec_fit_KPNO-M42-O-bin0_06",
    "exec_fit_KPNO-M42-S-bin0",
    "exec_fit_KPNO-M42-S-bin0_04",
    "exec_fit_KPNO-M42-S-bin0_05",
    "exec_fit_KPNO-M42-S-bin0_06",
)

NOTEBOOKS_MUSE = (
   # *NOTEBOOKS_H,
   # *NOTEBOOKS_AR,
   # *NOTEBOOKS_N,
   # *NOTEBOOKS_O,
   # *NOTEBOOKS_S,
   # *NOTEBOOKS_TRIM,
    *NOTEBOOKS_KPNO,
)

NOTEBOOK_SAMPLES = {
    "H": NOTEBOOKS_H,
    "AR": NOTEBOOKS_AR,
    "N": NOTEBOOKS_N,
    "O": NOTEBOOKS_O,
    "S": NOTEBOOKS_S,
    "TRIM": NOTEBOOKS_TRIM,
    "MUSE": NOTEBOOKS_MUSE,
    "KPNO": NOTEBOOKS_KPNO,
}

# This selection is used when no filenames, --file-list, or --sample are given.
# KPNO notebooks normally live in another directory, so select them separately
# with: python run_notebooks_only.py --sample KPNO
DEFAULT_NOTEBOOKS = NOTEBOOKS_MUSE


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Execute notebooks in place without editing their cells."
    )
    parser.add_argument(
        "notebooks",
        nargs="*",
        help=(
            "Notebook filenames. The .ipynb extension is optional. "
            "If omitted, DEFAULT_NOTEBOOKS is used."
        ),
    )
    parser.add_argument(
        "--file-list",
        type=Path,
        help=(
            "Optional text file containing one notebook path per line. Blank "
            "lines and lines beginning with # are ignored."
        ),
    )
    parser.add_argument(
        "--sample",
        action="append",
        choices=tuple(NOTEBOOK_SAMPLES),
        help=(
            "Run a predefined sample. May be repeated, for example: "
            "--sample H --sample N."
        ),
    )
    parser.add_argument(
        "--notebook-dir",
        type=Path,
        default=Path.cwd(),
        help="Directory containing the notebooks (default: current directory).",
    )
    parser.add_argument(
        "--kernel",
        help="Optional Jupyter kernel name, for example viento.",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=-1,
        help="Execution timeout per cell in seconds; -1 means unlimited.",
    )
    parser.add_argument(
        "--no-backup",
        action="store_true",
        help="Do not create one-time .before_execution.ipynb backups.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help=(
            "Validate and list the selected notebooks without creating "
            "backups or executing them."
        ),
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


def resolve_notebooks(args: argparse.Namespace) -> list[Path]:
    if args.notebooks:
        candidates = [Path(name) for name in args.notebooks]
    elif args.file_list is not None:
        candidates = names_from_file_list(args.file_list)
    elif args.sample:
        candidates = [
            Path(name)
            for sample in args.sample
            for name in NOTEBOOK_SAMPLES[sample]
        ]
    else:
        candidates = [Path(name) for name in DEFAULT_NOTEBOOKS]

    if not candidates:
        raise ValueError(
            "No notebooks were supplied and DEFAULT_NOTEBOOKS is empty."
        )

    resolved: list[Path] = []
    seen: set[Path] = set()
    for candidate in candidates:
        if candidate.suffix.lower() != ".ipynb":
            candidate = candidate.with_suffix(".ipynb")
        if not candidate.is_absolute():
            candidate = args.notebook_dir / candidate
        path = candidate.resolve()
        if not path.is_file():
            raise FileNotFoundError(f"Notebook not found: {path}")
        if path not in seen:
            resolved.append(path)
            seen.add(path)
    return resolved


def backup_notebook(path: Path) -> None:
    backup = path.with_name(f"{path.stem}.before_execution.ipynb")
    if not backup.exists():
        shutil.copy2(path, backup)
        print(f"Backup: {backup}")


def execute_notebook(
    path: Path,
    *,
    jupyter_command: str,
    kernel: str | None,
    timeout: int,
) -> None:
    command = [
        jupyter_command,
        "nbconvert",
        "--to",
        "notebook",
        "--execute",
        "--inplace",
        f"--ExecutePreprocessor.timeout={timeout}",
    ]
    if kernel:
        command.append(f"--ExecutePreprocessor.kernel_name={kernel}")
    command.append(path.name)

    subprocess.run(command, cwd=path.parent, check=True)


def main() -> int:
    args = parse_arguments()

    try:
        notebooks = resolve_notebooks(args)
    except (FileNotFoundError, ValueError) as exc:
        print(exc, file=sys.stderr)
        return 1

    if args.dry_run:
        print(f"Dry run: {len(notebooks)} notebook(s) found.")
        for notebook in notebooks:
            print(f"  {notebook}")
        print("\nNo backups were created and no notebooks were executed.")
        return 0

    jupyter_command = shutil.which("jupyter")
    if jupyter_command is None:
        print(
            "Jupyter was not found. Activate the viento environment first.",
            file=sys.stderr,
        )
        return 1

    failures: list[tuple[Path, str]] = []
    for notebook in notebooks:
        print(f"\nNotebook: {notebook}")
        try:
            if not args.no_backup:
                backup_notebook(notebook)
            print(f"Executing: {notebook.name}")
            execute_notebook(
                notebook,
                jupyter_command=jupyter_command,
                kernel=args.kernel,
                timeout=args.timeout,
            )
        except (OSError, subprocess.CalledProcessError) as exc:
            failures.append((notebook, str(exc)))
            print(f"Failed: {exc}", file=sys.stderr)

    if failures:
        print("\nThe following notebooks failed:", file=sys.stderr)
        for notebook, message in failures:
            print(f"  {notebook.name}: {message}", file=sys.stderr)
        return 1

    print("\nAll selected notebooks were executed successfully.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
