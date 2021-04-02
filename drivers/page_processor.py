from drivers.crawler.forecast_crawler import ForecastCrawler
from drivers.storm_watcher import StormPage
from drivers.crawler.history_crawler import HistoryCrawler

from db import config
from db import api as db_api


class PageProcessor():

    def __init__(self, href_link):
        self._href_link = href_link

    def process_page(self, storm_page, crawler):
        crawl = crawler(storm_page.storm_id, storm_page.get_html())
        df = crawl.get_table_df()
        for index, row in df.iterrows():
            db_api.insert_values_forecast(
                row['forecast_epoch'], row['storm_id'],
                row['latitude'], row['longitude'],
                row['intensity'])

    def __call__(self):
        storm_page = StormPage.find(self._href_link)
        self.process_page(storm_page, ForecastCrawler)