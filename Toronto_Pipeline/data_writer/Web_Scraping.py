# Importing system and PATH management packages:
import sys
from os.path import dirname

# Importing web scraping packages:
import requests
import bs4
from selenium import webdriver

# Importing data management packages:
import pandas as pd


class Toronto_raw_data(object):
    """
    This object stores all of the methods and processes that scrapes the various
    Toronto real estate listings sites for the relevant real estate listings
    data.

    Initializing this object runs the methods that perform the web scraping and
    stores all the collected data as instance variables in pandas dataframes

    The websites for which web scrapers will be built are:

    'Point 2 Homes.com' : 'https://www.point2homes.com/CA/
    Real-Estate-Listings/ON/Toronto.html'



    """
    def __init__(self):

        # Point 2 Homes dataframe:
        self.Point_2_Homes = self.build_point_2_homes()

    def build_point_2_homes(self):
        '''This method calls on the point_2_homes object to build the pandas
            dataframe containing all of the listings from 'Point 2 Homes.com'

         Returns
         --------
         point_2_homes_data : pandas dataframe
            Dataframe containing all the listings data scraped from 'Point 2 Homes
            .com'

        '''
        # TODO: Create looping fuction that collects and builds Point 2 Homes data
        # using the .get_listings() and .get_next_url() methods.
