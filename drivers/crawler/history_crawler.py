import pandas as pd
from bs4 import BeautifulSoup


class HistoryCrawler():
    first_col_name = "Synoptic Time"
    cols_map = {
        "Forecast Hour": "forecast_hour",
        "Latitude": "latitude",
        "Longitude": "longitude",
        "Intensity": "intensity",
    }

    def __init__(self, storm_id, html_content):
        self._storm_id = storm_id
        self._soup = BeautifulSoup(html_content)

    def get_table_df(self):
        tables = self._soup.find_all({"table"})

        for tab in tables:
            df = pd.read_html(str(tab), header=0)[0]
            # Hack for finding the relevant table
            if df.columns[0] == self.first_col_name:
                break
        df['storm_id'] = self._storm_id
        df.rename(columns=self.cols_map, inplace=True)

        return df