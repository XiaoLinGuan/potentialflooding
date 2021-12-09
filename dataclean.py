"""
Clean and Filter the datasets
"""
import pandas as pd
import numpy as np

"""
Line Graph -> Sea Level Rise Trend
"""
# Return the year in a column
def specific_year(year):
	return year[7:11]

# Return the whole number of the measurement
def whole_number(x):
	return round(x)

# Read dataset.
df = pd.read_csv("techrpt083.csv", skiprows=15, low_memory=False)
# print(df)

# For all three regions, we will use 1.0 HIGH scenario for plotting the data.
# It corresponds to 83rd percentile of the climate-related sea level projections.

# Global Scale
global_sea_level = df[(df["Site"]=="GMSL") & (df["Scenario"] == "1.0 - HIGH")]

# East Coast. Find all the locations according to their latitude and longitude.
east_coast_sea_level = df[(df["Latitude"]>=24) & (df["Latitude"]<=44)]
east_coast_sea_level = east_coast_sea_level[(east_coast_sea_level["Longitude"]>=-82) & (east_coast_sea_level["Longitude"]<=-66)]
east_coast_sea_level = east_coast_sea_level[east_coast_sea_level["Scenario"]=="1.0 - HIGH"]

# NYC
nyc_sea_level = df[(df["Site"]=="NEW YORK") & (df["Scenario"] == "1.0 - HIGH")]

# Swap index column with header.
global_sea_level = global_sea_level.swapaxes("index", "columns")
nyc_sea_level = nyc_sea_level.swapaxes("index", "columns")

# Reset index column.
global_sea_level = global_sea_level.reset_index()
nyc_sea_level = nyc_sea_level.reset_index()

# Take the wanted rows from the data frame.
global_sea_level = global_sea_level.iloc[6:]
east_coast_sea_level = east_coast_sea_level.iloc[:,6:21]
nyc_sea_level = nyc_sea_level.iloc[6:]

# Take the median of each column.
east_coast_sea_level = east_coast_sea_level.median()
east_coast_sea_level = east_coast_sea_level.reset_index()

# Rename the columns and applying functions.
global_sea_level.columns = ["Year", "Centimeter"]
east_coast_sea_level.columns = ["Year", "Centimeter"]
nyc_sea_level.columns = ["Year", "Centimeter"]

global_sea_level["Year"] = global_sea_level["Year"].apply(specific_year)
east_coast_sea_level["Year"] = east_coast_sea_level["Year"].apply(specific_year)
nyc_sea_level["Year"] = nyc_sea_level["Year"].apply(specific_year)

global_sea_level["Inch"] = (global_sea_level["Centimeter"]/2.54).apply(whole_number)
east_coast_sea_level["Inch"] = (east_coast_sea_level["Centimeter"]/2.54).apply(whole_number)
nyc_sea_level["Inch"] = (nyc_sea_level["Centimeter"]/2.54).apply(whole_number)

global_sea_level["Region"] = "Global"
east_coast_sea_level["Region"] = "East Coast"
nyc_sea_level["Region"] = "NYC"

global_sea_level.to_csv("global_sea_level.csv", index=False)
east_coast_sea_level.to_csv("east_coast_sea_level.csv", index=False)
nyc_sea_level.to_csv("nyc_sea_level.csv", index=False)

# ALl three regions
all_three_regions_sea_level = pd.concat([global_sea_level, east_coast_sea_level, nyc_sea_level])
# print(all_three_regions_sea_level)
all_three_regions_sea_level.to_csv("all_three_regions_sea_level.csv", index=False)

"""
Scatter Plot -> Tropical Cyclones Pattern
"""
# Read dataset.
df = pd.read_csv("ibtracs.NA.list.v04r00.csv", skiprows=[1], low_memory=False)
# print(df)

# Take only the rows with nature value equal to HU, TS, or TD.
df = df[(df["USA_STATUS"]=="HU") | (df["USA_STATUS"]=="TS") | (df["USA_STATUS"]=="TD")]

