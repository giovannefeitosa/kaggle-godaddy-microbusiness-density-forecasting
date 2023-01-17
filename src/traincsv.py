import pandas as pd
from urllib.request import urlopen
import json
import plotly.express as px


class TrainCSV:
    def __init__(self, csv_path):
        self.load(csv_path)
        self.prefix_cfips()

    def load(self, csv_path):
        self.df = pd.read_csv(csv_path).astype({'cfips': 'str'})
        with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
            self.countiesgeo = json.load(response)

    def prefix_cfips(self):
        # zerofill cfips to 5 digits
        self.df['cfips'] = self.df['cfips'].apply(lambda x: x.zfill(5))

    def counties_density_map_fig(self, cfip=None):
        # get only cfips and microbusiness_density columns
        newdf = self.df[['cfips', 'microbusiness_density']]
        # group by cfips and get the mean
        newdf = newdf.groupby('cfips') \
            .mean() \
            .reset_index(drop=False) \
            .sort_values(by='microbusiness_density', ascending=False)
        if cfip is None or cfip == '':
            color = 'microbusiness_density'
            color_continuous_scale = 'blugrn'
            color_discrete_map = None
        else:
            newdf['is_current'] = newdf['cfips'] == cfip
            color = 'is_current'
            color_continuous_scale = None
            color_discrete_map = {True: 'blue', False: 'gray'}
        # create figure
        fig = px.choropleth_mapbox(newdf, geojson=self.countiesgeo, locations='cfips', color=color,
                                   # color_continuous_scale="blugrn",
                                   # color_continuous_scale="Viridis",
                                   color_continuous_scale=color_continuous_scale,
                                   color_discrete_map=color_discrete_map,
                                   range_color=(0, 7),
                                   mapbox_style="carto-positron",
                                   zoom=3, center={"lat": 37.0902, "lon": -95.7129},
                                   opacity=0.5,
                                   labels={
                                       'microbusiness_density': 'Microbusiness Density'}
                                   )
        fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
        return fig

    def county_line_fig(self, cfip):
        newdf = self.df[self.df['cfips'] == cfip][[
            'first_day_of_month', 'cfips', 'microbusiness_density']]
        newdf['date'] = pd.to_datetime(newdf['first_day_of_month'])
        maxrange = max(5, newdf['microbusiness_density'].max() + 0.2)
        # create figure
        fig = px.line(newdf, x='date',
                      y='microbusiness_density',
                        title='Microbusiness Density in ' + cfip,
                        range_y=[0, maxrange],
                      )
        fig.update_layout(
            xaxis_title="Date",
            yaxis_title="Microbusiness Density",
            legend_title="Legend Title",
            font=dict(
                family="Courier New, monospace",
                size=18,
                color="#7f7f7f"
            )
        )
        return fig

    def county_line_comparison_fig(self, cfip):
        newdf = self.df[[
            'first_day_of_month', 'cfips', 'microbusiness_density']]
        newdf['date'] = pd.to_datetime(newdf['first_day_of_month'])
        maxrange = min(100, max(5, newdf['microbusiness_density'].max() + 0.2))
        newdf['is_current'] = newdf['cfips'].apply(lambda x: x == cfip)
        # create figure
        fig = px.line(newdf, x='date', y='microbusiness_density',
                      custom_data=['cfips'],
                      title='Microbusiness Density in ' + cfip,
                      range_y=[0, maxrange],
                      color='is_current',
                      color_discrete_map={
                          True: 'blue',
                          False: 'gray'
                      }
                      )
        fig.update_layout(
            xaxis_title="Date",
            yaxis_title="Microbusiness Density",
            legend_title="Legend Title",
            font=dict(
                family="Courier New, monospace",
                size=18,
                color="#7f7f7f"
            )
        )
        return fig

    def counties_dropdown_options(self):
        return self.df['cfips']
