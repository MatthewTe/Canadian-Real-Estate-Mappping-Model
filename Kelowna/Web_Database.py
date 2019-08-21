# Package Imports:
import requests
import bs4
import pandas as pd
import time
import datetime


def page_2_dataframe(url):
    '''The function that returns a dataframe of basic real-estate listings on kijiji

    Parameters
    ----------
    url : str
        The url link of the kijiji listings page to be parsed

    Returns
    --------
    df
        The dataframe containing the Title, price, date_posted, address, details,
        page link, # of bedrooms and # of Bathrooms of every real-estate listing
        on the kijiji page
    '''

    # Getting each individual div tag containing links to each real-estate listing page:
    res = requests.get(url)
    soup = bs4.BeautifulSoup(res.text)
    div = soup.findAll('div', {'class': 'search-item regular-ad'})

    # Creating the empty dataframe:
    df = pd.DataFrame(columns=['Title', 'Price', 'Date', 'Address', 'Details' ,'Link',
    'Bedrooms', 'Bathrooms'])

    # Loop that parses each collected <div> tag for data 2 populate df:
    counter = 0
    for e in div:

        # Searching for imbeded <div> tag, class ='price'7
        price = div[counter].findAll('div', {'class': 'price'})[0].text

        # Searching for imbeded <a> tag, class ='title enable-search-navigation-flag'
        title = div[counter].findAll('a', {'class':
         'title enable-search-navigation-flag'})[0].text

        # Searching for imbeded <span> tag, class = 'date-posted'
        date_stated = div[counter].findAll('span', {'class': 'date-posted'})[0].text
        # If date returned is > 1 day then the date value of current date is used:
        try:
            date = datetime.datetime.strptime(date_stated, '%d/%m/%Y')
        except:
            date = datetime.datetime.today()

        # Searching for imbeded <a> tag, class ='title enable-search-navigation-flag':
        href_link = 'http://kijiji.ca' + div[counter].findAll('a', {'class':
        'title enable-search-navigation-flag'},href=True)[0]['href']

        # Searching for imbeded <div> tag, class = 'description':
        details = div[counter].findAll('div', {'class': 'description'})[0].text

        # Acessing the href link to pull data directly from the listings full page:
        res = requests.get(href_link)
        soup = bs4.BeautifulSoup(res.text)

        # Searching listings page for <span> tag, itemprop = 'address'
        address = soup.findAll('span', {'itemprop': 'address'})[0].text

        # Searching for imbeded <dl> tag, class = 'itemAttribute-983037059'
        house_descriptors = soup.findAll('dl', {'class': 'itemAttribute-983037059'})

        # For loop parsing the descriptor strings:
        for i in house_descriptors:

            # for value bedrooms:
            try:
                if 'Bedrooms' in house_descriptors[0].text:
                    bedrooms = house_descriptors[0].text.replace('Bedrooms','')
                else:
                    bedrooms = 'NaN'
            except:
                bedrooms = 'NaN'

            # for value bathrooms:
            try:
                if 'Bathrooms' in house_descriptors[1].text:
                    bathrooms = house_descriptors[1].text.replace('Bathrooms','')
                else:
                    bathrooms = 'NaN'
            except:
                bathrooms = 'NaN'

            # TODO: Determine the necessity of sqft tag scraping as very few listings
            # contain this information

        # Appending a row onto the dataframe by mapping a series to the df:
        df = df.append(pd.Series([title, price, date, address, details, href_link,
        bedrooms, bathrooms], index=df.columns), ignore_index=True)

        counter = counter + 1

    return df

#test = page_2_dataframe('https://www.kijiji.ca/b-for-sale/kelowna/c30353001l1700228')
