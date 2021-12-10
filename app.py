import dash
from dash import dcc
from dash import html
from dash import dash_table
from dash.dash_table.Format import Group
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from pandas.core.groupby.generic import DataFrameGroupBy
import plotly.express as px
import statsmodels.api as sm
import datasets

"""
Build the Web App
"""
app = dash.Dash(
	external_stylesheets=[dbc.themes.FLATLY]
)
server = app.server

tab_style = {
	"border": "2px solid #97CBEC",
	"border-radius": "20px",
	"font-size": "120%",
}

selected_tab_style = {
	"background-color": "#C3E0E5",
	"border": "2px solid #97CBEC",
	"border-radius": "20px",
	"font-weight": "bold",
	"font-size": "120"
}

overview_content_style = {
	"background-color": "#EAF2F8",
	"border": "5px solid white",
	"border-radius": "20px",
}

lg_data_download_button_style = {
	"border": "1px solid #174978", 
	"border-Radius": "15px"
}

sp_data_download_button_style = {
	"border": "1px solid #405A45",
	"border-Radius": "15px"
}

"""
Title of the dashboard
"""
title = html.Div([
	html.H1(
		["Potential Coastal Flooding of NYC as Sea Level rises"],
		style = {
			"height": "50px",
			"font-size": "40px",
			"text-align": "center",
			"border": "1px solid white",
			"border-radius": "20px",
			"background-image": "linear-gradient(to bottom, #B7F8DB, #50A7C2)"
		}
	)	
], style={"margin-left": "10px", "margin-right": "10px"})

"""
Tab1
Introduction content
Descriprtion of the web app and data sources
"""
tab1 = html.Div([
	html.H4("CSCI39542 Intro to Data Science Project"),
	html.H3(""),

	# Image link of Sandy
	# Image link of Ida
	
	# Brief description of Line Graph
	# and explain how the data is obtained and processed
	html.H5("Line Graph", style={"color": "#174978", "margin-left": "5px"}),

	# Brief description of Scatter Plot
	# and explain how the data is obtained and processed
	html.H5("Scatter Plot", style={"color": "#405A45", "margin-left": "5px"}),

	# Brief description of Choropleth Map
	# and explain how the data is obtained and processed
	html.H5("Choropleth Map", style={"color": "", "margin-left": "5px"}),

	# Brief description of Bar Chart
	# and explain how the data is obtained and processed
	html.H5("Bar Chart", style={"color": "", "margin-left": "5px"}),

	# Data sources
	html.H5("Original Data Sources:", style={"margin-left": "5px"}),
	# html.H6(html.Ul(html.A(html.H6("sea level rise", style={"color": "purple"}), href="https://dash.plotly.com/dash-html-components/img", target="_blank"),)),
	# https://www.ncei.noaa.gov/data/international-best-track-archive-for-climate-stewardship-ibtracs/v04r00/access/csv/ (Choose ibtracs.NA.list.v04r00.csv)
	html.H5("😂📉Just testing if copying an emoji directly to my web app will work"),

	html.Hr(style={"border": "1px dashed white"})

], id="overview_tab_content", style=overview_content_style)
# End of Tab1

