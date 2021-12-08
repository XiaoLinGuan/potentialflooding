"""
Clean and Filter the datasets
"""
import pandas as pd

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

# Swap index column with header.
global_sea_level = global_sea_level.swapaxes("index", "columns")

# Reset index column.
global_sea_level = global_sea_level.reset_index()

# Remove unwanted rows from the data frame.
global_sea_level = global_sea_level.iloc[6:]

# Rename the columns for applying functions.
global_sea_level.columns = ["Year", "Centimeter"]
global_sea_level["Year"] = global_sea_level["Year"].apply(specific_year)
global_sea_level["Inch"] = (global_sea_level["Centimeter"]/2.54).apply(whole_number)
global_sea_level["Region"] = "Global"
global_sea_level.to_csv("global_sea_level.csv", index=False)
# print(global_sea_level)

# East Coast
# Find all the locations on th east coast according to their latitude and longitude.
east_coast_sea_level = df[(df["Latitude"]>=24) & (df["Latitude"]<=44)]
east_coast_sea_level = df[(df["Longitude"]>=-82) & (df["Longitude"]<=-66)]

# Find all the rows with 1.0 HIGH Scenario.
east_coast_sea_level = east_coast_sea_level[east_coast_sea_level["Scenario"]=="1.0 - HIGH"]

# Remove the unwanted columns from the data frame.
east_coast_sea_level = east_coast_sea_level.iloc[:,6:21]

# Take the median of each column.
east_coast_sea_level = east_coast_sea_level.median()
east_coast_sea_level = east_coast_sea_level.reset_index()

# Rename the columns for applying functions.
east_coast_sea_level.columns = ["Year", "Centimeter"]
east_coast_sea_level["Year"] = east_coast_sea_level["Year"].apply(specific_year)
east_coast_sea_level["Inch"] = (east_coast_sea_level["Centimeter"]/2.54).apply(whole_number)
east_coast_sea_level["Region"] = "East Coast"
east_coast_sea_level.to_csv("east_coast_sea_level.csv", index=False)
# print(east_coast_sea_level)

# NYC
nyc_sea_level = df[(df["Site"]=="NEW YORK") & (df["Scenario"] == "1.0 - HIGH")]

# Swap index column with header.
nyc_sea_level = nyc_sea_level.swapaxes("index", "columns")

# Reset index column.
nyc_sea_level = nyc_sea_level.reset_index()

# Remove unwanted rows from the data frame.
nyc_sea_level = nyc_sea_level.iloc[6:]

# Rename the columns for applying functions.
nyc_sea_level.columns = ["Year", "Centimeter"]
nyc_sea_level["Year"] = nyc_sea_level["Year"].apply(specific_year)
nyc_sea_level["Inch"] = (nyc_sea_level["Centimeter"]/2.54).apply(whole_number)
nyc_sea_level["Region"] = "NYC"
nyc_sea_level.to_csv("nyc_sea_level.csv", index=False)
# print(nyc_sea_level)

# ALl three regions
all_three_regions_sea_level = pd.concat([global_sea_level, east_coast_sea_level, nyc_sea_level])
all_three_regions_sea_level.to_csv("all_three_regions_sea_level.csv", index=False)
# print(all_three_regions_sea_level)

"""
Scatter Plot -> Tropical Cyclones Pattern
"""
# Number of tropical cyclones formed on the Atlantic Ocean.
# Read dataset.
df = pd.read_csv("ibtracs.NA.list.v04r00.csv", skiprows=[1], low_memory=False)
# print(df)

# Take only the rows with nature value equal to HU, TS, or TD.
df = df[(df["USA_STATUS"]=="HU") | (df["USA_STATUS"]=="TS") | (df["USA_STATUS"]=="TD")]

# Take only three columns from the original dataset.
df1 = df[["SID", "SEASON", "USA_STATUS"]]

# Keep one instance of each unique cyclone id.
df1 = df1.drop_duplicates(subset="SID", keep="last")

# Count the number of cyclones formed each year by grouping SEASON and USA_STATUS.
df1 = df1.groupby(["SEASON", "USA_STATUS"]).count()

# Reset index.
atlantic_ocean_cyclones_count = df1.reset_index()

# Rename the columns.
atlantic_ocean_cyclones_count.columns = ["Year", "Category", "Count"]
atlantic_ocean_cyclones_count.to_csv("atlantic_ocean_cyclones_count.csv", index=False)
# print(atlantic_ocean_cyclones_count)

# Number of tropical cyclones made landfall on the East Coast.
# Take only the rows with USA_RECORD equal to L, which means made landfall on the East Coast.
df2 = df[df["USA_RECORD"]=="L"]

# Take only three columns from the data frame.
df2 = df2[["SID", "SEASON", "USA_STATUS"]]

# Keep one instance of each unique cyclone id.
df2 = df2.drop_duplicates(subset="SID", keep="last")

# Count the number of cyclones made landfall on East coast each year by grouping SEASON and USA_STATUS.
df2 = df2.groupby(["SEASON", "USA_STATUS"]).count()

# Reset index.
east_coast_landfall_count = df2.reset_index()

# Rename the columns.
east_coast_landfall_count.columns = ["Year", "Category", "Count"]
east_coast_landfall_count.to_csv("east_coast_landfall_count.csv", index=False)
# print(east_coast_landfall_count)

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
