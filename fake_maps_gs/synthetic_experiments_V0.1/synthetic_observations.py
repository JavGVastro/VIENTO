"""Load and validate base fields before physical scaling and PPV generation.

Requires NumPy and Astropy only; no GSTools or PyVista import is needed.
The supported input convention is a real 3D scalar field in the primary HDU,
with NumPy axes (x, y, z), as written by our generation stage.
"""
from pathlib import Path

import numpy as np
from astropy.io import fits


def find_field_pair(input_dir, model_gs, alpha):
    """Find exactly one velocity and one density field from FITS metadata.

Do not choose silently between duplicate realizations. Filenames are not parsed.
An incomplete or ambiguous selection raises an informative error.
"""
    folder = Path(input_dir).expanduser()
    if not folder.is_dir():
        raise FileNotFoundError(f"Input folder not found: {folder.resolve()}")

    model_name = str(model_gs).strip().lower()
    exponent = float(alpha)
    if not np.isfinite(exponent) or not 0 < exponent <= 2:
        raise ValueError("alpha/M3D must be finite and satisfy 0 < alpha <= 2.")

    matches = {"velocity": [], "density": []}
    available = []
    for path in sorted(folder.iterdir()):
        if not path.is_file() or path.suffix.lower() != ".fits":
            continue
        h = fits.getheader(path, ext=0)
        if h.get("NAXIS") != 3:
            continue
        role = str(h.get("FIELD", "")).strip().lower()
        model = str(h.get("MODEL", "")).strip().lower()
        if role not in matches or "M3D" not in h:
            continue
        value = float(h["M3D"])
        available.append(f"{path.name}: {model}, M3D={value:g}, {role}")
        if model == model_name and np.isclose(value, exponent, rtol=0, atol=1e-12):
            matches[role].append(path)

    if any(len(paths) != 1 for paths in matches.values()):
        counts = ", ".join(f"{role}={len(paths)}" for role, paths in matches.items())
        listing = "\n".join(available) or "No labeled base cubes found."
        raise ValueError(
            f"Expected one velocity and one density file for {model_name}, "
            f"M3D={exponent:g}; found {counts}.\n"
            f"Available samples:\n{listing}\n"
            "Use a folder with one realization per role for this selection."
        )
    return {role: paths[0] for role, paths in matches.items()}


def _read_field(path, expected_role):
    with fits.open(path, memmap=False) as hdul:
        h = hdul[0].header.copy()
        data = hdul[0].data
        if data is None or data.ndim != 3 or np.iscomplexobj(data):
            raise ValueError(f"{path}: expected a real 3D primary array.")
        # Native-endian, contiguous float64 for later numerical operations.
        array = np.array(data, dtype=np.float64, order="C", copy=True)

    if str(h.get("FIELD", "")).strip().lower() != expected_role:
        raise ValueError(f"{path}: FIELD does not match {expected_role!r}.")
    required = ["MODEL", "M3D", "SEED", "ARRORDER"]
    required += [f"LSCALE_{a}" for a in "XYZ"]
    required += [f"ANGLE_{a}" for a in "XYZ"]
    required += [f"D{a}" for a in "XYZ"]
    missing = [key for key in required if key not in h]
    if missing:
        raise ValueError(f"{path}: missing required header keywords: {missing}")
    if str(h["ARRORDER"]).strip().upper() != "XYZ":
        raise ValueError(f"{path}: expected ARRORDER='XYZ'; axis interpretation is ambiguous.")
    if any(n < 2 for n in array.shape) or not np.isfinite(array).all():
        raise ValueError(f"{path}: expected finite values and at least two points per axis.")
    for key in [f"LSCALE_{a}" for a in "XYZ"] + [f"D{a}" for a in "XYZ"]:
        if not np.isfinite(float(h[key])) or float(h[key]) <= 0:
            raise ValueError(f"{path}: {key} must be finite and positive.")
    for a in "XYZ":
        if not np.isfinite(float(h[f"ANGLE_{a}"])):
            raise ValueError(f"{path}: invalid rotation angle.")
    if array.std() == 0:
        raise ValueError(f"{path}: constant base field cannot be standardized.")
    return array, h


def load_field_pair(input_dir, model_gs, alpha, los_axis=0):
    """Return validated raw arrays, headers, paths, and explicit LOS metadata.

No normalization, physical units, exponentiation, or output writing occurs.
The two seeds may differ; all spatial-model settings must match at this stage.
"""
    if isinstance(los_axis, bool) or not isinstance(los_axis, (int, np.integer)) or los_axis not in (0, 1, 2):
        raise ValueError("los_axis must be 0 (x), 1 (y), or 2 (z).")
    paths = find_field_pair(input_dir, model_gs, alpha)
    velocity, hv = _read_field(paths["velocity"], "velocity")
    density, hd = _read_field(paths["density"], "density")
    if velocity.shape != density.shape:
        raise ValueError(f"Shape mismatch: velocity={velocity.shape}, density={density.shape}")

    keys = ["M3D"] + [f"LSCALE_{a}" for a in "XYZ"]
    keys += [f"ANGLE_{a}" for a in "XYZ"] + [f"D{a}" for a in "XYZ"]
    for key in keys:
        if not np.isclose(float(hv[key]), float(hd[key]), rtol=1e-12, atol=1e-12):
            raise ValueError(f"Pair mismatch in {key}: velocity={hv[key]}, density={hd[key]}")

    return {
        "velocity_base": velocity,
        "density_base": density,
        "header_velocity": hv,
        "header_density": hd,
        "paths": paths,
        "shape": velocity.shape,
        "los_axis": int(los_axis),
        "sky_axes": tuple(a for a in range(3) if a != los_axis),
    }


def print_pair_summary(pair):
    """Show actual full-cube statistics, without altering the input arrays."""
    print(f"Shape (x,y,z): {pair['shape']}")
    print(f"LOS axis: {pair['los_axis']}; remaining NumPy axes: {pair['sky_axes']}")
    for role in ("velocity", "density"):
        data = pair[f"{role}_base"]
        h = pair[f"header_{role}"]
        print(f"\n{role}: {pair['paths'][role].name}")
        print(f"  Model={h['MODEL']}, M3D={h['M3D']}, seed={h['SEED']}")
        print(f"  Min={data.min():.6f}, max={data.max():.6f}")
        print(f"  Mean={data.mean():.6f}, std={data.std():.6f}, variance={data.var():.6f}")
    print("\nRaw base fields only: physical quantities have not yet been assigned.")