"""
Tab2
Line Graph content and Scatter Plot content
Line Graph will be showing sea-level rise trend
Scatter Plot will be showing tropical cyclones pattern
"""
tab2 = html.Div([

	# Line Graph content
	html.Div([
		# Line Graph Description
		html.H4("Sea Level Trend", style={"color": "#174978", "margin-left": "10px"}),
		html.P([
			"As the emission of CO", html.Sub("2"), 
			"""
			and other greenhouse gases increase, global warming becomes one of
			the main concerns to coastal cities. It triggers glaciers and ice 
			sheets to melt rapidly, which causes the sea level to rise more 
			drastically than in the past. NYC, one of the biggest coastal cities 
			in the world, has a population of more than eight million people is 
			at high risk of constant flooding. By comparing the relative sea-level
			rise on a global scale and in NYC, NYC has a higher chance of experiencing
			a more drastic sea-level increase. Even when we compare NYC"s mean 
			sea-level rise to the data of the East Coast, NYC will still take the
			lead in experiencing an acceleration of sea-level rise. 
			"""
		], style={"color": "#174978", "text-align": "justify", "margin-left": "10px", "margin-right": "10px"}),

		html.Hr(style={"border-top": "2px dashed #A0D6B4", "margin-left": "10px", "margin-right": "10px"}),

		# Line Graph options
		html.H5("Choose a region:", style={"color": "#2181A1", "margin-left": "10px"}),
		dbc.RadioItems(
			options=[
				{"label": "Global", "value": "global_sl"},
				{"label": "East Coast", "value": "east_coast_sl"},
				{"label": "NYC", "value": "nyc_sl"},
				{"label": "All Three Regions", "value": "all_sl"}
			],
			value="global_sl",
			inline=True,
			id="line_graph_radioitems_region",
			label_checked_style={"color": "#2181A1"},
			style={"margin-left": "10px"}
		),
		html.H5("Choose the unit:", style={"color": "#2181A1", "margin-left": "10px"}),
		dbc.RadioItems(
			options=[
				{"label": "inch", "value": "measure_inch"},
				{"label": "cm", "value": "measure_cm"}
			], 
			value="measure_inch",
			inline=True,
			id="line_graph_radioitems_measurement",
			label_checked_style={"color": "#2181A1"},
			style={"margin-left": "10px"}
		),

		# Line Graph
		dcc.Graph(id="line_graph"),

		# Options to show or hide line graph dataset
		dbc.RadioItems(
			options=[
				{"label": "Show Dataset", "value": "l_g_show_dataset"},
				{"label": "Hide Dataset", "value": "l_g_hide_dataset"}
			],
			value="l_g_hide_dataset",
			inline=True,
			id="line_graph_show_dataset",
			label_style={"font-size": "20px", "color": "#174978"},
			style={"margin-left": "10px"}
		),

		# Examples of applying filter on the dataset
		html.Div(id="line_graph_filter_example", style={"margin-left": "10px"}),
	
		# Line Graph Dataset
		# By default, the dataset is hidden so that user can focus on the graph
		html.Div(id="line_graph_dataset", style={"margin-left": "10px", "margin-right": "10px"}),

		# Dropdown menu for users to download datasets used in line graph
		html.Div([
			html.H6(html.I(html.B("Download datasets used in line graph: ")), style={"margin-left": "10px"}),
			html.Div([
				dcc.Dropdown(
					options=[
						{"label": "global_sea_level_rise.csv", "value": "global_sea_level_rise"},
						{"label": "east_coast_sea_level_rise.csv", "value": "east_coast_sea_level_rise"},
						{"label": "nyc_sea_level_rise.csv", "value": "nyc_sea_level_rise"},
						{"label": "all_three_regions_sea_level_rise.csv", "value": "all_three_regions_sea_level_rise"}
					],
					placeholder="Pick a dataset",
					id="line_graph_download_option",
					style={"background-color": "#EAF2F8", "border-radius": "10px", "color": "#174978"}
				),
				dcc.Download(id="line_graph_download_data")
			],style={"margin-left": "10px", "margin-right": "950px"}),
			html.H6(
				html.I([
					"""
					The datasets are cleaned and modified for plotting. To read or download 
					the original datasets, please click on 
					""", 
					html.B("Conclusion"), 
					""", scroll to the bottom of the page, and click on any links under Data 
					Sources. Sorry for the inconvenience.
					"""
				]),
			style={"text-align": "justify", "margin-left": "10px", "margin-right": "10px"})
		])
	], style={"background-color": "#CDDEEE", "border": "5px solid white", "border-radius": "20px"}),
	# End of Line Graph Content

	# Scatter Plot content
	html.Div([
		# Scatter Plot Descriprtion
		html.H4("Tropical Cyclone Pattern", style={"color": "#405A45", "margin-left": "10px"}),
		html.P(
			"""
			With the help of warmer ocean temperatures, tropical cyclones will 
			intensify much easier and faster than in the past. With only a few 
			centimeters of the sea-level rise, they will push more water inland, 
			allowing them to affect a more significant part of the coastal regions. 
			As we look at the scatter plot below, we will see the overall trend 
			that more tropical cyclones are developing on the Atlantic Ocean and 
			making landfalls on the East Coast. Even though the chart shows, most 
			tropical cyclones hit other parts of the East Coast instead of making 
			landfalls in the tri-state region. The truth is, if we look closely at 
			the chart, where the number of cyclones affected or made landfalls in 
			tri-state and NYC, we can see that NYC is getting hit by tropical 
			cyclones more frequently in recent years. And that increases the chance 
			of NYC suffering from severe coastal flooding in the future.	
			""",
		style={"color": "#405A45", "text-align": "justify", "margin-left": "10px", "margin-right": "10px"}),

		html.Hr(style={"border-top": "2px dashed #A0D6B4", "margin-left": "10px", "margin-right": "10px"}),

		# Scatter Plot options
		html.H5("Choose a region:", style={"color": "#568203", "margin-left": "10px"}),
		dbc.RadioItems(
			options=[
				{"label": "Atlantic Ocean", "value": "ao_c"},
				{"label": "East Coast Landfalls", "value": "ec_c"},
				{"label": "Tri-State Landfalls/Affected NYC", "value": "tri_state_c"}
			],
			value="ao_c",
			inline=True,
			id="scatter_plot_radioitems",
			label_checked_style={"color": "#568203"},
			style={"margin-left": "10px"}
		),
		html.Br(),
		dbc.ListGroup([
			dbc.ListGroupItem("HU-Hurricane", id="hu"),
			dbc.ListGroupItem("TS-Tropical Storm", id="ts"),
			dbc.ListGroupItem("TD-Tropical Depression", id="td")
		],horizontal=True, style={"background-color": "#DDF2D1", "margin-left": "10px"}),

		# Scatter Plot
		dcc.Graph(id="scatter_plot"),

		# Options to show or hide scatter plot dataset
		dbc.RadioItems(
			options=[
				{"label": "Show Dataset", "value": "s_c_show_dataset"},
				{"label": "Hide Dataset", "value": "s_c_hide_dataset"}
			],
			value="s_c_hide_dataset",
			inline=True,
			id="scatter_plot_show_dataset",
			label_style={"font-size": "20px", "color": "#405A45"},
			style={"margin-left": "10px"}
		),

		# Examples of applying filter on the dataset
		html.Div(id="scatter_plot_filter_example", style={"margin-left": "10px"}),

		# Scatter Plot Dataset
		# By default, the dataset is hidden so that user can focus on the plot
		html.Div(id="scatter_plot_dataset", style={"margin-left": "10px", "margin-right": "10px"}),

		# Dropdown menu for users to download datasets used in scatter plot
		html.Div([
			html.H6(html.I(html.B("Download datasets used in line graph: ")), style={"margin-left": "10px"}),
			html.Div([
				dcc.Dropdown(
					options=[
						{"label": "atlantic_ocean_cyclones_count.csv", "value": "atlantic_ocean_dataset"},
						{"label": "east_coast_landfall_count.csv", "value": "east_coast_landfall_dataset"},
						{"label": "tri_state_and_nyc_landfall_count.csv", "value": "tri_state_and_nyc_dataset"}
					],
					placeholder="Pick a dataset",
					id="scatter_plot_download_option",
					style={"background-color": "#EFF8EA", "border-radius": "10px", "color": "#405A45"}
				),
				dcc.Download(id="scatter_plot_download_data")
			],style={"margin-left": "10px", "margin-right": "950px"}),
			html.H6(
				html.I([
					"""
					The datasets are cleaned and modified for plotting. To read or download 
					the original datasets, please click on 
					""", 
					html.B("Conclusion"), 
					""", scroll to the bottom of the page, and click on any links under Data 
					Sources. Sorry for the inconvenience.
					"""
				]),
			style={"text-align": "justify", "margin-left": "10px", "margin-right": "10px"})
		])
	], style={"background-color": "#DDF2D1", "border": "5px solid white", "border-radius": "20px"})
	# End of Scatter Plot Content
])
# End of Tab2

