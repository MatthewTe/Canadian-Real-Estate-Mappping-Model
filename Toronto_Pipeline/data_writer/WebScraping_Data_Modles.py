# Importing web scraping packages:
import requests
import bs4
from selenium import webdriver

# Importing data management packages:
import pandas as pd
from datetime import datetime


class Point_2_Homes(object):
    """
    The Point_2_Homes object is the data model that will be used to scrape listings
    data from the Point 2 Homes listings website given the url.

    These methods will be called by the Webscraping object in Web_Scraping.py
    to build the main dataframes
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
            Address = Address.replace('\r', '')
            Address = Address.replace('\n', '')
            Address = Address.rstrip()

            # Type '           xxx' -> xxxx:
            Type = Type.replace(' ', '')
            Type = Type.replace('\n', '')
            Type = Type.replace('\r', '')
            Type = Type.rstrip()

            # Price '$xxx,xxx CAD' -> xxxxxx:
            Price = Price.replace('$', '')
            Price = Price.replace(',', '')
            Price = Price.replace('CAD', '')
            Price = Price.replace(' ', '')
            Price = Price.replace('\n', '')
            Price = Price.rstrip()

            # Beds 'x Beds' -> x:
            Beds = Beds.replace('Beds', '')
            Beds = Beds.replace(' ', '')
            Beds = Beds.replace('\n', ' ')
            Beds = Beds.rstrip()

            # Baths 'x Baths' -> x:
            Baths = Baths.replace('Baths', '')
            Baths = Baths.replace(' ', '')
            Baths = Baths.replace('\n', '')
            Baths = Baths.rstrip()

            # Size x,xxx Sqft -> xxxx:
            Size = Size.replace(',', '')
            Size = Size.replace('Sqft', '')
            Size = Size.replace(' ', '')
            Size = Size.replace('\n', '')
            Size = Size.rstrip()

            # Appending Data to dataframe:
            listings_data = listings_data.append(pd.Series([Address, Price,
             Beds, Baths, Size, Type], index=listings_data.columns), ignore_index=True)

        return listings_data

    def get_date(self, href):
        '''Method navigates to a specific listings page given an imbeded href
            link and from said full listings page extracts and returns the date
            that the listing was posted

            Parameters
            ----------
            href : str
                This is the link to each listings main page that is imbeded within
                every listings post

            Returns
            -------
            date_object : datetime object
                This is the date that the listing was posted, converted from str
                to pandas datetime object
        '''

        # Connecting to webpage:
        # Header to request for Incapsula:
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1)\
        AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

        res = requests.get(href, headers=headers)

        soup = bs4.BeautifulSoup(res.text, 'lxml')

        # Extracting <div class= details-charcs> containing date:
        Div_container = soup.findAll('div', {'class': 'details-charcs'})

        # Iterating over Div_container searching for <dd> that holds date:
        for element in Div_container:

            # Assumes date is 4th listed <dd> tag in Property Summary div:
            date = element.find_all('dd')[3].text

        # Converting date string to datetime object:
        date_object = datetime.strptime(date, '%d %B %Y')

        return date_object

    # TODO: Write get_next_url() method


#Point_2_Homes.get_listings('https://www.point2homes.com/CA/Real-Estate-Listings/ON/Toronto.html')
Point_2_Homes().get_date('https://www.point2homes.com/CA/Condo-For-Sale/ON/Toronto/Entertainment-District/25-Oxley-St/81151344.html')
