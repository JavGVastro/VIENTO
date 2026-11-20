import gstools as gs
import numpy as np
import pyvista as pv
from pathlib import Path
from astropy.io import fits

def create_model(config):
    """Build the covariance model and return its effective exponent."""
    model_name = config["model_gs"].lower()

    parameters = {
        "dim": 3,
        "len_scale": config["len_scale"],
        "angles": config["angles"],
    }

    if model_name == "exponential":
        model = gs.Exponential(**parameters)
        m3d = 1.0

    elif model_name == "gaussian":
        model = gs.Gaussian(**parameters)
        m3d = 2.0

    elif model_name == "stable":
        m3d = float(config.get("alpha", 1.5))

        if not 0 < m3d <= 2:
            raise ValueError("Stable alpha must satisfy 0 < alpha <= 2.")

        model = gs.Stable(**parameters, alpha=m3d)

    else:
        raise ValueError(
            f"Unknown model: {model_name!r}. "
            "Choose 'exponential', 'gaussian', or 'stable'."
        )

    return model, m3d


def generate_cube(config):
    """Generate a scalar field using the existing PyVista mesh method."""
    shape = tuple(config["shape"])
    spacing = tuple(config["spacing"])

    model, m3d = create_model(config)

    grid = pv.ImageData(
        dimensions=shape,
        spacing=spacing,
    )

    srf = gs.SRF(model, seed=config["seed"])
    srf.mesh(grid, points="points", name="random-field")

    # Preserve the axis ordering used in your original notebooks.
    field_3d = np.asarray(
        grid.point_data["random-field"]
    ).reshape(shape, order="F")

    return field_3d, grid, model, m3d


def save_cube(field_3d, config, m3d, output_dir="cubes", overwrite=False):
    """Save a generated cube with its configuration in the FITS header."""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    if field_3d.shape != tuple(config["shape"]):
        raise ValueError("Cube shape does not match the configuration.")

    model_name = config["model_gs"].lower()
    field_role = config["field_synth"]
    seed = int(config["seed"])

    header = fits.Header()

    header["MODEL"] = (model_name, "GSTools covariance model")
    header["FIELD"] = (field_role, "Intended role of the base scalar field")
    header["SEED"] = (seed, "Random realization seed")
    header["M3D"] = (float(m3d), "Effective covariance shape exponent")
    header["ALPHA"] = (float(m3d), "Stable alpha or fixed model exponent")

    for axis, length, angle, step in zip(
        "XYZ",
        config["len_scale"],
        config["angles"],
        config["spacing"],
    ):
        header[f"LSCALE_{axis}"] = float(length)
        header[f"ANGLE_{axis}"] = float(angle)
        header[f"D{axis}"] = float(step)

    header["ARRORDER"] = ("XYZ", "NumPy array axes: x, y, z")
    header["GSTVER"] = (gs.__version__, "GSTools version")

    # Include shape and seed to distinguish test cubes and realizations.
    #shape_tag = "x".join(str(n) for n in field_3d.shape)
    #filename = (
    #    f"{model_name}_3d_{field_role}"
    #    f"_N{shape_tag}_seed{seed}.fits"
    #)

    #shape_tag = "x".join(str(n) for n in field_3d.shape)

    #model_tag = model_name
    #if model_name == "stable":
    #    model_tag += f"_alpha{m3d:g}"

    #filename = (
    #    f"{model_tag}_3d_{field_role}"
    #    f"_N{shape_tag}_seed{seed}.fits"
    #)

    grid_tag = get_grid_tag(config)

    model_tag = model_name
    if model_name == "stable":
        model_tag += f"_alpha{m3d:g}"

    filename = f"{model_tag}_3d_{field_role}_{grid_tag}.fits"
    path = output_dir / filename    


    # Convert once to the output precision.
    export_cube = field_3d.astype(np.float32)

    # Store numerical values without rounding to six decimal places.
    header["DATAMIN"] = (float(export_cube.min()), "Minimum field value")
    header["DATAMAX"] = (float(export_cube.max()), "Maximum field value")
    header["MEAN"] = (
        float(export_cube.mean(dtype=np.float64)),
        "Mean field value",
    )
    header["STD"] = (
        float(export_cube.std(dtype=np.float64, ddof=0)),
        "Population standard deviation",
    )

    fits.writeto(
        path,
        export_cube,
        header=header,
        overwrite=overwrite,
    )

    return path


def get_grid_tag(config):
    """Identify a cubic grid with equal model length scales."""
    shape = tuple(config["shape"])
    lengths = tuple(config["len_scale"])

    if len(shape) != 3 or not (shape[0] == shape[1] == shape[2]):
        raise ValueError("This naming scheme requires shape=(N, N, N).")

    if len(lengths) != 3 or not (lengths[0] == lengths[1] == lengths[2]):
        raise ValueError(
            "This naming scheme requires len_scale=(L, L, L)."
        )

    n = shape[0]

    # Preserve decimal length scales while displaying 16.0 as 16.
    length_tag = str(float(lengths[0]))
    if length_tag.endswith(".0"):
        length_tag = length_tag[:-2]

    return f"N{n}_L{length_tag}"