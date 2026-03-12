
# pipeline_config.py
from pathlib import Path

# Absolute path to the base folder
#BASE_DIR = Path(r"C:\Users\javas\Dropbox\GitHub\VIENTO\MUSE_orion")

# Base del proyecto = carpeta que contiene este archivo (o su padre)
BASE_DIR = Path(__file__).resolve().parent   # si pipeline_config.py está en la raíz del repo
# BASE_DIR = Path(__file__).resolve().parent.parent  # si está dentro de un subfolder (p.ej. py_modules)

# Specific folders
OBSERVATIONS_DIR = BASE_DIR / 'observations'
CONFIDENCE_DIR   = BASE_DIR / 'results_fit'
MODULES_DIR      = BASE_DIR / 'py_modules'
STRUCTURE_DIR    = BASE_DIR / 'results_Br'
MAPS_DIR         = BASE_DIR / 'fits_ready'
FIGS_DIR         = BASE_DIR / 'Imgs'



