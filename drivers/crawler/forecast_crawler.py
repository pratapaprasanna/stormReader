import pandas as pd

from bs4 import BeautifulSoup
from datetime import datetime

from utils import utils

class ForecastCrawler():
    first_col_name = "Forecast Hour"
    cols_map = {
        "Forecast Hour": "forecast_hour",
        "Latitude": "latitude",
        "Longitude": "longitude",
        "Intensity": "intensity",
    }

    def __init__(self, storm_id, html_content):
        self._storm_id = storm_id
        self._soup = BeautifulSoup(html_content, 'lxml')

    def get_table_df(self):
        df = pd.DataFrame()
        tables = self._soup.find_all({"table"})
        for tab in tables:
            temp_df = pd.read_html(str(tab), header=0)[0]
            # Hack for finding the relevant table
            if temp_df.columns[0] == self.first_col_name:
                df = temp_df
                break
        if not df.empty:
            captured_time = ":".join(
                self._soup.find("div", {"class": "text_product_wrapper"}).\
                find("h4").text.split(" ")[-2:])
            captured_time_epoch = utils.get_epoch_time(captured_time)
            df['storm_id'] = self._storm_id
            df['forecast_epoch'] = df['Forecast Hour'].apply(lambda x: x * 60 * 60 * 1000)
            df['forecast_epoch'] = df['forecast_epoch'] + captured_time_epoch
            df['forecast_epoch'] = df['forecast_epoch'].astype(int)
            df.rename(columns=self.cols_map, inplace=True)
        return df
