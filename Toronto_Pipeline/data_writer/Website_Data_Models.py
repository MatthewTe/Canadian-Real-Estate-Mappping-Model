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

    def get_listings(self, url):
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
        listings_data = pd.DataFrame(columns=['Date', 'Address', 'Price', 'Beds',
         'Baths', 'Size', 'Type'])

        # Populating dataframe with elements found in list soup:
        for element in list:

            # Href link to listings main page: <a class = button-flat-color
            href = element.findAll('a', {'class': 'button-flat-color'})[0].get('href')
            # Combining href with url to form link to listings page:
            link = ('https://www.point2homes.com' + href)

            # Extracting date from listings main page:
            Date = self.get_date(link)

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
            listings_data = listings_data.append(pd.Series([Date, Address, Price,
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

            # Collecting all <dd> tags in the Propery Summary Div_container:
            dd_tags = element.find_all('dd')

            for element in dd_tags:

                # Itterates through each <dd> string trying to convert to datetime
                # object untill it reaches the date:
                try:
                    # NOTE: Very inefficient, update with regx:
                    date_object = datetime.strptime(element.text, '%d %B %Y')
                except:
                    pass

        return date_object

    def get_next_page(self, url):
        '''The method extracts and parses the html of the Point2Homes page
        dictated by the url link and returns the link to the next listings page.

        Parameters
        ----------
        url : str
            This is the url from which the html data will be parsed and the next
            navigational link will be extracted

        Returns
        -------
        next_url : str
            The link to the next listings page
        '''
        # Connecting to a webpage:
        # Header to request for Incapsula:
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1)\
        AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

        res = requests.get(url, headers=headers)

        soup = bs4.BeautifulSoup(res.text, 'lxml')

        # Extracting the href link from the page: stored in <a class = pager-next>
        # Assumes the enxt page href atribute tag is the second tag of said class:
        next_href = soup.findAll('a', {'class': 'pager-next'})[1].get('href')

        # Building the full url to the next page with the extracted href:
        next_url = ('https://www.point2homes.com' + next_href)

        return next_url


Point_2_Homes().get_listings('https://www.point2homes.com/CA/Real-Estate-Listings/ON/Toronto.html')
