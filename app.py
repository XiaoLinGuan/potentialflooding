import dash
from dash import dcc
from dash import html
from dash import dash_table
from dash.dash_table.Format import Group
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
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

bar_button_styles = {"border": "2px solid #aaf0d1"}

pie_button_styles = {"border": "2px solid #66ddaa"}

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
Overview content
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

	# Link to GitHub Source Code Page
	html.H6(html.A("GitHub Source Code Page", href="https://github.com/XiaoLinGuan/potentialflooding", target="_blank"),
		style={"margin-left": "5px"}),

	# Contact Information
	html.Div([
		html.H6(html.B("Get in touch"), style={"color": ""}),
		html.H6("Feel free to reach out for any improvements that I can work on for this project."),
		html.Address([
			"Gmail address: ", html.A("xiaolinggguan@gmail.com", href="mailto:xiaolinggguan@gmail.com", target="_blank"),
			html.Br(),
			"Email address: ", html.A("xiaolin.guan72@myhunter.cuny.edu", href="mailto:xiaolin.guan72@myhunter.cuny.edu", target="_blank")
		])
	], style={"margin-left": "5px"})
], id="overview_tab_content", style=overview_content_style)

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
					style={"background-color": "#EAF2F8", "border": "1px solid #174978",
						"border-radius": "20px", "color": "#174978"}
				),
				dcc.Download(id="line_graph_download_data")
			],style={"margin-left": "10px", "margin-right": "950px"}),
			html.H6(
				html.I([
					"""
					The datasets are cleaned and modified for plotting. To read or download 
					the original datasets, please click on 
					""", 
					html.B("Overview"), 
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
			With the help of warmer ocean temperatures, tropical cyclones will intensify
			much easier and faster than in the past. With only a few centimeters of the 
			sea-level rise, they will push more water inland, allowing them to affect a 
			more significant part of the coastal regions. As we look at the scatter plot 
			below, we will see the overall trend that more tropical cyclones are developing
			on the Atlantic Ocean and making landfalls on the East Coast. Even though the 
			chart shows most tropical cyclones hit other parts of the East Coast, and that 
			tri-state region does not experience frequent damage from hurricanes. The truth 
			is, given that NYC is a coastal city with an average elevation of thirty-three 
			feet or approximately ten meters, most residents are at risk of experiencing 
			severe flooding from the impact of a tropical cyclone during more unusual 
			hurricane season in the future. 	
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
					style={"background-color": "#EFF8EA", "border": "1px solid #405A45",
						"border-radius": "20px", "color": "#405A45"}
				),
				dcc.Download(id="scatter_plot_download_data")
			],style={"margin-left": "10px", "margin-right": "950px"}),
			html.H6(
				html.I([
					"""
					The datasets are cleaned and modified for plotting. To read or download 
					the original datasets, please click on 
					""", 
					html.B("Overview"), 
					""", scroll to the bottom of the page, and click on any links under Data 
					Sources. Sorry for the inconvenience.
					"""
				]),
			style={"text-align": "justify", "margin-left": "10px", "margin-right": "10px"})
		])
	], style={"background-color": "#DDF2D1", "border": "5px solid white", "border-radius": "20px"})
	# End of Scatter Plot Content
])
# End of Tab2.

"""
Tab3
Choropleth Map content and Bar Chart content
"""
tab3 = html.Div([
	html.H4("will be available by the end of Monday or Tuesday"),
	# Map options
	dcc.Slider(
	min=2010, 
	max=2050, 
	step=None,
	marks={
		2010: "2010",
		2020: "2020",
		2030: "2030",
		2040: "2040",
		2050: "2050"
	},
	value=2020,
	included=False,
	id="slider"),

	# Map 
	dcc.Graph(id="map"),

	html.H4("Stacked Barchart"),

	# Bar chart options
	dbc.Button("2010", id="bar_2010", outline=True, color="info", class_name="me-1", style=bar_button_styles),
	dbc.Button("2020", id="bar_2020", outline=True, color="info", class_name="me-1", style=bar_button_styles),
	dbc.Button("2030", id="bar_2030", outline=True, color="info", class_name="me-1", style=bar_button_styles),
	dbc.Button("2040", id="bar_2040", outline=True, color="info", class_name="me-1", style=bar_button_styles),
	dbc.Button("2050", id="bar_2050", outline=True, color="info", class_name="me-1", style=bar_button_styles),
	dcc.Graph(id="stacked_bar_chart"),
])