"""
Tab3
Bar Chart and Bubble Chat content
Bar Chart will be showing the elevation status and population of NYC
Bubble Chart will be showing the probability of a rare flooding event occur
in the future and an approximate land coverage(in square miles) by the flood
"""
tab3 = html.Div([
	# Bar Chart content
	html.Div([
		# Bar Chart Description
		html.H4("NYC Elevation", style={"color": "#056A54", "margin-left": "10px"}),
		html.P([
			"""
			NYC, one of the world's biggest coastal cities with an elevation of 
			only approximately thirty-three feet or ten meters, has been facing 
			an increasing amount of stress over storm surge in recent years. In 
			the following bar chart, although we can see that most of NYC's elevation 
			points are greater than ten meters and are under the category of "Average." 
			They are, in fact, below average and often considered at risk of high-tide 
			flooding if they are near the shoreline. Some might say we can avoid 
			taking the risk if we don't go to places with a low elevation point, 
			which is a common misunderstanding. Many people might not realize 
			that almost half of NYC's population lives in coastal neighborhoods. 
			As we click on "population" as the focus of the bar chart, we will 
			see that in each borough, there is a significant number of residents 
			living in coastal regions. In both Manhattan and Staten Island, more 
			than half of their population live in coastal neighborhoods. How can 
			New Yorkers avoid going to the low elevation zone? It's impossible 
			and given there is a huge part of NYC's population living in coastal 
			areas, as the sea level rises more quickly than before, more of us 
			will be at risk of being affected by future flooding.
			"""
		], style={"color": "#056A54", "text-align": "justify", "margin-left": "10px", "margin-right": "10px"}),

		html.Hr(style={"border-top": "2px dashed #85CD92", "margin-left": "10px", "margin-right": "10px"}),

		# Bar Chart options
		html.H5("Choose one of the two variables:", style={"color": "#056A54", "margin-left": "10px"}),
		dbc.RadioItems(
			options=[
				{"label": "Elevation Status", "value": "elevation_status"},
				{"label": "Population", "value": "population"}
			], 
			value="elevation_status",
			inline=True,
			id="bar_chart_variable",
			label_checked_style={"color": "#056A54"},
			style={"margin-left": "10px"}
		),
		html.Div([
			html.H5("Choose a borough:", style={"color": "#339966", "margin-left": "10px"}),
			dbc.RadioItems(
				options=[
					{"label": "NYC", "value": "nyc_bar"},
					{"label": "Brooklyn", "value": "bk_bar"},
					{"label": "Bronx", "value": "bx_bar"},
					{"label": "Manhattan", "value": "mh_bar"},
					{"label": "Queens", "value": "q_bar"},
					{"label": "Staten Island", "value": "si_bar"}
				], 
				value="nyc_bar",
				inline=True,
				id="bar_chart_radioitems_region",
				label_checked_style={"color": "#339966"},
				style={"margin-left": "10px"}
			),
			html.Div([
				html.H6("Choose a way to display the bar chart(Only applies to NYC): ",
					style={"color": "#339933", "margin-left": "10px"}),
				dbc.RadioItems(
					options=[
						{"label": "Stacked", "value": "stacked_bar_chart"},
						{"label": "Regular", "value": "regular_bar_chart"}
					],
					value="regular_bar_chart",
					inline=True,
					id="bar_chart_radioitems_stack",
					label_checked_style={"color": "#339933"},
					style={"margin-left": "10px", "font-size": "14px"}
				)
			], id="stacked_bar_chart_option")
		]),

		html.Br(),

		# Elevation classification.
		html.Div([
			html.H6([html.B("Extremely Low: "), 
				"Elevation point that is below or equal to 3 meters above sea level."]),
			html.H6([html.B("Very Low: "), 
				"Elevation point that is between 4 to 7 meters above sea level."]),
			html.H6([html.B("Low: "), 
				"Elevation point that is between 8 to 10 meters above sea level."]),
			html.H6([html.B("Average: "), 
				"Elevation point that is greater than or equal to 10 meters."])
		], id="elevation_classificaton"),

		# Population classification.
		html.Div([
			html.H6([html.B("Coastal Neighborhood: "), 
				"Neighborhood that is bordering the shoreline."]),
			html.H6([html.B("Non-Coastal Neighborhood: "), 
				"Neighborhood that is not bordering the shoreline, or inland."])
		], id="population_classification"),

		# Bar Chart
		dcc.Graph(id="bar_chart"),

		# Options to show or hide bar chart dataset
		dbc.RadioItems(
			options=[
				{"label": "Show Dataset", "value": "b_c_show_dataset"},
				{"label": "Hide Dataset", "value": "b_c_hide_dataset"}
			],
			value="b_c_hide_dataset",
			inline=True,
			id="bar_chart_show_dataset",
			label_style={"font-size": "20px", "color": "#056A54"},
			style={"margin-left": "10px"}
		),

		# Examples of applying filter on the dataset
		html.Div(id="bar_chart_filter_example", style={"margin-left": "10px"}),

		# Bar Chart Dataset
		# By default, the dataset is hidden so that user can focus on the chart
		html.Div(id="bar_chart_dataset", style={"margin-left": "10px", "margin-right": "10px"}),
	
		# Dropdown menu for users to download datasets used in bar chart
		html.Div([
			html.H6(html.I(html.B("Download datasets used in bar chart: ")), style={"margin-left": "10px"}),
			html.Div([
				dcc.Dropdown(
					options=[
						{"label": "nyc_elevation_status_count.csv", "value": "nyc_esc1"},
						{"label": "nyc_elevation_status_count_stacked.csv", "value": "nyc_esc2"},
						{"label": "brooklyn_elevation_status_count.csv", "value": "bk_esc"},
						{"label": "bronx_elevation_status_count.csv", "value": "bx_esc"},
						{"label": "manhattan_elevation_status_count.csv", "value": "mh_esc"},
						{"label": "queens_elevation_status_count.csv", "value": "q_esc"},
						{"label": "staten_island_elevation_status_count.csv", "value": "si_esc"},
						{"label": "nyc_coastal_vs_non_coastal.csv", "value": "nyc_p"},
						{"label": "brooklyn_coastal_vs_non_coastal.csv", "value": "bk_p"},
						{"label": "bronx_coastal_vs_non_coastal.csv", "value": "bx_p"},
						{"label": "manhattan_coastal_vs_non_coastal.csv", "value": "mn_p"},
						{"label": "queens_coastal_vs_non_coastal.csv", "value": "qn_p"},
						{"label": "staten_island_vs_non_coastal.csv", "value": "si_p"}
					],
					placeholder="Pick a dataset",
					id="bar_chart_download_option",
					style={"background-color": "#E3F0DD", "border-radius": "10px", "color": "#056A54"}
				),
				dcc.Download(id="bar_chart_download_data")
			],style={"margin-left": "10px", "margin-right": "900px"}),
			html.H6(
				html.I([
					"""
					The datasets are cleaned and modified for plotting. To read or download 
					the original datasets, please click on 
					""", 
					html.B("Conclusion"), 
					""", scroll to the bottom of the page, and click on any links under Data 
					Sources. Sorry for the inconvenience.
					"""
				]),
			style={"text-align": "justify", "margin-left": "10px", "margin-right": "10px"})
		])

	], style={"background-color": "#C1E3C4", "border": "5px solid white", "border-radius": "20px"}),
	# End of Bar Chat Content

	# Bubble Chart content
	html.Div([
		# Bubble Chart Description
		html.H4("Possible Flood Coverage",  
			style={"color": "#053845", "margin-left": "10px"}),
		html.P([
			"""
			Given almost half the population lives in coastal areas, 
			NYC will face another challenge when rare and severe flooding 
			such as the ones that occur approximately once in a hundred years 
			or once in five hundred years becomes more frequent. The following 
			bubble chart represents the potential flooding coverage during a 
			100-year flood in five different years. The federal emergency 
			management agency initially developed this model to improve our 
			city's urban planning by keeping people aware of places with higher 
			exposure to flooding than other places. But this model only takes 
			sea level as the reason that it will cause flooding. It ignores many 
			different factors such as heavy rain, broken drainage system, lack 
			of vegetation. Many had turned to other models for the prediction 
			of flooding. However, this model still covers the overall trend of 
			potential flood coverage in NYC, and we can see how a few inches of 
			sea-level rise would damage NYC. 
			"""
		], style={"color": "#053845", "text-align": "justify", "margin-left": "10px", "margin-right": "10px"}),
		html.P([
			"""
			At first, when I plotted the data points onto the chart, I didn't 
			think that the flood coverage changed drastically because the data 
			points didn't seem to increase a lot in size. Then, I checked their 
			possible coverage area. After searching NYC's land area, I realize 
			that if NYC's sea-level trend follows this model, we will be left 
			with approximately two-thirds of NYC's land area by the end of the 
			century. NYC only has a land area of roughly 302 square miles. In 
			2050, if a 100-year flood occur, 72 square miles of NYC would 
			experience flooding. That's more than one-fourth of NYC's land area. 
			And if we move onto the last data point on this chart, with a 75 inches 
			increase in sea level, a 100-year flood would flood 91 square miles of NYC, 
			which is almost one-third of the land area. We know that there are a 
			lot of residents living in coastal neighborhoods, and this will be a 
			disaster for most people.  
			"""
		], style={"color": "#053845", "text-align": "justify", "margin-left": "10px", "margin-right": "10px"}),

		html.Hr(style={"border-top": "2px dashed #85CD92", "margin-left": "10px", "margin-right": "10px"}),
		
		dcc.Graph(id="bubble_chart"),

		# Options to show or hide bubble chart dataset
		dbc.RadioItems(
			options=[
				{"label": "Show Dataset", "value": "bub_c_show_dataset"},
				{"label": "Hide Dataset", "value": "bub_c_hide_dataset"}
			],
			value="bub_c_hide_dataset",
			inline=True,
			id="bubble_chart_show_dataset",
			label_style={"font-size": "20px", "color": "#053845"},
			style={"margin-left": "10px"}
		),

		# Examples of applying filter on the dataset
		html.Div(id="bubble_chart_filter_example", style={"margin-left": "10px"}),

		# Bubble Chart Dataset
		# By default, the dataset is hidden so that user can focus on the chart
		html.Div(id="bubble_chart_dataset", style={"margin-left": "10px", "margin-right": "10px"}),
		
		# Dropdown menu for users to download dataset used in bubble chart
		html.Div([
			html.H6(html.I(html.B("Download datasets used in bubble chart: ")), style={"margin-left": "10px"}),
			html.Div([
				dcc.Dropdown(
					options=[
						{"label": "100_year_flood_data.csv", "value": "flood_data"}
					],
					placeholder="Pick a dataset",
					id="bubble_chart_download_option",
					style={"background-color": "#C9EAF2", "border-radius": "10px", "color": "#0067A5"}
				),
				dcc.Download(id="bubble_chart_download_data")
			],style={"margin-left": "10px", "margin-right": "900px"}),
			html.H6(
				html.I([
					"""
					The datasets are cleaned and modified for plotting. To read or download 
					the original datasets, please click on 
					""", 
					html.B("Conclusion"), 
					""", scroll to the bottom of the page, and click on any links under Data 
					Sources. Sorry for the inconvenience.
					"""
				]),
			style={"text-align": "justify", "margin-left": "10px", "margin-right": "10px"})
		])
	], style={"background-color": "#97D4DE", "border": "5px solid white", "border-radius": "20px"})
])
# End of Tab3

