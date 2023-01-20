import json
import os
import numpy as np
import pandas as pd


class USGEO:
    def load(self):
        csv_location = f"{os.environ['PROJECT_ROOT']}/io/customdata/cfips_coordinates.csv"
        self.cfips_coordinates = pd.read_csv(csv_location).sort_values(by=[
            'cfips']).reset_index(drop=True)


usgeo = USGEO()
