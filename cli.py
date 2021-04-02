import logging

from flask import Flask
from flask_apscheduler import APScheduler

from db import api as db_api
from drivers.crawler import base
from drivers.page_processor import PageProcessor

from urllib import parse
from flask import jsonify


logging.basicConfig(level=logging.DEBUG)


app = Flask(__name__)
scheduler = APScheduler()

def scheduleHourlyTask():
    main( "https://rammb-data.cira.colostate.edu/tc_realtime/index.asp", "storm_identifier", {"class":"basin_storms"})


def scheduleMonthlyTask():
    archival_store("https://rammb-data.cira.colostate.edu/tc_realtime/index.asp", "storm_season", {"id":"sidebar"})


def archival_store(base_link, href_id, div_element):
    base_obj = base.BaseDriver()
    main_soup = base_obj.get_soup_element(base_link)
    div_segs = base_obj.get_div_content(main_soup, div_element)
    for i in div_segs:
        href_links = base_obj.get_href_elements(i, href_id)
        for href_link in href_links:
            archivalyear = dict(parse.parse_qsl(parse.urlsplit(href_link.attrs['href']).query))[href_id]
            tmp_link="/".join(base_link.split('/')[:-1])
            archival_link = f"{tmp_link}/season.asp?storm_season={archivalyear}"
            main(archival_link, "storm_identifier", {"class":"basin_storms_archive"})


def main(base_link, href_id, div_element):
    base_obj = base.BaseDriver()
    main_soup = base_obj.get_soup_element(base_link)
    div_segs = base_obj.get_div_content(main_soup, div_element)
    for i in div_segs:
        href_links = base_obj.get_href_elements(i, href_id)
        for href_link in href_links:
            page_processor = PageProcessor(href_link)
            page_processor()


@app.route("/forecast/<storm_id>", methods=['GET'])
def get_db_vaues(storm_id):
  data = db_api.fetch_data_forecast(storm_id)
  response =  [{'latitude':i.latitude, 'longitude':i.longitude, 'intensity':i.intensity} for i in data]
  return jsonify(response)


if __name__ == "__main__":
    logging.debug("Creating tables")
    db_api.create_tables()
    scheduler.add_job(id = 'Hourly Task', func=scheduleHourlyTask, trigger="interval", minutes=1)
    scheduler.add_job(id = 'Monthly Task', func=scheduleMonthlyTask, trigger="interval", month='*', day='last')
    scheduler.start()
    app.run(host="0.0.0.0")
