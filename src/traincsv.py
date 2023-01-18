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
        self.df['first_day_of_month'] = pd.to_datetime(self.df['first_day_of_month'])
        with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
            self.countiesgeo = json.load(response)
        self.last_cfip = None
        self.df_cfip_map = None
        self.df_cfip_line = None

    def prefix_cfips(self):
        # zerofill cfips to 5 digits
        self.df['cfips'] = self.df['cfips'].apply(lambda x: x.zfill(5))
    
    def load_cfip(self, cfip=None):
        # df_cfip_map
        if cfip != self.last_cfip or self.df_cfip_map is None:
            self.df_cfip_map = self.df[['cfips', 'microbusiness_density']] \
                .groupby('cfips') \
                .mean() \
                .reset_index(drop=False)
        
        # df_cfip_line
        if cfip is None or cfip == '':
            self.last_cfip = None
            self.df_cfip_line = None
        elif cfip != self.last_cfip:
            # self.df_cfip_map = self.df[['cfips', 'microbusiness_density']] \
            #     .groupby('cfips') \
            #     .mean() \
            #     .reset_index(drop=False)
            self.df_cfip_line = self.df[['cfips', 'first_day_of_month', 'microbusiness_density']] \
                [self.df['cfips'] == cfip]
            # self.df_cfip_line['is_current'] = self.df_cfip_line

    def counties_density_map_fig(self, cfip=None):
        self.load_cfip(cfip)
        if self.df_cfip_map is None:
            return px.choropleth_mapbox()
        color = 'microbusiness_density'
        color_continuous_scale = 'blugrn'
        color_discrete_map = None
        # create figure
        fig = px.choropleth_mapbox(self.df_cfip_map, geojson=self.countiesgeo, locations='cfips', color=color,
                                   # color_continuous_scale="blugrn",
                                   # color_continuous_scale="Viridis",
                                   color_continuous_scale=color_continuous_scale,
                                   color_discrete_map=color_discrete_map,
                                   range_color=(0, 7),
                                   mapbox_style="carto-positron",
                                   zoom=3, center={"lat": 37.0902, "lon": -95.7129},
                                   opacity=0.5,
                                   labels={
                                       'microbusiness_density': 'mbd'}
                                   )
        fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
        return fig

    def county_line_fig(self, cfip):
        self.load_cfip(cfip)
        if self.df_cfip_line is None:
            return px.line()
        # newdf = self.df[self.df['cfips'] == cfip][[
        #     'first_day_of_month', 'cfips', 'microbusiness_density']]
        # newdf['date'] = pd.to_datetime(newdf['first_day_of_month'])
        maxrange = max(5, self.df_cfip_line['microbusiness_density'].max() + 0.2)
        # create figure
        fig = px.line(self.df_cfip_line, x='first_day_of_month',
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
        return self.df['cfips'].unique()
