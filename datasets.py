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

# Bar Chart
nyc_elevation_status1 = pd.read_csv("nyc_elevation_status.csv")
nyc_elevation_status2 = pd.read_csv("nyc_stacked.csv")
bk_elevation_status = pd.read_csv("brooklyn_elevation_status.csv")
bx_elevation_status = pd.read_csv("bronx_elevation_status.csv")
mh_elevation_status = pd.read_csv("manhattan_elevation_status.csv")
q_elevation_status = pd.read_csv("queens_elevation_status.csv")
si_elevation_status = pd.read_csv("staten_island_elevation_status.csv")

bk_population = pd.read_csv("bk_population.csv")
bx_population = pd.read_csv("bx_population.csv")
mn_population = pd.read_csv("mn_population.csv")
qn_population = pd.read_csv("qn_population.csv")
si_population = pd.read_csv("si_population.csv")
nyc_population = pd.read_csv("nyc_population.csv")

# Bubble Chart
# elevation_status_map = pd.read_csv("nyc_elevation.csv")
# elevation_status_map = elevation_status_map.sample(n=100, random_state=1)
possible_flooding_coverage = pd.read_csv("100_year_flood_data.csv")
# print(possible_flooding_coverage)
