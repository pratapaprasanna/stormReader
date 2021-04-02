import requests
from urllib import parse


class StormPage():
    base_url = "https://rammb-data.cira.colostate.edu/tc_realtime/storm.asp"

    def __init__(self, storm_id):
        self.storm_id = storm_id

    @property
    def query_params(self):
        return {
            'storm_identifier': self.storm_id,
        }

    def get_html(self):
        response = requests.get(self.base_url, self.query_params, verify=False)
        return response.content

    @classmethod
    def find(cls, href_link):
        params = dict(parse.parse_qsl(parse.urlsplit(href_link.attrs['href']).query))
        return cls(params["storm_identifier"])