# All the tabs
tabs = html.Div([
	dcc.Tabs([ 
			dcc.Tab(tab1, label="Overview", value="tab_1", style=tab_style, selected_style=selected_tab_style),			
			dcc.Tab(tab2, label="Line Graph and Scatter Plot", value="tab_2", style=tab_style, selected_style=selected_tab_style),
			dcc.Tab(tab3, label="Choropleth Map and Bar Chart", value="tab_3", style=tab_style,  selected_style=selected_tab_style)
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
			html.H6(html.U("The dataset will change depending on the region the user chooses at the top of the graph.")),
			html.H6(
				html.Li([
					html.U(["For example, if the user chooses ", html.Code("NYC"), """ at the top of the graph,
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
			])
		], style={"color": "#174978", "margin-left": "10px", "margin-right": "10px"})
		dataset = dash_table.DataTable(
			data=data.to_dict("records"),
			filter_action="native",
			columns=[{"name": i, "id": i,} for i in (data.columns)],
			page_size=10,
			style_header={"background-color": "#AEB7C8", "border": "1px solid #174978", "font-size": "14px"},
			style_cell={"background-color": "#E4ECF7", "border": "1px solid #174978", "font-size": "14px"}
		)
		return filter_example, dataset
	else:
		message1 = html.H6("By default, the dataset is hidden so that user can focus on the graph.", style={"margin-left": "10px"})
		message2 = html.H6(["User can view the dataset by choosing ", html.U("Show Dataset.")], style={"margin-left": "10px"})
		return message1, message2

# Download datasets that are used in line graph.
@app.callback(
	Output(component_id="line_graph_download_data", component_property="data"),
	Input(component_id="line_graph_download_option", component_property="value"))

def download_line_graph_dataset(line_graph_download_option):
	if line_graph_download_option == "global_sea_level_rise":
		return dcc.send_data_frame((datasets.global_sea_level_rise).to_csv, "global_sea_level_rise.csv")
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
		data = atlantic_ocean_cyclones_count
	elif value == "ec_c":
		title = "The number of cyclones made landfall on the East Coast"
		data = east_coast_landfall_count
	elif value == "tri_state_c":
		title = "The number of cyclones made landfall or affected Tri-State Area and NYC"
		data = tri_state_region_and_nyc_count
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
	fig.update_layout(paper_bgcolor="#DDF2D1", plot_bgcolor="#BEE3BA")
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

def shor_or_hide_sp_dataset(option_show_or_hide, region):
	if option_show_or_hide == "s_c_show_dataset":
		if region == "ao_c":
			data = datasets.atlantic_ocean_cyclones_count
		elif region == "ec_c":
			data = datasets.east_coast_landfall_count
		elif region == "tri_state_c":
			data = datasets.tri_state_region_and_nyc_count
		filter_example = html.Div([
			html.H6(html.U("The dataset will change depending on the region the user chooses at the top of the graph.")),
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
				])
		], style={"color": "#405A45", "margin-left": "10px"})
		dataset = dash_table.DataTable(
			data=data.to_dict("records"),
			filter_action="native",
			columns=[{"name": i, "id": i,} for i in (data.columns)],
			page_size=10,
			style_header={"background-color": "#A9BA9D", "border": "1px solid #405A45", "font-size": "14px"},
			style_cell={"background-color": "#E9EFEA", "border": "1px solid #405A45", "font-size": "14px"}
		)
		return filter_example, dataset
	else:
		message1 = html.H6("By default, the dataset is hidden so that user can focus on the graph.", style={"margin-left": "10px"})
		message2 = html.H6(["User can view the dataset by choosing ", html.U("Show Dataset.")], style={"margin-left": "10px"})
		return message1, message2

# Download datasets that are used in scatter plot.
@app.callback(
	Output(component_id="scatter_plot_download_data", component_property="data"),
	Input(component_id="scatter_plot_download_option", component_property="value"))	

def download_line_graph_dataset(scatter_plot_download_option):
	if scatter_plot_download_option == "atlantic_ocean_dataset":
		return dcc.send_data_frame((datasets.atlantic_ocean_cyclones_count).to_csv, "atlantic_ocean_cyclones_count.csv")
	elif scatter_plot_download_option == "east_coast_landfall_dataset":
		return dcc.send_data_frame((datasets.east_coast_landfall_count).to_csv, "east_coast_landfall_count.csv")
	elif scatter_plot_download_option == "tri_state_and_nyc_dataset":
		return dcc.send_data_frame((datasets.tri_state_region_and_nyc_count).to_csv, "tri_state_and_nyc_landfall_count.csv")	
"""End of Scatter Plot functions"""

# Build the Map
@app.callback(
	Output(component_id="map", component_property="figure"),
	[Input(component_id="slider", component_property="value"),])

def build_map(year):
	fig = px.choropleth(
		locations=["NY"],
		locationmode = "USA-states",
		scope = "usa",
		title = "Work In Progress"
	)
	return fig

# Build the Stacked Bar Chart
@app.callback(
	Output(component_id="stacked_bar_chart", component_property="figure"),
	Input(component_id="bar_2010", component_property="value"))

def build_stacked_bar_chart(value):
	fig = px.bar(
		title = "Work In Progress"
	)
	return fig

app.layout = html.Div(
	children = [title, tabs]
)

if __name__ == "__main__":
	app.run_server(debug=True)
