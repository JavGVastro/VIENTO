"""Modify the pc definition and execute selected Jupyter notebooks on Windows."""

from __future__ import annotations

import argparse
import json
import math
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


H_NOTEBOOKS = (
    "exec_fit_MUSE-M42-H-bin0_04",
    "exec_fit_MUSE-M42-H-bin0",
    "exec_fit_MUSE-M42-H-bin0_06",
    "exec_fit_MUSE-M42-H-bin1_04",
    "exec_fit_MUSE-M42-H-bin1",
    "exec_fit_MUSE-M42-H-bin1_06",
    "exec_fit_MUSE-M42-H-bin2_04",
    "exec_fit_MUSE-M42-H-bin2",
    "exec_fit_MUSE-M42-H-bin2_06",
    "exec_fit_MUSE-M42-H-bin3_04",
    "exec_fit_MUSE-M42-H-bin3",
    "exec_fit_MUSE-M42-H-bin3_06",
    "exec_fit_MUSE-M42-H-bin4_04",
    "exec_fit_MUSE-M42-H-bin4",
    "exec_fit_MUSE-M42-H-bin4_06",
)





DEFAULT_NOTEBOOKS = (
    "exec_fit_KPNO-M42-H-bin0_04",
    "exec_fit_KPNO-M42-H-bin0",
    "exec_fit_KPNO-M42-H-bin0_06",
    "exec_fit_KPNO-M42-N-bin0_04",
    "exec_fit_KPNO-M42-N-bin0",
    "exec_fit_KPNO-M42-N-bin0_06",
    "exec_fit_KPNO-M42-O-bin0_04",
    "exec_fit_KPNO-M42-O-bin0",
    "exec_fit_KPNO-M42-O-bin0_06",
    "exec_fit_KPNO-M42-S-bin0_04",
    "exec_fit_KPNO-M42-S-bin0",
    "exec_fit_KPNO-M42-S-bin0_06",
    )

# Match any active assignment to the variable named exactly ``pc``. This does
# not match comments or similarly named variables such as ``pc_per_arcsec``.
PC_ASSIGNMENT_PATTERN = re.compile(r"^(?P<indent>\s*)pc\s*=.*$")


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            'Replace the active pc = hdr["PC"] line and execute selected '
            "notebooks in place."
        )
    )
    parser.add_argument(
        "notebooks",
        nargs="*",
        help=(
            "Notebook filenames. The .ipynb extension is optional. "
            "If omitted, the predefined Ar notebook list is used."
        ),
    )
    parser.add_argument(
        "--distance",
        type=float,
        default=388.0,
        help="Distance to the source in parsecs (default: 388).",
    )
    parser.add_argument(
        "--notebook-dir",
        type=Path,
        default=Path.cwd(),
        help="Directory containing the notebooks (default: current directory).",
    )
    parser.add_argument(
        "--no-execute",
        action="store_true",
        help="Modify the notebooks but do not execute them.",
    )
    parser.add_argument(
        "--no-backup",
        action="store_true",
        help="Do not create the one-time .before_pc_override.ipynb backups.",
    )
    parser.add_argument(
        "--kernel",
        help="Optional Jupyter kernel name, for example: viento.",
    )
    return parser.parse_args()


def resolve_notebook_paths(
    notebook_names: list[str] | tuple[str, ...], notebook_dir: Path
) -> list[Path]:
    paths: list[Path] = []

    for notebook_name in notebook_names:
        path = Path(notebook_name)
        if path.suffix.lower() != ".ipynb":
            path = path.with_suffix(".ipynb")
        if not path.is_absolute():
            path = notebook_dir / path
        path = path.resolve()

        if not path.is_file():
            raise FileNotFoundError(f"Notebook not found: {path}")
        paths.append(path)

    return paths


def create_backup(notebook_path: Path) -> Path:
    backup_path = notebook_path.with_name(
        f"{notebook_path.stem}.before_pc_override.ipynb"
    )
    if not backup_path.exists():
        shutil.copy2(notebook_path, backup_path)
        print(f"Backup:   {backup_path}")
    return backup_path