df2 = df[df["USA_RECORD"]=="L"]	# L means made landfall on the East Coast.

# Take only three columns from the original dataset.
df1 = df[["SID", "SEASON", "USA_STATUS"]]
df2 = df2[["SID", "SEASON", "USA_STATUS"]]

# Keep one instance of each unique cyclone id.
df1 = df1.drop_duplicates(subset="SID", keep="last")
df2 = df2.drop_duplicates(subset="SID", keep="last")

# Count the number of cyclones by grouping SEASON and USA_STATUS.
df1 = df1.groupby(["SEASON", "USA_STATUS"]).count()
df2 = df2.groupby(["SEASON", "USA_STATUS"]).count()

# Reset index.
atlantic_ocean_cyclones_count = df1.reset_index()
east_coast_landfall_count = df2.reset_index()

# Rename the columns.
atlantic_ocean_cyclones_count.columns = ["Year", "Category", "Count"]
east_coast_landfall_count.columns = ["Year", "Category", "Count"]

# print(atlantic_ocean_cyclones_count)
# print(east_coast_landfall_count)

atlantic_ocean_cyclones_count.to_csv("atlantic_ocean_cyclones_count.csv", index=False)
east_coast_landfall_count.to_csv("east_coast_landfall_count.csv", index=False)

# Number of cyclones made landfall or affected Tri-State and NYC.
# Return the category of a cyclone.
def rename_category(category):
	if category[0:8] == "Category":
		return "HU"
	elif category == "Major Hurricane":
		return "HU"
	elif category == "Likely a Category 3":
		return "HU"
	elif category == "85mph Post-Tropical": 
		return "HU"
	elif category == "Tropical Storm":
		return "TS"
	elif category == "Unknown":
		return "TD"

# Read dataset.
df = pd.read_csv("tri_state_and_nyc.csv")
# print(df)

# Take only three columns from the original dataset.
df = df[["YEAR2", "NAME", "CATEGORY AT LANDFALL"]]

# Apply function to reformat the category column.
df["CATEGORY AT LANDFALL"] = df["CATEGORY AT LANDFALL"].apply(rename_category)

# Count the number of cyclones each year by grouping YEAR2 and CATEGORY AT LANDFALL.
tri_state_region_and_nyc_count = df.groupby(["YEAR2", "CATEGORY AT LANDFALL"]).count()

# Reset index.
tri_state_region_and_nyc_count = tri_state_region_and_nyc_count.reset_index()

# Rename the columns.
tri_state_region_and_nyc_count.columns = ["Year", "Category", "Count"]
tri_state_region_and_nyc_count.to_csv("tri_state_region_and_nyc_count.csv", index=False)
# print(tri_state_region_and_nyc_count)

"""
Bar Chart -> Elevation of NYC locations
"""
# Return latitude and longitude of a location.
def lat_and_lon(location):
	return location[7:-1]

# Convert the string to float.
def convert_string(number):
	return float(number)

# Return the elevation status according to the elevation.
def elevation_status(elevation):
	# Below 3 meters -> Extremely Low
	if elevation <= 3:
		return "Extremely Low"
	# Between 4 to 7 meters -> Very Low
	elif elevation <= 7:
		return "Very Low"
	# Between 8 to 10 meters -> Low
	elif elevation <= 10:
		return "Low"
	# Greater than 10 meters -> Average
	elif elevation > 10:
		return "Average"

# Read the data.
nyc_elevation = pd.read_csv("Elevation.csv", low_memory=False)
nyc_elevation = nyc_elevation[["ELEVATION", "the_geom"]]

# Split column the_geom into two new columns, "Longitude" and "Latitude".
nyc_elevation["the_geom"] = nyc_elevation["the_geom"].apply(lat_and_lon)
nyc_elevation[["Longitude", "Latitude"]] = nyc_elevation["the_geom"].str.split(" ", 1, expand=True)
nyc_elevation = nyc_elevation[["ELEVATION", "Longitude", "Latitude"]]

