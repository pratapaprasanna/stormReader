import pandas as pd
import requests
from bs4 import BeautifulSoup

class BaseDriver(object):

    def __init__(self, *args, **kwargs):
        super(BaseDriver, self).__init__(*args, **kwargs)

    def get_soup_element(self, link):
        response = requests.get(link, verify=False)
        soup = BeautifulSoup(response.content, 'lxml')
        return soup

    def get_div_content(self, soup, div_element):
        return soup.find_all("div", div_element)

    def get_href_elements(self, soup, href_id):
        return soup.find_all("a", href=lambda href: href and href_id in href)
