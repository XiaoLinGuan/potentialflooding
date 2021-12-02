import dash
from dash import dcc
from dash import html
from dash import dash_table
from dash.dash_table.Format import Group
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import datasets
import statsmodels.api as sm

app = dash.Dash(
	external_stylesheets=[dbc.themes.FLATLY]
)
server = app.server

"""
Title of the dashboard
"""
title = html.Div([
	html.H1(
		["Potential Flooding of NYC as Sea Level rises"],
		style = {
			'height': '50px',
			'font-size': '40px',
			'text-align': 'center',
			'background-image': 'linear-gradient(to bottom, #0f8cf2, #22c3a5)'
		}
	)	
])

"""
Top Left
Stacked Barchart
Prediction of affected population vs non-affected population
Each bar separated by borough
Year Options: 2010, 2020, 2030, 2040, 2050
"""
stacked_barchart = html.Div([

])

"""
Bottom Left
Line Graph
Global Sea Level current trend and future trend
East-Coast sea current trend and future trend
NYC area current trend and future trend
"""
line_graph = html.Div([

])

"""
Top Left
Map Graph
Prediction of areas affected by flooding
Year Options: 2010, 2020, 2030, 2040, 2050
"""
flooding_map = html.Div([

])

"""
Bottom Right
Pie Chart/Donut Chart
Year Options: 2010, 2020, 2030, 2040, 2050
For each option, shows the percentage of overall affected population separated by boroughs
"""
pie_chart = html.Div([

])

bar_button_styles = {"border": "2px solid #aaf0d1"}

line_button_styles = {"border": "2px solid #a0d6b4"}

pie_button_styles = {"border": "2px solid #66ddaa"}

content = dbc.Container([
	dbc.Row([
		dbc.Col([
			dbc.Card([
				dbc.CardBody([
					html.H4("Map"),
					dcc.Slider(
						id = "slider", 
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
						included=False)
				])
			], style = {"border": "2px solid #99e6b3"})
		],width=6),
		dbc.Col([
			dbc.Card([
				dbc.CardBody([
					html.H4("Stacked Barchart"),
					dbc.Button("2010", id="bar_2010", outline=True, color="info", class_name="me-1", style=bar_button_styles),
					dbc.Button("2020", id="bar_2020", outline=True, color="info", class_name="me-1", style=bar_button_styles),
					dbc.Button("2030", id="bar_2030", outline=True, color="info", class_name="me-1", style=bar_button_styles),
					dbc.Button("2040", id="bar_2040", outline=True, color="info", class_name="me-1", style=bar_button_styles),
					dbc.Button("2050", id="bar_2050", outline=True, color="info", class_name="me-1", style=bar_button_styles),
					dcc.Graph(id = "stacked_bar_chart")
				])
			],style = {"border": "2px solid #aaf0d1"})
		],width=6)
	]),
	html.Br(),
	dbc.Row([
		dbc.Col([
			dbc.Card([
				dbc.CardBody([
					html.H4("Line Graph/Scatter Plot"),
					dbc.Select(
						id = "line_graph_dropdown",
						options=[
							{"label": "Sea Level Pattern", "value": "sea_level"},
							{"label": "Cyclone Count", "value": "cyclones"}
						],
						value = "sea_level",
						style=line_button_styles
					),
					html.Br(),
					html.Div([
						dbc.RadioItems(
							options=[
								{"label": "Global", "value": "global_sl"},
								{"label": "East Coast", "value": "east_coast_sl"},
								{"label": "NYC", "value": "nyc_sl"}
							],
							value = "global_sl",
							inline = True,
							id = "line_graph_radioitems_region"
						),
						html.Hr(style={"border-top": "2px dashed #a0d6b4"}),
						dbc.RadioItems(
							options=[
								{"label": "inch", "value": "measure_inch"},
								{"label": "cm", "value": "measure_cm"}
							], 
							value = "measure_inch",
							inline = True,
							id = "line_graph_radioitems_measurement"
						)
					], id = "sea_level_options"),
					html.Div([
						dcc.Graph(id="line_graph")
					], id = "sl_graph"),
					html.Div([
						dbc.RadioItems(
							options=[
								{"label": "Atlantic Ocean", "value": "ao_c"},
								{"label": "East Coast Landfalls", "value": "ec_c"},
								{"label": "Tri-State Landfalls/Affected NYC", "value": "tri_state_c"}
							],
							value = "ao_c",
							inline = True,
							id = "scatter_plot_radioitems"
						),
						html.Br(),
						dbc.ListGroup([
							dbc.ListGroupItem("HU-Hurricane", id="hu"),
							dbc.ListGroupItem("TS-Tropical Storm", id="ts"),
							dbc.ListGroupItem("TD-Tropical Depression", id="td")
						],horizontal=True)
					], id = "cyclone_options"),
					html.Div([
						dcc.Graph(id="scatter_plot")
					], id = "c_plot")
				])
			], style = {"border": "2px solid #a0d6b4"})
		],width=6),
		dbc.Col([
			dbc.Card([
				dbc.CardBody([
					html.H4("Pie Chart/Donut Chart"),
					html.Div(children=[
						dbc.Button("2010", id="pie_2010", outline=True, color="info", class_name="me-1", style=pie_button_styles),
						dbc.Button("2020", id="pie_2020", outline=True, color="info", class_name="me-1", style=pie_button_styles),
						dbc.Button("2030", id="pie_2030", outline=True, color="info", class_name="me-1", style=pie_button_styles),
						dbc.Button("2040", id="pie_2040", outline=True, color="info", class_name="me-1", style=pie_button_styles),
						dbc.Button("2050", id="pie_2050", outline=True, color="info", class_name="me-1", style=pie_button_styles)
					],id = "pie_options"),
					dcc.Graph(id = "pie_chart")
				])
			],style = {"border": "2px solid #66ddaa"})
		],width=6)
	])
])