"""
Tab4 
Conclusion of project
Citations links
Source code links
"""
tab4 = html.Div([
	# Conclusion summary
	# 7393A1

	# Link to GitHub Source Code Page
	html.H6(html.A("GitHub Source Code", href="https://github.com/XiaoLinGuan/potentialflooding", target="_blank"),
		style={"margin-left": "5px"}),

	# Contact Information
	html.Div([
		html.H6(html.B("Get in touch"), style={"color": "black"}),
		html.H6("Feel free to reach out for any improvements that I can work on for this project."),
		html.Address([
			"📧",
			html.A("xiaolinggguan@gmail.com", href="mailto:xiaolinggguan@gmail.com", target="_blank"),
			html.Br(),
			"📧", 
			html.A("xiaolin.guan72@myhunter.cuny.edu", href="mailto:xiaolin.guan72@myhunter.cuny.edu", target="_blank")
		]),
	], style={"margin-left": "5px", "margin-right": "100px"})
])
# End of Tab4

# All the tabs
tabs = html.Div([
	dcc.Tabs([ 
			dcc.Tab(tab1, label="Introduction", value="tab_1", style=tab_style, selected_style=selected_tab_style),			
			dcc.Tab(tab2, label="Line Graph and Scatter Plot", value="tab_2", style=tab_style, selected_style=selected_tab_style),
			dcc.Tab(tab3, label="Bar Chart and Bubble Chart", value="tab_3", style=tab_style,  selected_style=selected_tab_style),
			dcc.Tab(tab4, label="Conclusion", value="tab_4", style=tab_style, selected_style=selected_tab_style)
		],
		value="tab_1", # Default tab is Overview 
		id="tabs"
	)
], style={"margin-left": "10px", "margin-right": "10px"})

"""
Line Graph functions
Including: 
	build line graph, 
	show or hide line graph dataset,
	options to download the dataset
"""
# Build the line graph.
@app.callback(
	Output(component_id="line_graph", component_property="figure"),
	[Input(component_id="line_graph_radioitems_region", component_property="value"),
	Input(component_id="line_graph_radioitems_measurement", component_property="value")])

def build_line_graph(region, measurement):
	if region == "global_sl":
		if measurement == "measure_inch":
			y = "Inch"
		elif measurement == "measure_cm":
			y = "Centimeter"
		data = datasets.global_sea_level
		title = "Relative Sea Level Rise on Global Scale"
	elif region == "east_coast_sl":
		if measurement == "measure_inch":
			y = "Inch"
		elif measurement == "measure_cm":
			y = "Centimeter"
		data = datasets.east_coast_sea_level
		title = "Relative Sea Level Rise in East Coast"
	elif region == "nyc_sl":
		if measurement == "measure_inch":
			y = "Inch"
		elif measurement == "measure_cm":
			y = "Centimeter"
		data = datasets.nyc_sea_level
		title = "Relative Sea Level Rise in NYC Region"
	elif region == "all_sl":
		if measurement == "measure_inch":
			y = "Inch"
		elif measurement == "measure_cm":
			y = "Centimeter"
		data = datasets.all_three_regions_sea_level
		title = "Relative Sea Level Rise in All Three Regions"
	fig = px.line(
		data, 
		x = "Year",
		y = y,
		color = "Region",
		color_discrete_sequence = ["#11694E", "#1F3FAB", "#EC3445"],
		symbol = "Region",
		title = title
	)
	fig.update_layout(paper_bgcolor = "#CDDEEE", plot_bgcolor = "#AECCE4", title_font=dict(size=20))
	return fig

# Show or hide datasets for the line graph.
@app.callback(
	[Output(component_id="line_graph_filter_example", component_property="children"),
	Output(component_id="line_graph_dataset", component_property="children")],
	[Input(component_id="line_graph_show_dataset", component_property="value"),
	Input(component_id="line_graph_radioitems_region", component_property="value")])

