
# pipeline_config.py
from pathlib import Path

# Absolute path to the base folder
#BASE_DIR = Path(r"C:\Users\javas\Dropbox\GitHub\VIENTO\MUSE_orion")

#  Absolute path to the base folder
BASE_DIR = Path(__file__).resolve().parent   
MAIN_DIR = Path(__file__).resolve().parent.parent  

# Specific folders
OBSERVATIONS_DIR = MAIN_DIR / 'observations'
#CONFIDENCE_DIR   = BASE_DIR / 'results_fit'
MODULES_DIR      = BASE_DIR / 'py_modules'
#STRUCTURE_DIR    = BASE_DIR / 'results_Br'
MAPS_DIR         = BASE_DIR / 'fits_ready'
FIGS_DIR         = BASE_DIR / 'Imgs'



