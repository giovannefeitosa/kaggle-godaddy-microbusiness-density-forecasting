import json
from urllib.request import urlopen

class USGEO:
  def load(self):
    with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
      self.json = json.load(response)

usgeo = USGEO()
