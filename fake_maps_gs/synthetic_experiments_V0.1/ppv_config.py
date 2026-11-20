"""Stage 1: select an existing pair of base fields.

Paths are relative to the notebook's working directory. This module does not
import the GSTools generation configuration or change any input FITS files.
Physical scaling and spectral settings will be added in the next step.
"""
from pathlib import Path

config = {
    "input_dir": Path("cubes/N256_L16"),  # Change to your existing folder.
    "model_gs": "stable",
    "alpha": 1.5,                       # Effective M3D: exponential=1, gaussian=2.
    "los_axis": 0,                      # NumPy axes: 0=x, 1=y, 2=z.
}

# Physical preparation settings.
# These are separate from the input-file selection settings.
physical_config = {
    "velocity_scale_kms": 1.0,  # Multiplier, not a target dispersion
    #"sig_E": 1.0,               # Std of the natural logarithm of weights
    "sig_E_values": [0.0, 1.0, 2.0],
    "mean_density_cm3": 1.0,    # Normalization for make_ppv's density input
}

spectral_config = {
    "temperature_K": 10000.0,
    "particle_mass_mp": 1.0,       # Thermal broadening mass: 1 × proton mass
    "los_length_pc": 1.0,          # Assumed physical depth of the cube
    "channel_width_kms": 0.5,
    "v_min_kms": -60.0,
    "v_max_kms": 60.0,
}