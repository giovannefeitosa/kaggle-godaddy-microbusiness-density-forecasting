# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, html, dcc, Input, Output, State, exceptions
import dash_daq as daq
import plotly.express as px
import pandas as pd
from traincsv import TrainCSV

external_stylesheets = [
    'https://codepen.io/chriddyp/pen/bWLwgP.css', '/assets/styles.css']
# external_stylesheets = ['https://raw.githubusercontent.com/plotly/dash-app-stylesheets/master/dash-uber-ride-demo.css']
app = Dash(__name__, external_stylesheets=external_stylesheets)
# app = Dash(__name__)

traincsv = TrainCSV('io/dataset/train.csv')

app.layout = html.Div(
    # style={'backgroundColor':colors['background'],'color':colors['text']},
    children=[
        html.H1(children='Train.csv'),

        dcc.Dropdown(traincsv.counties_dropdown_options(),
                     '08003', id='counties-dropdown'),

        html.Div([
            dcc.Graph(
                id='counties-density-map',
                figure=traincsv.counties_density_map_fig(),
            )
        ], style={'width': '49%', 'display': 'inline-block', 'padding': '0 20'}),

        html.Div(
            [
                dcc.Loading(
                    id="loading-1",
                    type="default",
                    children=html.Div(id="county-line-container"),
                ),
            ],
            style={'width': '49%', 'display': 'inline-block', 'padding': '0 20'}
        ),
    ]
)


@app.callback(
    Output('counties-dropdown', 'value'),
    # Output('counties-density-map', 'figure'),
    Input('counties-density-map', 'hoverData'),
)
def update_county_line_loading(hoverData):
    if hoverData is None:
        return '08003'
    cfip = hoverData['points'][0]['location']
    return cfip


@app.callback(
    Output('county-line-container', 'children'),
    Input('counties-dropdown', 'value'),
)
def update_county_line(cfip):
    if cfip is None:
        return []
    # cfip = hoverData['points'][0]['location']
    return dcc.Graph(id='county-line', figure=traincsv.county_line_comparison_fig(cfip),)


if __name__ == '__main__':
    app.run_server(debug=True)
