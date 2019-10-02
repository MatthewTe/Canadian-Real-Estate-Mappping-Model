# Importing system and PATH management packages:
import sys
from os.path import dirname

# Importing web scraping packages:
import requests
import bs4
from selenium import webdriver

# Importing data management packages:
import pandas as pd

# Importing website data models:
from Website_Data_Models import Point_2_Homes

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

        # Initializing the Point_2_Homes data model:
        self.Point_model = Point_2_Homes()

        # Point 2 Homes dataframe:
        # WARNING: Point_2_Homes data model depreciated due to Incapsula protection:
        # sself.Point_2_Homes = self.build_point_2_homes()

    def build_point_2_homes(self):
        '''This method calls on the point_2_homes object to build the pandas
            dataframe containing all of the listings from 'Point 2 Homes.com'

         Returns
         --------
         point_2_homes_data : pandas dataframe
            Dataframe containing all the listings data scraped from 'Point 2 Homes
            .com'

        '''
        # Creating the main dataframe from the inital listings link:
        url = 'https://www.point2homes.com/CA/Real-Estate-Listings/ON/Toronto.html'

        # Initializing page1 listings data into main data:
        main_listings_data = self.Point_model.get_listings(url)
        print(main_listings_data)

        # Creating a list of url's with which to itterate from:
        url_list = []

        loop = True
        while loop == True:
            try:
                # Extracting url for next page:
                url = self.Point_model.get_next_page(url)

                # Appending url to list:
                url_list.append(url)

            except:
                break

        # Itterating over the list of urls, appeding dataframes to them:
        for url in url_list:

            append_data = self.Point_model.get_next_page(url)

            main_listings_data = main_listings_data.append(append_data)

        return main_listings_data

# Test cases:
Toronto_raw_data()
