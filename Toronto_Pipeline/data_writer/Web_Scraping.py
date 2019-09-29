# Importing system and PATH management packages:
import sys
from os.path import dirname

# Importing web scraping packages:
import requests
import bs4
from selenium import webdriver

# Importing data management packages:
import pandas as pd

# PATH management:


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

        # WARNING: Code unstalbe due to websites use of Incapsula protection:


        # Connecting to webpage:
        # Using selenium to bypass Incapsula:

        # Header to request for Incapsula:
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1)\
        AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

        res = requests.get(url, headers=headers)

        soup = bs4.BeautifulSoup(res.text, 'lxml')

        # Seaching for all instances of listings article {class : item-cnt clearfix gold}
        list = soup.find_all('div', {'class': 'item-cnt clearfix gold'})

        # Creating dataframe:
        listings_data = pd.DataFrame(columns=['Address', 'Price', 'Beds',
         'Baths', 'Size', 'Type'])

        # Populating dataframe with elements found in list soup:
        for element in list:
            # Address: <div class = address-container>
            Address = element.findAll('div', {'class': 'address-container'})[0].text

            # Price: <div class = price>
            Price = element.findAll('div', {'class': 'price'})[0].text

            # Beds: <li data-label = Beds >
            try:
                Beds = element.findAll('li', {'data-label': 'Beds'})[0].text
            except:
                Beds = 'NaN'

            # Baths: <li data-label = Baths>
            try:
                Baths = element.findAll('li', {'data-label': 'Baths'})[0].text
            except:
                Baths = 'NaN'

            # Size: <li data-label = Sqft>
            try:
                Size = element.findAll('li', {'data-label': 'Sqft'})[0].text
            except:
                Size = 'NaN'

            # Type: <li class = property-type ic-proptype>
            try:
                Type = element.findAll('li', {'class': 'property-type ic-proptype'})[0].text
            except:
                Type = 'NaN'


            # Performing Raw data transformations and placing data into a pd.series:

            # Address '     xxxx, xxxx, xxxx' -> xxxx, xxxx, xxxx:
            Address = Address.replace('        ', '')
            Address = Address.rstrip()

            # Type '           xxx' -> xxxx:
            Type = Type.replace(' ', '')
            Type = Type.rstrip()

            # Price '$xxx,xxx CAD' -> xxxxxx:
            Price = Price.replace('$', '')
            Price = Price.replace(',', '')
            Price = Price.replace('CAD', '')
            Price = Price.replace(' ', '')
            Price = Price.rstrip()

            # Beds 'x Beds' -> x:
            Beds = Beds.replace('Beds', '')
            Beds = Beds.replace(' ', '')
            Beds = Beds.rstrip()

            # Baths 'x Baths' -> x:
            Baths = Baths.replace('Baths', '')
            Baths = Baths.replace(' ', '')
            Baths = Baths.rstrip()

            # Size x,xxx Sqft -> xxxx:
            Size = Size.replace(',', '')
            Size = Size.replace('Sqft', '')
            Size = Size.replace(' ', '')
            Size = Size.rstrip()

            # Creating Series:
            print(Address, Beds, Baths, Size, Price, Type)




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
