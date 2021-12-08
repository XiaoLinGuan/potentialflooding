"""
Read all the datasets needed for the Web App
"""
import pandas as pd


# Line Graph
global_sea_level = pd.read_csv("global_sea_level.csv")
east_coast_sea_level = pd.read_csv("east_coast_sea_level.csv")
nyc_sea_level = pd.read_csv("nyc_sea_level.csv")
all_three_regions_sea_level = pd.read_csv("all_three_regions_sea_level.csv")

# Scatter Plot
atlantic_ocean_cyclones_count = pd.read_csv("atlantic_ocean_cyclones_count.csv")
east_coast_landfall_count = pd.read_csv("east_coast_landfall_count.csv")
tri_state_region_and_nyc_count = pd.read_csv("tri_state_region_and_nyc_count.csv")
