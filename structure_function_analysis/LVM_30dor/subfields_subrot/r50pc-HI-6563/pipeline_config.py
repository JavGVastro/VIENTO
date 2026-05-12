
# pipeline_config.py
from pathlib import Path

# Absolute path to the base folder
BASE_DIR = Path(__file__).resolve().parent   # si pipeline_config.py está en la raíz del repo

# Specific folders
CONFIDENCE_DIR   = BASE_DIR / 'results_fit'
MODULES_DIR      = BASE_DIR / 'py_modules'
STRUCTURE_DIR    = BASE_DIR / 'results_Br'
MAPS_DIR         = BASE_DIR / 'fits_ready'
MAPS_DIR1        = BASE_DIR / 'fits_ready_large_scales'
FIGS_DIR         = BASE_DIR / 'Figs'



