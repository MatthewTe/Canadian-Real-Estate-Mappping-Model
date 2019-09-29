# Importing web scraping packages:
import requests
import bs4
# Importing data management packages:
import pandas as pd


class Point_2_Homes(object):
    """
    The Point_2_Homes object contains all the methods that scrape listings data
    directly from 'https://www.point2homes.com/CA/Real-Estate-Listings/ON/Toronto.html'.

    These methods will be called by the Toronto_raw_data() object to build the main
    dataframe.
    """

    def get_listings(url):
        '''Method generates a pandas dataframe containing all the real estate
        listings data scraped from a given 'Point 2 Home' url using bs4 and
        requests packages

        Parameters
        ----------
        url : str
            String representing the url of the 'Point 2 Homes' webpage

        Returns
        -------
        listings_data : pandas dataframe
            Dataframe containing all real estate listings data from the webpage
        '''

        # Connecting to webpage:
        res = requests.get(url)
        soup = bs4.BeautifulSoup(res.text, 'lxml')

        # Seaching for all instances of listings article {class : item-cnt clearfix gold}
        # TODO: Write parser for res.text to scrape all listings.

        print(soup)


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


# Test Cases:
Point_2_Homes.get_listings('https://www.point2homes.com/CA/Real-Estate-Listings/ON/Toronto.html')
