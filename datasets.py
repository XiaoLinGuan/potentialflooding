"""
Filter and analysis of datasets
"""

import pandas as pd
# import numpy as np


# Datasets for Map


# Datasets for Stacked Barchart


# Datasets for Pie Chart/Donut Chart


# Datasets for Line Graph
global_sl = pd.read_csv('global_sea_level.csv')
ec_sl = pd.read_csv('ec_sea_level.csv')
nyc_sl = pd.read_csv('nyc_sea_level.csv')
all_sl = pd.read_csv('all_sea_level.csv')

# Datasets for Scatter Plot
cyclones_AO = pd.read_csv('cyclones_AO.csv')
landfall_EC = pd.read_csv('cyclones_landfall_EC.csv')
tri_state_and_nyc = pd.read_csv('cyclones_tri_state_and_nyc.csv')