def show_or_hide_lg_dataset(option_show_or_hide, region):
	if option_show_or_hide == "l_g_show_dataset":
		if region == "global_sl":
			data = datasets.global_sea_level
		elif region == "east_coast_sl":
			data = datasets.east_coast_sea_level
		elif region == "nyc_sl":
			data = datasets.nyc_sea_level
		elif region == "all_sl":
			data = datasets.all_three_regions_sea_level
		filter_example = html.Div([
			html.H6(html.U("The dataset will change depending on the region we choose at the top of the graph.")),
			html.H6(
				html.Li([
					html.U(["For example, if we choose ", html.Code("NYC"), """ at the top of the graph,
					then the dataset """, html.B("will not"), """ show any regions other than NYC. In this case, if 
					we apply a filter such as """, html.Code("Global"), " to the dataset, it ", html.B("will not"),
					" work."])])),
			html.Table([
				html.Tr(html.H6(html.B("Examples on how to apply filters on the dataset:"))),
				html.Tr([
					html.Td([			
						html.H6("Apply filter on numbers:"),
						html.H6(html.Li(["Example 1: Enter ", html.Code("=2010")])),
						html.H6(html.Li(["Example 2: Enter ", html.Code(">=2060")])),
						html.Li(html.H6(["Example 3: Enter ", html.Code("<43.26")]))
					]),
					html.Td([
						html.H6("Apply filter on strings:"),
						html.H6(html.Li(["Example 1: Enter ", html.Code("Global")])),
						html.H6(html.Li(["Example 2: Enter ", html.Code("=NYC")])),
						html.H6(html.Li(["Example 3: Enter ", html.Code("contains East Coast")]))
					])
				])
			]),
			html.H6([
				html.B("1st Column: "),
				html.B("Year", style={"color": "#4C6472"}),
				" - the year in which the relative sea-level rise is predicted."
			]),	
			html.H6([
				html.B("2nd Column: "),
				html.B("Centimeter", style={"color": "#4C6472"}),
				" - the predictive sea-level rise in centimeters."
			]),
			html.H6([
				html.B("3rd Column: "),
				html.B("Inch", style={"color": "#4C6472"}),
				" - the predicted sea-level rise in inches."
			]),
			html.H6([
				html.B("4th Column: "),
				html.B("Region", style={"color": "#4C6472"}),
				" - the specific region for the predicted result."
			])
		], style={"color": "#174978", "margin-left": "10px", "margin-right": "10px"})
		dataset = dash_table.DataTable(
			data=data.to_dict("records"),
			filter_action="native",
			columns=[{"name": i, "id": i} for i in (data.columns)],
			page_size=10,
			style_header={"background-color": "#AEB7C8", "border": "1px solid #174978", "font-size": "14px"},
			style_cell={"background-color": "#E4ECF7", "border": "1px solid #174978", "font-size": "14px"}
		)
		return filter_example, dataset
	else: 
		message1 = html.H6("Dataset is hidden.", style={"margin-left": "10px"})
		message2 = html.H6(["To view the dataset, please click on ", html.U("Show Dataset.")], style={"margin-left": "10px"})
		return message1, message2

# Download datasets that are used in line graph.
@app.callback(
	Output(component_id="line_graph_download_data", component_property="data"),
	Input(component_id="line_graph_download_option", component_property="value"))

def download_line_graph_dataset(line_graph_download_option):
	if line_graph_download_option == "global_sea_level_rise":
		return dcc.send_data_frame((datasets.global_sea_level).to_csv, "global_sea_level_rise.csv")
	elif line_graph_download_option == "east_coast_sea_level_rise":
		return dcc.send_data_frame((datasets.east_coast_sea_level).to_csv, "east_coast_sea_level_rise.csv")
	elif line_graph_download_option == "nyc_sea_level_rise":
		return dcc.send_data_frame((datasets.nyc_sea_level).to_csv, "nyc_sea_level_rise.csv")
	elif line_graph_download_option == "all_three_regions_sea_level_rise":
		return dcc.send_data_frame((datasets.all_three_regions_sea_level).to_csv, "all_three_regions_sea_level_rise.csv")
"""End of Line Graph functions"""

"""
Scatter Plot functions
Including: 
	build scatter plot,
	match the color of the legend with the color of the legend description,
	show or hide scatter plot dataset,
	options to download the dataset		
"""
# Build the scatter plot.
@app.callback(
	Output(component_id="scatter_plot", component_property="figure"),
	Input(component_id="scatter_plot_radioitems", component_property="value"))

def build_scatter_plot(value):
	if value == "ao_c":
		title = "The number of cyclones formed on the Atlantic Ocean"
		data = datasets.atlantic_ocean_cyclones_count
	elif value == "ec_c":
		title = "The number of cyclones made landfall on the East Coast"
		data = datasets.east_coast_landfall_count
	elif value == "tri_state_c":
		title = "The number of cyclones made landfall or affected Tri-State Area and NYC"
		data = datasets.tri_state_region_and_nyc_count
	fig = px.scatter(
		data,
		x = "Year",
		y = "Count",
		color = "Category",
		symbol = "Category", 
		size = "Count",
		trendline = "ols",
		trendline_scope = "overall",
		trendline_color_override = "#6C3483",
		title = title
	)
	fig.update_layout(paper_bgcolor="#DDF2D1", plot_bgcolor="#BEE3BA", title_font=dict(size=20))
	return fig

# Match the color of the legend description to the legend of the scatter plot.
@app.callback(
	[Output(component_id="hu", component_property="style"),
	Output(component_id="ts", component_property="style"),
	Output(component_id="td", component_property="style")],
	Input(component_id="scatter_plot_radioitems", component_property="value"))

def match_legend_color(value):
	if ((value == "ao_c") | (value == "ec_c")):
		return (
			{"color": "#9398f5", "background-color": "#DDF2D1",
			"border-top": "2px solid white", "border-bottom": "2px solid white", 
			"border-left": "2px solid white", "border-right": "1px solid white"}, 
			{"color": "#e8907e", "background-color": "#DDF2D1",
			"border-top": "2px solid white", "border-bottom": "2px solid white", 
			"border-left": "1px solid white", "border-right": "1px solid white"},
			{"color": "#4db299", "background-color": "#DDF2D1", 
			"border-top": "2px solid white", "border-bottom": "2px solid white",
			"border-left": "1px solid white", "border-right": "2px solid white"})
	elif value == "tri_state_c":
		return (
			{"color": "#e8907e", "background-color": "#DDF2D1",
			"border-top": "2px solid white", "border-bottom": "2px solid white", 
			"border-left": "2px solid white", "border-right": "1px solid white"}, 
			{"color": "#4db299", "background-color": "#DDF2D1",
			"border-top": "2px solid white", "border-bottom": "2px solid white", 
			"border-left": "1px solid white", "border-right": "1px solid white"}, 
			{"color": "#9398f5", "background-color": "#DDF2D1", 
			"border-top": "2px solid white", "border-bottom": "2px solid white", 
			"border-left": "1px solid white", "border-right": "2px solid white",})

# Show or hide scatter plot dataset
@app.callback(
	[Output(component_id="scatter_plot_filter_example", component_property="children"),
	Output(component_id="scatter_plot_dataset", component_property="children")],
	[Input(component_id="scatter_plot_show_dataset", component_property="value"),
	Input(component_id="scatter_plot_radioitems", component_property="value")])

