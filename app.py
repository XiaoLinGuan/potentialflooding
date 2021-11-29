import dash
from dash import dcc
from dash import html
from dash import dash_table
from dash.dash_table.Format import Group
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
# import datasets

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
Bottom Right
Line Graph
Global Sea Level current trend and future trend
East-Coast sea current trend and future trend
NYC area current trend and future trend
"""
line_graph = html.Div([

])

"""
Top Right
Map Graph
Prediction of areas affected by flooding
Year Options: 2010, 2020, 2030, 2040, 2050
"""
flooding_map = html.Div([

])

"""
Bottom Left
Pie Chart/Donut Chart
Year Options: 2010, 2020, 2030, 2040, 2050
For each option, shows the percentage of overall affected population separated by boroughs
"""
pie_chart = html.Div([

])

content = dbc.Container([
	dbc.Row([
		dbc.Col([
			dbc.Card([
				dbc.CardBody([
					html.H4("Map")
				])
			])
		],width=6),
		dbc.Col([
			dbc.Card([
				dbc.CardBody([
					html.H4("Stacked Barchart"),
					dbc.Button("2010", outline=True, color="info", class_name="me-1"),
					dbc.Button("2020", outline=True, color="info", class_name="me-1"),
					dbc.Button("2021", outline=True, color="info", class_name="me-1"),
					dbc.Button("2022", outline=True, color="info", class_name="me-1"),
					dbc.Button("2023", outline=True, color="info", class_name="me-1"),
				])
			])
		],width=6)
	]),
	dbc.Row([
		dbc.Col([
			dbc.Card([
				dbc.CardBody([
					html.H4("Line Graph"),
					dbc.Select(
						id = "line_graph_dropdown",
						options=[
							{"label": "Sea Level", "value": "sea_level"},
							{"label": "Hurricane Patterns", "value": "hurricanes"}
						],
						value = "sea_level"
					),
					html.Div([
						dbc.Button("Global", outline=True, color = "info", class_name="me-1"),
						dbc.Button("East Coast", outline=True, color = "info", class_name="me-1"),
						dbc.Button("NYC", outline=True, color = "info", class_name="me-1")
					], id = "sea_level_options"),
				])
			])
		],width=6),
		dbc.Col([
			dbc.Card([
				dbc.CardBody([
					html.H4("Pie Chart/Donut Chart")
				])
			])
		],width=6)
	])
])

@app.callback(Output(component_id="sea_level_options", component_property="style"),
				Input(component_id="line_graph_dropdown", component_property="value"))

def show_or_hide_line_graph_options(line_graph_dropdown):
	if line_graph_dropdown == 'hurricanes':
		return {"display": "none"}
		
app.layout = html.Div(
	children = [title, content]
)

if __name__ == "__main__":
	app.run_server(debug=True)