# Package Imports:
import requests
import bs4
import pandas as pd


# Function that scrapes the kijiji website for each housing listing in the Kelowna area
def kijiji_href_get(url):
    '''
    The function that extracts href links for the listings on a single kijiji page

    Parameters
    ----------
    url: str
        The url is the link to the webpage where the html is parsed

    Returns
    -------
    href_list
        A list containing all relevant href links from the webpag
    '''

    # Getting each individual div tag containing links to each real-estate listing page:
    res = requests.get(url)
    soup = bs4.BeautifulSoup(res.text)
    div = soup.findAll('div', {'class': 'search-item regular-ad'})

    # For loop that goes through the ResultSet and extacts the href-links and appends
    # them to a list
    counter = 0
    href_list = []
    for e in div:
        # Searching for imbeded <a> tag, class ='title enable-search-navigation-flag':
        href_link = 'kijiji.ca' + div[counter].findAll('a', {'class':
        'title enable-search-navigation-flag' },href=True)[0]['href']

        # Creating list of href links:
        href_list.append(href_link)
        counter = counter + 1

    return href_list

print(kijiji_href_get('https://www.kijiji.ca/b-for-sale/kelowna/c30353001l1700228'))