# Rename the columns.
nyc_elevation.columns = ["Elevation(ft)", "Longitude", "Latitude"]

# Add a column with elevation in meters.
nyc_elevation["Elevation(m)"] = nyc_elevation["Elevation(ft)"]/3.28

# Lower than 3 meters will be considered extremely low elevation point.
nyc_elevation["Elevation Status"] = nyc_elevation["Elevation(m)"].apply(elevation_status)
nyc_elevation["Longitude"] = nyc_elevation["Longitude"].apply(convert_string)
nyc_elevation["Latitude"] = nyc_elevation["Latitude"].apply(convert_string)
# print(nyc_elevation)

# NYC elevation.
# Count the number of elevation points by grouping their status.
nyc_elevation_status_count = nyc_elevation.groupby("Elevation Status").count().reset_index()

# Only get two columns from the data frame.
nyc_elevation_status_count = nyc_elevation_status_count.iloc[:, 0:2]

# Rename the columns.
nyc_elevation_status_count.columns = ["Elevation Status", "Count"]

# Sort the data frame according to Count.
nyc_elevation_status_count = nyc_elevation_status_count.sort_values(by=["Count"])
# print(nyc_elevation_status_count)
nyc_elevation_status_count.to_csv("nyc_elevation_status.csv", index=False)

# Separate the data frame according to column values Longitude and Latitude.
manhattan_elevation = nyc_elevation[(nyc_elevation["Longitude"]>=-74.02) & (nyc_elevation["Longitude"]<=-73.93)]
manhattan_elevation = manhattan_elevation[(manhattan_elevation["Latitude"]>=40.70) & (manhattan_elevation["Latitude"]<=40.87)]

brooklyn_elevation = nyc_elevation[(nyc_elevation["Longitude"]>=-74.04) & (nyc_elevation["Longitude"]<=-73.87)]
brooklyn_elevation = brooklyn_elevation[(brooklyn_elevation["Latitude"]>=40.57) & (brooklyn_elevation["Latitude"]<=40.73)]

queens_elevation = nyc_elevation[(nyc_elevation["Longitude"]>=-73.95) & (nyc_elevation["Longitude"]<=-73.71)]
queens_elevation = queens_elevation[(queens_elevation["Latitude"]>=40.54) & (queens_elevation["Latitude"]<=40.79)]

bronx_elevation = nyc_elevation[(nyc_elevation["Longitude"]>=-73.92) & (nyc_elevation["Longitude"]<=-73.77)]
bronx_elevation = bronx_elevation[(bronx_elevation["Latitude"]>=40.78) & (bronx_elevation["Latitude"]<=40.90)]

staten_island_elevation = nyc_elevation[(nyc_elevation["Longitude"]>=-74.25) & (nyc_elevation["Longitude"]<=-74.05)]
staten_island_elevation = staten_island_elevation[
	(staten_island_elevation["Latitude"]>=40.49) & (staten_island_elevation["Latitude"]<=40.64)]

# Count the number of elevation points by grouping their status.
manhattan_elevation_status_count = manhattan_elevation.groupby("Elevation Status").count().reset_index()
brooklyn_elevation_status_count = brooklyn_elevation.groupby("Elevation Status").count().reset_index()
queens_elevation_status_count = queens_elevation.groupby("Elevation Status").count().reset_index()
bronx_elevation_status_count = bronx_elevation.groupby("Elevation Status").count().reset_index()
staten_island_elevation_status_count = staten_island_elevation.groupby("Elevation Status").count().reset_index()