def replace_pc_definition(notebook_path: Path, distance_pc: float) -> float:
    if not math.isfinite(distance_pc) or distance_pc <= 0:
        raise ValueError("The distance must be a finite number greater than zero.")

    with notebook_path.open(encoding="utf-8") as stream:
        notebook = json.load(stream)

    distance_text = f"{distance_pc:g}"
    replacement_count = 0

    for cell in notebook.get("cells", []):
        if cell.get("cell_type") != "code":
            continue

        new_source: list[str] = []
        for original_line in cell.get("source", []):
            line_body = original_line.rstrip("\r\n")
            line_ending = original_line[len(line_body) :]

            match = PC_ASSIGNMENT_PATTERN.fullmatch(line_body)

            if match is not None:
                indentation = match.group("indent")
                original_line = (
                    f"{indentation}pc = {distance_text} * (2 * np.pi) / "
                    f"(360 * 60 * 60)  # PC_DISTANCE_OVERRIDE{line_ending}"
                )
                replacement_count += 1

            new_source.append(original_line)

        cell["source"] = new_source

    if replacement_count == 0:
        raise RuntimeError(
            f"{notebook_path}: no active assignment to the variable pc was found."
        )
    if replacement_count > 1:
        raise RuntimeError(
            f"{notebook_path}: found {replacement_count} active pc assignments; "
            "the notebook was not changed."
        )

    temporary_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=notebook_path.parent,
            prefix=f".{notebook_path.stem}.",
            suffix=".tmp",
            delete=False,
        ) as stream:
            temporary_path = Path(stream.name)
            json.dump(notebook, stream, ensure_ascii=False, indent=1)
            stream.write("\n")

        os.replace(temporary_path, notebook_path)
    finally:
        if temporary_path is not None and temporary_path.exists():
            temporary_path.unlink()

    return distance_pc * (2 * math.pi) / (360 * 60 * 60)


def execute_notebook(
    notebook_path: Path, jupyter_command: str, kernel: str | None
) -> None:
    command = [
        jupyter_command,
        "nbconvert",
        "--to",
        "notebook",
        "--execute",
        "--inplace",
        "--ExecutePreprocessor.timeout=-1",
    ]
    if kernel:
        command.append(f"--ExecutePreprocessor.kernel_name={kernel}")
    command.append(notebook_path.name)

    # Executing from the notebook directory preserves its relative FITS paths.
    subprocess.run(command, cwd=notebook_path.parent, check=True)


def main() -> int:
    args = parse_arguments()
    notebook_names = args.notebooks if args.notebooks else DEFAULT_NOTEBOOKS

    try:
        notebook_paths = resolve_notebook_paths(
            notebook_names, args.notebook_dir.resolve()
        )
    except FileNotFoundError as exc:
        print(exc, file=sys.stderr)
        return 1

    jupyter_command: str | None = None
    if not args.no_execute:
        jupyter_command = shutil.which("jupyter")
        if jupyter_command is None:
            print(
                "Jupyter was not found in the active environment. "
                "Activate the viento environment and try again.",
                file=sys.stderr,
            )
            return 1

    failures: list[tuple[Path, str]] = []

    for notebook_path in notebook_paths:
        print(f"\nUpdating:  {notebook_path}")
        try:
            if not args.no_backup:
                create_backup(notebook_path)

            pc_per_arcsec = replace_pc_definition(notebook_path, args.distance)
            print(f"New scale: pc = {pc_per_arcsec:.15g} pc per arcsec")

            if jupyter_command is not None:
                print(f"Executing: {notebook_path.name}")
                execute_notebook(notebook_path, jupyter_command, args.kernel)
        except (OSError, RuntimeError, subprocess.CalledProcessError) as exc:
            failures.append((notebook_path, str(exc)))
            print(f"Failed: {exc}", file=sys.stderr)

    if failures:
        print("\nThe following notebooks failed:", file=sys.stderr)
        for notebook_path, message in failures:
            print(f"  {notebook_path.name}: {message}", file=sys.stderr)
        return 1

    action = "modified" if args.no_execute else "modified and executed"
    print(f"\nAll selected notebooks were {action}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
