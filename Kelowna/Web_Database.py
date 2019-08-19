# Package Imports:
import requests
from bs4 import BeautifulSoup
import pandas as pd


# Function that scrapes the kijiji website for each housing listing in the Kelowna area
def kijiji_href_get(url):
    """ # TODO: Insert docstring documentation PEP-8 """
    # Connecting to kijiji and parsing w/ bs4:
    request = requests.get(url, timeout=5)

    page_1 = BeautifulSoup(requests.content, 'html.parser')
    print(page_1)

kijiji_href_get('https://www.kijiji.ca/b-for-sale/kelowna/c30353001l1700228')