# Only get two columns from the data frame.
manhattan_elevation_status_count = manhattan_elevation_status_count.iloc[:, 0:2]
brooklyn_elevation_status_count = brooklyn_elevation_status_count.iloc[:, 0:2]
queens_elevation_status_count = queens_elevation_status_count.iloc[:, 0:2]
bronx_elevation_status_count = bronx_elevation_status_count.iloc[:, 0:2]
staten_island_elevation_status_count = staten_island_elevation_status_count.iloc[:, 0:2]

# Rename the columns.
manhattan_elevation_status_count.columns = ["Elevation Status", "Count"]
brooklyn_elevation_status_count.columns = ["Elevation Status", "Count"]
queens_elevation_status_count.columns = ["Elevation Status", "Count"]
bronx_elevation_status_count.columns = ["Elevation Status", "Count"]
staten_island_elevation_status_count.columns = ["Elevation Status", "Count"]

# Sort the data frame according to Count.
manhattan_elevation_status_count = manhattan_elevation_status_count.sort_values(by=["Count"])
brooklyn_elevation_status_count = brooklyn_elevation_status_count.sort_values(by=["Count"])
queens_elevation_status_count = queens_elevation_status_count.sort_values(by=["Count"])
bronx_elevation_status_count = bronx_elevation_status_count.sort_values(by=["Count"])
staten_island_elevation_status_count = staten_island_elevation_status_count.sort_values(by=["Count"])

# print(manhattan_elevation_status_count)
# print(brooklyn_elevation_status_count)
# print(queens_elevation_status_count)
# print(bronx_elevation_status_count)
# print(staten_island_elevation_status_count)
manhattan_elevation_status_count.to_csv("manhattan_elevation_status.csv", index=False)
brooklyn_elevation_status_count.to_csv("brooklyn_elevation_status.csv", index=False)
queens_elevation_status_count.to_csv("queens_elevation_status.csv", index=False)
bronx_elevation_status_count.to_csv("bronx_elevation_status.csv", index=False)
staten_island_elevation_status_count.to_csv("staten_island_elevation_status.csv", index=False)

# For Stacked Bar Chart
# Swap index and columns.
mh_count = manhattan_elevation_status_count.transpose()
bk_count = brooklyn_elevation_status_count.transpose()
q_count = queens_elevation_status_count.transpose()
bx_count = bronx_elevation_status_count.transpose()
si_count = staten_island_elevation_status_count.transpose()

# Reset Index.
mh_count = mh_count.reset_index()
bk_count = bk_count.reset_index()
q_count = q_count.reset_index()
bx_count = bx_count.reset_index()
si_count = si_count.reset_index()

# Rename columns, remove duplicated header and Add "Manhattan" to the region column.
mh_count.columns = ["Region", "Extremely Low", "Low", "Very Low", "Average"]
mh_count = mh_count.iloc[1:]
mh_count.iloc[0,0] = "Manhattan"

# Rename columns, remove duplicated header and Add "Brooklyn" to the region column.
bk_count.columns = ["Region", "Extremely Low", "Low", "Very Low", "Average"]
bk_count = bk_count.iloc[1:]
bk_count.iloc[0,0] = "Brooklyn"

# Rename columns, remove duplicated header and Add "Queens" to the region column.
q_count.columns = ["Region", "Extremely Low", "Low", "Very Low", "Average"]
q_count = q_count.iloc[1:]
q_count.iloc[0,0] = "Queens"

# Rename columns, remove duplicated header and Add "Bronx" to the region column.
bx_count.columns = ["Region", "Extremely Low", "Low", "Very Low", "Average"]
bx_count = bx_count.iloc[1:]
bx_count.iloc[0,0] = "Bronx"

# Rename columns, remove duplicated header and Add "Staten Island" to the region column.
si_count.columns = ["Region", "Extremely Low", "Low", "Very Low", "Average"]
si_count = si_count.iloc[1:]
si_count.iloc[0,0] = "Staten Island"