def show_or_hide_sp_dataset(option_show_or_hide, region):
	if option_show_or_hide == "s_c_show_dataset":
		if region == "ao_c":
			data = datasets.atlantic_ocean_cyclones_count
		elif region == "ec_c":
			data = datasets.east_coast_landfall_count
		elif region == "tri_state_c":
			data = datasets.tri_state_region_and_nyc_count
		filter_example = html.Div([
			html.H6(html.U("The dataset will change depending on the region the user chooses at the top of the plot.")),
			html.Table([
				html.Tr(html.H6(html.B("Examples on how to apply filters on the dataset:"))),
				html.Tr([
					html.Td([			
						html.H6("Apply filter on numbers:"),
						html.H6(html.Li(["Example 1: Enter ", html.Code("=2010")])),
						html.H6(html.Li(["Example 2: Enter ", html.Code(">=2060")])),
						html.H6(html.Li(["Example 3: Enter ", html.Code("<43.26")]))
					]),
					html.Td([
						html.H6("Apply filter on strings:"),
						html.H6(html.Li(["Example 1: Enter ", html.Code("TD")])),
						html.H6(html.Li(["Example 2: Enter ", html.Code("=HU")])),
						html.H6(html.Li(["Example 3: Enter ", html.Code("contains TS")]))
					])
				])
			]),
			html.H6([
				html.B("1st Column: "),
				html.B("Year", style={"color": "#696969"}),
				" - the year in which the number of tropical cyclones are recorded."
			]),	
			html.H6([
				html.B("2nd Column: "),
				html.B("Category", style={"color": "#696969"}),
				" - classify each cyclone according to their maximum sustained surface winds(intensity).",
				html.P(
					html.I([
						"In this dataset, ",
						html.Abbr("HU", title="Hurricane"), " is the highest rank in the category, ",
						html.Abbr("TS", title="Tropical Storm"), " is the second one, and ",
						html.Abbr("TD", title="Tropical Depression"), " is the last one."
					]),
				style={"text-indent": "50px"})
			]),
			html.H6([
				html.B("3rd Column: "),
				html.B("Count", style={"color": "#696969"}),
				" - the number of cyclones for each year."
			])
		], style={"color": "#405A45", "margin-left": "10px"})
		dataset = dash_table.DataTable(
			data=data.to_dict("records"),
			filter_action="native",
			columns=[{"name": i, "id": i} for i in (data.columns)],
			page_size=10,
			style_header={"background-color": "#A9BA9D", "border": "1px solid #405A45", "font-size": "14px"},
			style_cell={"background-color": "#E9EFEA", "border": "1px solid #405A45", "font-size": "14px"}
		)
		return filter_example, dataset
	else:
		message1 = html.H6("Dataset is hidden", style={"margin-left": "10px"})
		message2 = html.H6(["To view the dataset, please click on ", html.U("Show Dataset.")], style={"margin-left": "10px"})
		return message1, message2

# Download datasets that are used in scatter plot.
@app.callback(
	Output(component_id="scatter_plot_download_data", component_property="data"),
	Input(component_id="scatter_plot_download_option", component_property="value"))	

def download_scatter_plot_dataset(scatter_plot_download_option):
	if scatter_plot_download_option == "atlantic_ocean_dataset":
		return dcc.send_data_frame((datasets.atlantic_ocean_cyclones_count).to_csv, "atlantic_ocean_cyclones_count.csv")
	elif scatter_plot_download_option == "east_coast_landfall_dataset":
		return dcc.send_data_frame((datasets.east_coast_landfall_count).to_csv, "east_coast_landfall_count.csv")
	elif scatter_plot_download_option == "tri_state_and_nyc_dataset":
		return dcc.send_data_frame((datasets.tri_state_region_and_nyc_count).to_csv, "tri_state_and_nyc_landfall_count.csv")	
"""End of Scatter Plot functions"""

"""
Bar Chart functions
Including:
	option to modify regular bar chart into a stacked bar chart,
	build bar chart,
	show legend descriptions,
	show or hide bar chart dataset,
	options to download the dataset
"""
# Modify the stacked bar chart option.
@app.callback(
	Output(component_id="stacked_bar_chart_option", component_property="style"),
	[Input(component_id="bar_chart_variable", component_property="value"),
	Input(component_id="bar_chart_radioitems_region", component_property="value")])

def modify_stacked_bar_chart_option(bar_variable, region_option):
	if bar_variable == "elevation_status": 
		if region_option != "nyc_bar":
			return {"display": "none"}
	elif bar_variable == "population":
		return {"display": "none"}

# Build Bar Chart.
@app.callback(
	Output(component_id="bar_chart", component_property="figure"),
	[Input(component_id="bar_chart_variable", component_property="value"),
	Input(component_id="bar_chart_radioitems_region", component_property="value"),
	Input(component_id="bar_chart_radioitems_stack", component_property="value")])

def build_bar_chart(bar_variable, region, value):
	if bar_variable == "elevation_status":
		if region == "nyc_bar":
			if value == "stacked_bar_chart":
				data = datasets.nyc_elevation_status2
				fig = px.bar(
					data,
					x = "Region",
					y = ["Extremely Low", "Low", "Very Low", "Average"],
					color_discrete_sequence = ["#FC6659", "#F7A543", "#E1C739", "#A0BF5F"],
					title = "NYC Elevation Status"
				)
				fig.update_layout(paper_bgcolor = "#C1E3C4", plot_bgcolor = "#9BCC9F", title_font=dict(size=20),
					legend=dict(title="Elevation Status")
				)
				fig.update_yaxes(title_text="Count")
				return fig
			elif value == "regular_bar_chart":
				data = datasets.nyc_elevation_status1
				title = "NYC Elevation Status"
		elif region == "bk_bar":
			data = datasets.bk_elevation_status
			title = "Brooklyn Elevation Status"
		elif region == "mh_bar":
			data = datasets.mh_elevation_status
			title = "Manhattan Elevation Status"
		elif region == "q_bar":
			data = datasets.q_elevation_status
			title = "Queens Elevation Status"
		elif region == "bx_bar":
			data = datasets.bx_elevation_status
			title = "Bronx Elevation Status"
		elif region == "si_bar":
			data = datasets.si_elevation_status
			title = "Staten Island Elevation Status"
		fig = px.bar(
			data,
			x = "Elevation Status",
			y = "Count",
			color = "Elevation Status",
			color_discrete_sequence = ["#FC6659", "#F7A543", "#E1C739", "#A0BF5F"],
			title = title
		)
		fig.update_layout(paper_bgcolor = "#C1E3C4", plot_bgcolor = "#9BCC9F", title_font=dict(size=20))
		return fig		
	else:
		if region == "nyc_bar":
			data = datasets.nyc_population
			fig = px.bar(
				data,
				x = "Region",
				y = ["Coastal Neighborhood", "Non-Coastal Neighborhood"],
				color_discrete_sequence = ["#6495ED", "#A0BF5F"],
				title = "Coastal Neighborhood Population vs. Non-Coastal Neighborhood Population in NYC"
			)
			fig.update_layout(paper_bgcolor = "#C1E3C4", plot_bgcolor = "#9BCC9F", title_font=dict(size=20),
				legend=dict(title="Neighborhood Type")
			)
			fig.update_yaxes(title_text="Population")
			return fig
		elif region == "bk_bar":
			data = datasets.bk_population
			title = "Coastal Neighborhood Population vs. Non-Coastal Neighborhood Population in Brooklyn"
		elif region == "bx_bar":
			data = datasets.bx_population
			title = "Coastal Neighborhood Population vs. Non-Coastal Neighborhood Population in Bronx"
		elif region == "mh_bar":
			data = datasets.mn_population
			title = "Coastal Neighborhood Population vs. Non-Coastal Neighborhood Population in Manhattan"			
		elif region == "q_bar":
			data = datasets.qn_population
			title = "Coastal Neighborhood Population vs. Non-Coastal Neighborhood Population in Queens"			
		elif region == "si_bar":
			data = datasets.si_population
			title = "Coastal Neighborhood Population vs. Non-Coastal Neighborhood Population in Staten Island"
		fig = px.bar(
			data,
			x = "Neighborhood Type",
			y = "Population",
			color = "Neighborhood Type",
			color_discrete_sequence = ["#6495ED", "#A0BF5F"],
			title = title
		)
		fig.update_layout(paper_bgcolor = "#C1E3C4", plot_bgcolor = "#9BCC9F", title_font=dict(size=20))
		return fig

