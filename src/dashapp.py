# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, html, dcc
import dash_daq as daq
import plotly.express as px
import pandas as pd

# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
# app = Dash(__name__, external_stylesheets=external_stylesheets)
app = Dash(__name__)

df = pd.read_csv('io/dataset/train.csv')

# create a dataset that looks like this: cfips, microbusinessDensity
cfips = df['cfips'].unique()


app.layout = html.Div(
    #style={'backgroundColor':colors['background'],'color':colors['text']},
    children=[
        html.H1(children='Train.csv'),

        dcc.Graph(
            id='example-graph',
            figure=fig,
        )
    ]
)

if __name__ == '__main__':
    app.run_server(debug=True)
