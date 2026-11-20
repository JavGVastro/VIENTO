from pathlib import Path
import json
import re
import sys


if len(sys.argv) != 4:
    raise SystemExit(
        "Usage: python make_notebook_from_template.py "
        "TEMPLATE TARGET BIN"
    )


template_path = Path(sys.argv[1])
target_path = Path(sys.argv[2])
bin_level = int(sys.argv[3])


# Do not overwrite an existing notebook
if target_path.exists():
    print(f"Exists: {target_path}")
    raise SystemExit(0)


# Load template
with template_path.open("r", encoding="utf-8") as f:
    notebook = json.load(f)


# Replace bins = 0 with the requested bin level
n_replacements = 0

for cell in notebook["cells"]:

    if cell.get("cell_type") != "code":
        continue

    source = "".join(cell.get("source", []))
    lines = source.splitlines(keepends=True)

    for i, line in enumerate(lines):

        if re.fullmatch(
            r"\s*bins\s*=\s*\d+\s*\n?",
            line,
        ):
            newline = "\n" if line.endswith("\n") else ""
            lines[i] = f"bins = {bin_level}{newline}"
            n_replacements += 1

    cell["source"] = lines

    # Clean inherited outputs
    cell["outputs"] = []
    cell["execution_count"] = None


if n_replacements != 1:
    raise RuntimeError(
        f"Expected exactly one 'bins = ...' assignment, "
        f"found {n_replacements}"
    )


# Save generated notebook
with target_path.open("w", encoding="utf-8") as f:
    json.dump(
        notebook,
        f,
        indent=1,
        ensure_ascii=False,
    )


print(
    f"Created: {target_path} "
    f"(bins = {bin_level})"
)