# -*- coding: utf-8 -*-
"""
Created on Thu Mar 27 11:42:02 2025

@author: ZAINTEL2
"""

# pipeline_config.py
from pathlib import Path

# Base del proyecto = carpeta que contiene este archivo (o su padre)
BASE_DIR = Path(__file__).resolve().parent   # si pipeline_config.py está en la raíz del repo
# BASE_DIR = Path(__file__).resolve().parent.parent  # si está dentro de un subfolder (p.ej. py_modules)

# Specific folders
CONFIDENCE_DIR   = BASE_DIR / 'confidence_intervals'
OBSERVATIONS_DIR = BASE_DIR / 'observations'
MODULES_DIR      = BASE_DIR / 'py_modules'
RESULTS_DIR      = BASE_DIR / 'results_files'
STRUCTURE_DIR    = BASE_DIR / 'structure_function'
MAPS_DIR         = BASE_DIR / 'velocity_fields_maps'
FIGS_DIR         = BASE_DIR / 'figures'



