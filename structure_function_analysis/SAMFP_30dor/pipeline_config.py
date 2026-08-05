
# pipeline_config.py
from pathlib import Path

# Absolute path to the base folder
BASE_DIR = Path(__file__).resolve().parent   #pipeline_config.py in ROOT folder

# Specific folders
OBSERVATIONS_DIR = BASE_DIR / 'observations'
CONFIDENCE_DIR   = BASE_DIR / 'results_fit'
MODULES_DIR      = BASE_DIR / 'py_modules'
STRUCTURE_DIR    = BASE_DIR / 'results_Br'
MAPS_DIR         = BASE_DIR / 'fits_ready'
FIGS_DIR         = BASE_DIR / 'Imgs'