# Show legend descriptions.
@app.callback(
	[Output(component_id="elevation_classificaton", component_property="style"),
	Output(component_id="population_classification", component_property="style")],
	Input(component_id="bar_chart_variable", component_property="value"))

def show_legend_descriptions(variable):
	if variable == "elevation_status":
		return {"color": "#3E7A16", "margin-left": "10px"}, {"display": "none"}
	elif variable == "population":
		return {"display": "none"}, {"color": "#3E7A16", "margin-left": "10px"}

# Show or hide datasets for the bar chart.
@app.callback(
	[Output(component_id="bar_chart_filter_example", component_property="children"),
	Output(component_id="bar_chart_dataset", component_property="children")],
	[Input(component_id="bar_chart_show_dataset", component_property="value"),
	Input(component_id="bar_chart_variable", component_property="value"),
	Input(component_id="bar_chart_radioitems_region", component_property="value"),
	Input(component_id="bar_chart_radioitems_stack", component_property="value")])

def show_or_hide_bc_dataset(option_show_or_hide, variable, region, chart):
	if option_show_or_hide == "b_c_show_dataset":

		# Filter examples.
		optional_filter = html.Div([
			html.H6(html.U("""The dataset will change depending on 
					the variable and the region the user chooses at the top of the chart.""")),
			html.Table([
				html.Tr(html.H6(html.B("Examples on how to apply filter on the dataset:"))),
				html.Tr([
					html.Td([			
						html.H6("Apply filter on numbers:"),
						html.H6(html.Li(["Example 1: Enter ", html.Code("=1230000")])),
						html.H6(html.Li(["Example 2: Enter ", html.Code(">=95709")])),
						html.H6(html.Li(["Example 3: Enter ", html.Code("<500000")]))
					]),
					html.Td([
						html.H6("Apply filter on strings:"),
						html.H6(html.Li(["Example 1: Enter ", html.Code("Brooklyn")])),
						html.H6(html.Li(["Example 2: Enter ", html.Code("=Bronx")])),
						html.H6(html.Li(["Example 3: Enter ", html.Code("contains Queens")]))
					])
				])
			])
		])

		if variable == "elevation_status":	# Elevation Status
			if region == "nyc_bar":
				if chart == "stacked_bar_chart":
					data = datasets.nyc_elevation_status2
					columns = html.Div([
						html.H6([
							html.B("1st Column: "),
							html.B("Region", style={"color": "#4C6472"}), 
							" - the five boroughs of NYC."
						]),
						html.H6([
							html.B("2nd Column: "),
							html.B("Extremely Low", style={"color": "#4C6472"}),
							""" - the number of elevation points that are 
							classified into 'Extremely Low' category."""
						]),
						html.H6([
							html.B("3rd Column: "),
							html.B("Low", style={"color": "#4C6472"}),
							""" - the number of elevation points that are 
							classified into 'Low' category."""
						]),
						html.H6([
							html.B("3rd Column: "),
							html.B("Very Low", style={"color": "#4C6472"}),
							""" - the number of elevation points that are 
							classified into 'Very Low' category."""
						]),
						html.H6([
							html.B("5th Column: "),
							html.B("Average", style={"color": "#4C6472"}),
							""" - the number of elevation points that are 
							classified into 'Average' category."""
						])					
					])
				elif chart == "regular_bar_chart":
					data = datasets.nyc_elevation_status1
					columns = html.Div([
						html.H6([
							html.B("1st Column: "),
							html.B("Elevation Status", style={"color": "#4C6472"}),
							""" - the category that allows a geographical point 
							from NYC being classfied based on their elevations."""
						]),
						html.H6([
							html.B("2nd Column: "),
							html.B("Count", style={"color": "#4C6472"}),
							""" - the number of elevation points belong to a 
							specific elevation status."""
						])
					])
			else:
				columns = html.Div([
					html.H6([
						html.B("1st Column: "),
						html.B("Elevation Status", style={"color": "#4C6472"}),
						""" - the category that allows a geographical point 
						from NYC being classfied based on their elevations."""
					]),
					html.H6([
						html.B("2nd Column: "),
						html.B("Count", style={"color": "#4C6472"}),
						" - the number of elevation points belong to a specific elevation status."
					])
				])
				if region == "bk_bar":
					data = datasets.bk_elevation_status
				elif region == "bx_bar":
					data = datasets.bx_elevation_status
				elif region == "mh_bar":
					data = datasets.mh_elevation_status
				elif region == "q_bar":
					data = datasets.q_elevation_status
				elif region == "si_bar":
					data = datasets.si_elevation_status
			filter_example = html.Div([
				optional_filter,
				columns
			], style={"color": "#056A54","margin-left": "10px", "margin-right": "10px"})
		elif variable == "population":	# Population
			if region == "nyc_bar":
				data = datasets.nyc_population
				columns = html.Div([
					html.H6([
						html.B("1st Column: "),
						html.B("Region", style={"color": "#4C6472"}),
						" - the five boroughs of NYC."
					]),
					html.H6([
						html.B("2nd Column: "),
						html.B("Coastal Neightborhood", style={"color": "#4C6472"}),
						" - the neighborhoods that are bordering NYC's shoreline and the total population."
					]),
					html.H6([
						html.B("3rd Column: "),
						html.B("Non-Coastal Neighborhood", style={"color": "#4C6472"}),
						" - the neighborhoods that are not bordering NYC's shoreline and the total population."
					])
				])
			else:
				columns = html.Div([
					html.H6([
						html.B("1st Column: "),
						html.B("Neighborhood Type", style={"color": "#4C6472"}),
						" - the neighborhoods are classified into two types, either coastal or non-coastal."
					]),
					html.H6([
						html.B("2nd Column: "),
						html.B("Population", style={"color": "#4C6472"}),
						" - the population of the specific type of neighborhood in a borough."
					])		
				])
				if region == "bk_bar":
					data = datasets.bk_population	
					column1 = "Neighborhood Type"
					definition1 = ""
				elif region == "bx_bar":
					data = datasets.bx_population
					column1 = "Neighborhood Type"
				elif region == "mh_bar":
					data = datasets.mn_population
					column1 = "Neighborhood Type"
				elif region == "q_bar":
					data = datasets.qn_population
					column1 = "Neighborhood Type"
				elif region == "si_bar":
					data = datasets.si_population
					column1 = "Neighborhood Type"
			filter_example = html.Div([
				optional_filter,
				columns
			], style={"color": "#056A54","margin-left": "10px", "margin-right": "10px"})
		dataset = dash_table.DataTable(
			data=data.to_dict("records"),
			filter_action="native",
			columns=[{"name": i, "id": i} for i in (data.columns)],
			page_size=6,
			style_header={"background-color": "#76AD87", "border": "1px solid #405A45", "font-size": "14px"},
			style_cell={"background-color": "#ADC4B0", "border": "1px solid #405A45", "font-size": "14px"}
		)
		return filter_example, dataset
	else:
		message1 = html.H6("Dataset is hidden.", style={"margin-left": "10px"})
		message2 = html.H6(["To view the dataset, please click on ", html.U("Show Dataset.")], style={"margin-left": "10px"})
		return message1, message2

