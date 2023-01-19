import json
import os
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
            if len(rawcoordinates) > 1:
                raise Exception(
                    f"More than one coordinate set found. cfips={cfips} len={len(rawcoordinates)} len2={len(rawcoordinates[0][0])} centroid={_getCentroidCoordinates(rawcoordinates[0][0])}")
            lat, lon = _getCentroidCoordinates(rawcoordinates[0])
            ds.append([cfips, lat, lon])
        # save to pandas csv file
        df = pd.DataFrame(ds, columns=['cfips', 'lat', 'lon'])
        df.to_csv(
            f'{project_root}/io/customdata/cfips_coordinates.csv', index=False)


def _getCentroidCoordinates(coordinates):
    # returns (lat, lon)
    centroid = np.mean(np.array(coordinates), axis=0)
    return centroid[1], centroid[0]


if __name__ == '__main__':
    download()
