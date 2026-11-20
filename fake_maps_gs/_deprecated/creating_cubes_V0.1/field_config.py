# Base configuration for one 3D scalar random field.
# The generation notebook copies this dictionary for each sample.
# Batch changes do not modify this original dictionary.
# "density" labels a base field; no physical density transformation
# is applied at this stage.

config = {
    # Parameters varied between samples
    "field_synth": "velocity",       # Intended role: "velocity" or "density"
    "model_gs": "stable",            # Covariance model: exponential, gaussian, stable
    "alpha": 1.5,                    # Stable only: 0 < alpha <= 2
    "seed": 19880127,                # Velocity: 19880127; density: 19970221

    # Grid geometry — fixed within the current batch
    "shape": (64, 64, 64),           # Number of grid points along (x, y, z)
    "spacing": (1.0, 1.0, 1.0),      # Distance between adjacent points along each axis

    # Spatial covariance settings — fixed within the current batch
    "len_scale": (16.0, 16.0, 16.0), # Model length scales in the same units as spacing
    "angles": (0.0, 0.0, 0.0),       # GSTools rotation angles in radians; zero = no rotation
}

# Details:
# len_scale specifies the input covariance-model scale; it is not a correlation length measured from the generated cube!!