# Download datasets that are used in bar chart.
@app.callback(
	Output(component_id="bar_chart_download_data", component_property="data"),
	Input(component_id="bar_chart_download_option", component_property="value"))

def download_bar_chart_dataset(bar_chart_download_option):
	if bar_chart_download_option == "nyc_esc1":
		return dcc.send_data_frame((datasets.nyc_elevation_status1).to_csv, "nyc_elevation_status.csv")
	elif bar_chart_download_option == "nyc_esc2":
		return dcc.send_data_frame((datasets.nyc_elevation_status2).to_csv, "nyc_elevation_status_stacked_bar_chart.csv")
	elif bar_chart_download_option == "bk_esc":
		return dcc.send_data_frame((datasets.bk_elevation_status).to_csv, "brooklyn_elevation_status_count.csv")
	elif bar_chart_download_option == "bx_esc":
		return dcc.send_data_frame((datasets.bx_elevation_status).to_csv, "bronx_elevation_status.csv")
	elif bar_chart_download_option == "mh_esc":
		return dcc.send_data_frame((datasets.mh_elevation_status).to_csv, "manhattan_elevation_status.csv")
	elif bar_chart_download_option == "q_esc":
		return dcc.send_data_frame((datasets.q_elevation_status).to_csv, "queens_elevation_status.csv")
	elif bar_chart_download_option == "si_esc":
		return dcc.send_data_frame((datasets.si_elevation_status).to_csv, "staten_island_elevation_status.csv")
	elif bar_chart_download_option == "nyc_p":
		return dcc.send_data_frame((datasets.nyc_population).to_csv, "nyc_coastal_vs_non_coastal.csv")
	elif bar_chart_download_option == "bk_p":
		return dcc.send_data_frame((datasets.bk_population).to_csv, "brooklyn_coastal_vs_non_coastal.csv")
	elif bar_chart_download_option == "bx_p":
		return dcc.send_data_frame((datasets.bx_population).to_csv, "bronx_coastal_vs_non_coastal.csv")
	elif bar_chart_download_option == "mn_p":
		return dcc.send_data_frame((datasets.mn_population).to_csv, "manhattan_coastal_vs_non_coastal.csv")
	elif bar_chart_download_option == "qn_p":
		return dcc.send_data_frame((datasets.qn_population).to_csv, "queens_coastal_vs_non_coastal.csv")
	elif bar_chart_download_option == "si_p":
		return dcc.send_data_frame((datasets.si_population).to_csv, "si_population_vs_non_coastal.csv")
"""End of Bar Chart functions"""

"""
Bubble Chart functions
Including:
	build bubble chart,
	show or hide bubble chart dataset,
	options to download the dataset
"""
# Build the bubble chart.
@app.callback(
	Output(component_id="bubble_chart", component_property="figure"),
	Input(component_id="bubble_chart_show_dataset", component_property="value"))

def build_bubble_chart(value):
	if ((value == "bub_c_show_dataset") | (value == "bub_c_hide_dataset")):
		data = datasets.possible_flooding_coverage
		fig = px.scatter(
			data,
			x = "Year",
			y = "Approximate Rise Of Sea Level(Inch)",
			size = "Area(mi²)",
			color = "Year",
			title = "Possible Flood Coverage of A 100-Year Flooding"
		)
		fig.update_layout(paper_bgcolor = "#97D4DE", plot_bgcolor = "#74AAB3", title_font=dict(size=20))
	return fig

# Show or hide dataset for bubble chart.
@app.callback(
	[Output(component_id="bubble_chart_filter_example", component_property="children"),
	Output(component_id="bubble_chart_dataset", component_property="children")],
	Input(component_id="bubble_chart_show_dataset", component_property="value"))

def show_or_hide_bub_c_dataset(option_show_or_hide):
	if option_show_or_hide == "bub_c_show_dataset":
		optional_filter = html.Div([
			html.H6(html.U("""The dataset will change depending on 
					the variable and the region the user chooses at the top of the chart.""")),
			html.Table([
				html.Tr(html.H6(html.B("Examples on how to apply filter on the dataset:"))),
				html.Tr([
					html.Td([			
						html.H6("Apply filter on numbers:"),
						html.H6(html.Li(["Example 1: Enter ", html.Code("=2013")])),
						html.H6(html.Li(["Example 2: Enter ", html.Code(">=2050")])),
						html.H6(html.Li(["Example 3: Enter ", html.Code("<2020")]))
					]),
					html.Td([
						html.H6("Apply filter on strings:"),
						html.H6(html.Li(["Example 1: Enter ", html.Code("Brooklyn")])),
						html.H6(html.Li(["Example 2: Enter ", html.Code("=Bronx")])),
						html.H6(html.Li(["Example 3: Enter ", html.Code("contains Queens")]))
					], style={"text-decoration": "line-through"})
				])
			]),

			# Column Description
			html.Div([
				html.H6([
					html.B("1st Column: "),
					html.B("Year", style={"color": "#4C6472"}),
					" - the year where the predicted 100-Year flooding may occur."
				]),
				html.H6([
					html.B("2nd Column: "),
					html.B("Approximate Rise Of Sea Level(Inch)", style={"color": "#4C6472"}),
					" - the predicted approximate rise of sea level measured in inches."
				]),
				html.H6([
					html.B("3rd Column: "),
					html.B("Area(mi²)", style={"color": "#4C6472"}),
					" - the predicted flood coverage of land area measured in square miles."				
				])
			])
		])

		data = datasets.possible_flooding_coverage
		dataset = dash_table.DataTable(
			data=data.to_dict("records"),
			filter_action="native",
			columns=[{"name": i, "id": i} for i in (data.columns)],
			page_size=6,
			style_header={"background-color": "#56A3B0", "border": "1px solid #133C45", "font-size": "14px"},
			style_cell={"background-color": "#A9CAD1", "border": "1px solid #133c45", "font-size": "14px"}
		)		
		return optional_filter, dataset
	else:
		message1 = html.H6("Dataset is hidden.", style={"margin-left": "10px"})
		message2 = html.H6(["To view the dataset, please click on ", html.U("Show Dataset.")], style={"margin-left": "10px"})
		return message1, message2

# Download dataset that is used in bubble chart.
@app.callback(
	Output(component_id="bubble_chart_download_data", component_property="data"),
	Input(component_id="bubble_chart_download_option", component_property="value"))

def download_bubble_chart_dataset(bubble_chart_download_option):
	if bubble_chart_download_option == "flood_data":
		return dcc.send_data_frame((datasets.possible_flooding_coverage).to_csv, "possible_flooding_coverage.csv")
"""End of Bubble Chart functions"""

app.layout = html.Div(
	children = [title, tabs]
)

if __name__ == "__main__":
	app.run_server(debug=True)