# Concatenate the five dataframes from the five boroughs.
# Due to the approximation of the boundaries on longitude and latitude, 
# some elevation points might repeat in two or more boroughs.
concat_result = pd.concat([mh_count, bk_count, q_count, bx_count, si_count])
# print(concat_result)
concat_result.to_csv("nyc_stacked.csv", index=False)

# Bar Chart.
# Coastal Population Density vs Non-Coastal Population Density.

# Return the integer part of the NTA Code.
def nta_number(nta_code):
	return int(nta_code[2:4])

# Brooklyn
# Determine if it's a coastal neighborhood or a non-coastal neightborhood.
# And return the neighborhood type.
def bk_neighborhood_type(nta):
	if ((nta == 17) | (nta == 19) | (nta == 21) | (nta == 23) |
		(nta == 26) | (nta == 27) | (nta == 29) | (nta == 31) |
		(nta == 32) | (nta == 33) | (nta == 38) | (nta == 73) |
		(nta == 76) | (nta == 90) | (nta == 77) | (nta == 83) |
		(nta == 82) | (nta == 93) | (nta == 50) |	(nta == 45) |
		(nta == 9)):
		return "Coastal Neighborhood"
	else:
		return "Non-Coastal Neighborhood"

# Bronx
# Determine if it's a coastal neighborhood or a non-coastal neightborhood.
# And return the neighborhood type.
def bx_neighborhood_type(nta):
	if ((nta == 22) | (nta == 29) | (nta == 30) | (nta == 36) |
		(nta == 26) | (nta == 63) | (nta == 39) | (nta == 27) |
		(nta == 9) | (nta == 52) | (nta == 98) | (nta == 10) |
		(nta == 3) | (nta == 62)):
		return "Coastal Neighborhood"
	else:
		return "Non-Coastal Neighborhood"

# Manhattan
# Determine if it's a coastal neighborhood or a non-coastal neightborhood.
# And return the neighborhood type.
def mn_neighborhood_type(nta):
	if ((nta == 1) | (nta == 35) | (nta == 36) | (nta == 4) |
		(nta == 6) | (nta == 3) | (nta == 9) | (nta == 34) |
		(nta == 12) | (nta == 14) | (nta == 33) | (nta == 32) |
		(nta == 31) | (nta == 15) | (nta == 13) | (nta == 19) |
		(nta == 20) | (nta == 50) | (nta == 23) | (nta == 24) |
		(nta == 25) | (nta == 27) | (nta == 28)):
		return "Coastal Neighborhood"
	else:
		return "Non-Coastal Neighborhood"

# Queens
# Determine if it's a coastal neighborhood or a non-coastal neightborhood.
# And return the neighborhood type.
def qn_neighborhood_type(nta):
	if ((nta == 10) | (nta == 12) | (nta == 15) | (nta == 57) |
		(nta == 56) | (nta == 53) | (nta == 20) | (nta == 30) |
		(nta == 31) | (nta == 68) | (nta == 71) | (nta == 72) |
		(nta == 23) | (nta == 49) | (nta == 47) | (nta == 22) |
		(nta == 46) | (nta == 45) | (nta == 44) | (nta == 43) |
		(nta == 34) | (nta == 33) | (nta == 5)):
		return "Coastal Neighborhood"
	else:
		return "Non-Coastal Neighborhood"

# Staten Island
# Determine if it's a coastal neighborhood or a non-coastal neightborhood.
# And return the neighborhood type.
def si_neighborhood_type(nta):
	if ((nta == 5) | (nta == 12) | (nta == 28) | (nta == 22) |
		(nta == 37) | (nta == 14) | (nta == 36) | (nta == 45) |
		(nta == 25) | (nta == 54) | (nta == 1) | (nta == 11)):
		return "Coastal Neighborhood"
	else:
		return "Non-Coastal Neighborhood"
		
# Read dataset.
population = pd.read_csv("New_York_City_Population_By_Neighborhood_Tabulation_Areas.csv")

# Select rows with Year = 2010. The most recent year found on this dataset.
population = population[population["Year"]==2010]