# Show or hide line graph options
@app.callback(Output(component_id="sea_level_options", component_property="style"),
				Input(component_id="line_graph_dropdown", component_property="value"))

def show_or_hide_line_graph_options(value):
	if value != "sea_level":
		return {"display": "none"}

# Show or hide line graph
@app.callback(Output(component_id="sl_graph", component_property="style"),
				Input(component_id="line_graph_dropdown", component_property="value"))

def show_or_hide_line_graph(value):
	if value != "sea_level":
		return {"display": "none"}

# Building the line graph.
@app.callback(Output(component_id="line_graph", component_property="figure"),
				[Input(component_id="line_graph_radioitems_region", component_property="value"),
				Input(component_id="line_graph_radioitems_measurement", component_property="value")])

def build_line_graph(region, measurement):
	if (region == "global_sl" and measurement == "measure_inch"):
		data = datasets.global_sl
		y = "Inch"
	elif (region == "global_sl" and measurement == "measure_cm"):
		data = datasets.global_sl
		y = "Centimeters"
	fig = px.scatter(
		data, 
		x = "Year",
		y = y,
		trendline = "lowess",
		trendline_options=dict(frac=0.1)
	)
	return fig
	# elif (region == "east_coast_sl" & measurement == "measure_inch"):
	
	# elif (region == "east_coast_sl" & measurement == "measure_cm"):
	
	# elif (region == "nyc_sl" & measurement == "measure_inch"):
	
	# elif (region == "nyc_sl" & measurement == "measure_cm"):


# Show or hide scatter plot options
@app.callback(Output(component_id="cyclone_options", component_property="style"),
				Input(component_id="line_graph_dropdown", component_property="value"))

def show_or_hide_scatter_plot_options(value):
	if value != "cyclones":
		return {"display": "none"}

# Show or hide scatter plot
@app.callback(Output(component_id="c_plot", component_property="style"),
				Input(component_id="line_graph_dropdown", component_property="value"))

def show_or_hide_scatter_plot(value):
	if value != "cyclones":
		return {"display": "none"}

# Matching the color of the legend description to the legend.
@app.callback([Output(component_id="hu", component_property="style"),
				Output(component_id="ts", component_property="style"),
				Output(component_id="td", component_property="style")],
				Input(component_id="scatter_plot_radioitems", component_property="value"))

def match_ts_color(value):
	if value == "ao_c":
		return {"color": "#9398f5"}, {"color": "#8dd9b8"}, {"color": "#e8907e"}
	elif value == "ec_c":
		return {"color": "#9398f5"}, {"color": "#e8907e"}, {"color": "#8dd9b8"}
	elif value == "tri_state_c":
		return {"color": "#e8907e"}, {"color": "#9398f5"}, {"color": "#acacac", 
																			"text-decoration": "line-through",
																			"text-decoration-color": "#000000",
																			"text-decoration-thickness": "2px"}
		
# Building the scatter plot.
@app.callback(Output(component_id="scatter_plot", component_property="figure"),
				Input(component_id="scatter_plot_radioitems", component_property="value"))

def build_scatter_plot(value):
	if value == "ao_c":
		title = "The number of cyclones formed on the Atlantic Ocean"
		data = datasets.cyclones_AO
	elif value == "ec_c":
		title = "The number of cyclones made landfall on the East Coast"
		data = datasets.landfall_EC
	elif value == "tri_state_c":
		title = "Cyclones made landfall or affected Tri-State and NYC"
		data = datasets.tri_state_and_nyc
	fig = px.scatter(
		data,
		x = "Year",
		y = "Count",
		color = "Category",
		symbol = "Category",
		size = "Count",
		title = title
	)
	return fig

# The Webapp.
app.layout = html.Div(
	children = [title, content]
)

if __name__ == "__main__":
	app.run_server(debug=True)
