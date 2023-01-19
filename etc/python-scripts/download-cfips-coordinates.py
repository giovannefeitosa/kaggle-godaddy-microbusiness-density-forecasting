import json
import os
import sys
import numpy as np
import pandas as pd
from urllib.request import urlopen


def download():
    project_root = os.environ['PROJECT_ROOT']
    with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
        rawjson = json.load(response)
        ds = []
        for feature in rawjson['features']:
            cfips = int(
                f"{feature['properties']['STATE']}{feature['properties']['COUNTY']}")
            rawcoordinates = feature['geometry']['coordinates']
            lat, lon = _getCentroidCoordinates(rawcoordinates)
            ds.append([cfips, lat, lon])
        # save to pandas csv file
        df = pd.DataFrame(ds, columns=['cfips', 'lat', 'lon'])
        df.to_csv(
            f'{project_root}/io/customdata/cfips_coordinates.csv', index=False)


def _getCentroidCoordinates(coordinates):
    centroid = np.mean(
        np.array(_flatten(coordinates)).reshape(-1, 2), axis=0)
    return centroid[1], centroid[0]

# https://stackabuse.com/python-how-to-flatten-list-of-lists/


def _flatten(list_of_lists):
    flat = ()
    for element in list_of_lists:
        if isinstance(element, list):
            flat += _flatten(element)
        else:
            flat += (element,)
    return flat


if __name__ == '__main__':
    download()