# Separate the data frame according to column value Borough.
bk_population = population[population["Borough"]=="Brooklyn"].copy()
bx_population = population[population["Borough"]=="Bronx"].copy()
mn_population = population[population["Borough"]=="Manhattan"].copy()
qn_population = population[population["Borough"]=="Queens"].copy()
si_population = population[population["Borough"]=="Staten Island"].copy()

# Apply function to get each neighborhood's nta number.
bk_population["nta"] = bk_population["NTA Code"].apply(nta_number)
bx_population["nta"] = bx_population["NTA Code"].apply(nta_number)
mn_population["nta"] = mn_population["NTA Code"].apply(nta_number)
qn_population["nta"] = qn_population["NTA Code"].apply(nta_number)
si_population["nta"] = si_population["NTA Code"].apply(nta_number)

# Apply function to get the neighborhood type.
bk_population["Neighborhood Type"] = bk_population["nta"].apply(bk_neighborhood_type)
bx_population["Neighborhood Type"] = bx_population["nta"].apply(bx_neighborhood_type)
mn_population["Neighborhood Type"] = mn_population["nta"].apply(mn_neighborhood_type)
qn_population["Neighborhood Type"] = qn_population["nta"].apply(qn_neighborhood_type)
si_population["Neighborhood Type"] = si_population["nta"].apply(si_neighborhood_type)

# Count the population in both Coastal Neighborhood and Non-Coastal Neighborhood.
bk_population = bk_population.groupby("Neighborhood Type")["Population"].sum().reset_index()
bx_population = bx_population.groupby("Neighborhood Type")["Population"].sum().reset_index()
mn_population = mn_population.groupby("Neighborhood Type")["Population"].sum().reset_index()
qn_population = qn_population.groupby("Neighborhood Type")["Population"].sum().reset_index()
si_population = si_population.groupby("Neighborhood Type")["Population"].sum().reset_index()

# print(bk_population)
# print(bx_population)
# print(mn_population)
# print(qn_population)
# print(si_population)
bk_population.to_csv("bk_population.csv", index=False)
bx_population.to_csv("bx_population.csv", index=False)
mn_population.to_csv("mn_population.csv", index=False)
qn_population.to_csv("qn_population.csv", index=False)
si_population.to_csv("si_population.csv", index=False)

# Stacked Bar Chart for NYC population.
# Swap index and header.
bk_population = bk_population.transpose().reset_index()
bx_population = bx_population.transpose().reset_index()
mn_population = mn_population.transpose().reset_index()
qn_population = qn_population.transpose().reset_index()
si_population = si_population.transpose().reset_index()

# Rename columns.
bk_population.columns = ["Region", "Coastal Neighborhood", "Non-Coastal Neighborhood"]
bx_population.columns = ["Region", "Coastal Neighborhood", "Non-Coastal Neighborhood"]
mn_population.columns = ["Region", "Coastal Neighborhood", "Non-Coastal Neighborhood"]
qn_population.columns = ["Region", "Coastal Neighborhood", "Non-Coastal Neighborhood"]
si_population.columns = ["Region", "Coastal Neighborhood", "Non-Coastal Neighborhood"]

# Remove duplicated header.
bk_population = bk_population.drop(0)
bx_population = bx_population.drop(0)
mn_population = mn_population.drop(0)
qn_population = qn_population.drop(0)
si_population = si_population.drop(0)

# Add the correct borough name to the data frame.
bk_population.iloc[0,0] = "Brooklyn"
bx_population.iloc[0,0] = "Bronx"
mn_population.iloc[0,0] = "Manhattan"
qn_population.iloc[0,0] = "Queens"
si_population.iloc[0,0] = "Staten Island"
# print(bk_population)

nyc_population = pd.concat([bk_population, bx_population, mn_population, qn_population, si_population])
nyc_population.to_csv("nyc_population.csv", index=False)
# print(nyc_population)
