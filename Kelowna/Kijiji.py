# Package Imports:
import requests
import bs4
import pandas as pd
import time
import datetime

class Kijiji:
    '''
    The Object that contains the scraped Real-Estae listings data for Kijiji.com
    '''

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
        soup = bs4.BeautifulSoup(res.text, 'lxml')
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

    def get_next_page(url):
        '''Recieves the url to a kijiji listings page and returns the url for the next
            concecutive kijiji page in the listing category

        Parameters
        ----------
        url : str
            The url link for the first kijiji listings page

        Returns
        --------
        next_page_link : str
            The url for the next kijiji listings page in the category based on the url
            input
        '''

        # connecting to the page:
        res = requests.get(url)
        soup = bs4.BeautifulSoup(res.text)

        # Searching for the <a> tag, title = 'Next' and creating http link:
        next_page_link = 'http://kijiji.ca' + soup.findAll('a', {'title': 'Next'})[0]['href']

        return next_page_link

    def get_data(init_url, num_pages):
        '''Constructs a dataframe containing the the page_2_dataframe() data for
            multiple pages of kijiji real-estae listings

        Parameters
        -----------
        init_url : str
            The url link to the first page of the kijiji listings
        num_pages : int
            The number of subsequent listings pages to be scraped

        Returns
        -------
        df_main : pandas DataFrame
            The dataframe containing the scraped kijiji listings data
        '''

        counter = 0
        # loop that itterates thorugh each listings page:
        while counter < (num_pages+1):

            # for the first listings page:
            if counter == 0:

                df_main = Kijiji.page_2_dataframe(init_url)
                new_page_url = Kijiji.get_next_page(init_url)

                counter = counter + 1

            # For every subsequent listings page up to the penultimate one:
            elif counter < num_pages:

                df_main = df_main.append(Kijiji.page_2_dataframe(new_page_url),
                ignore_index=True)

                # Ending the loop if loop reaches the end of the listings list:
                try:
                    new_page_url = Kijiji.get_next_page(new_page_url)
                    counter = counter + 1
                except:
                    return df_main
                    break

            # for the final listings page and dataframe return:
            else:

                df_main = df_main.append(Kijiji.page_2_dataframe(new_page_url),
                 ignore_index=True)
                print('Download Complete with DataFrame Lenght:' + str(len(df_main)))

                return df_main

#test = Kijiji.get_data('https://www.kijiji.ca/b-for-sale/kelowna/c30353001l1700228',2)
#print(test)
