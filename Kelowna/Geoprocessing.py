# Importing the database connectors:
from Kelowna_Database_management import Kelowna_Database

# Importing data manipulation packages:
import pandas as pd
import geopy
from geopy.geocoders import OpenCage


class Processed_Dataframe():
    '''
    The object that is used to store all the methods that create the processed
    Dataframe that will be directly input into the Machine Learning Algorithm.

    Processed_Dataframe() contains all the methods that modify the raw data read
    from the Kijiji_Database. These methods each add one or several columns
    to the raw dataframe. These columns will all contain data derived from the
    ['Address'] column and subsequent location data.
    '''

    def Add_Geotags(dataframe):
        '''A Method that Geocodes the Address, Latitude and Longitude of a data
            frame read from the Kelowna_Database.

        The Method uses the Geopy Geocode packages to convert the scraped address
        string into a Geocode address as well as lat and long co-ordinates. The
        geocoder api that is being used for test purposes is OpenCage with a
        personal API key and should be changed before full deployment.

        Parameters
        ----------
        dataframe : pandas dataframe
            A dataframe containing Kelowna Real-Estate data from the local database

        Raises
        ------
        SettingWithCopyWarning
            A value is trying to be set on a copy of a slice from a Dataframe

        Returns
        -------
        dataframe
            The dataframe with the Geocode_Address, lat and long co-ordinates
            added to said dataframe.
        '''

        # Adding/Importing API. Will be using the Open Cage API for now:
        geolocator = OpenCage(api_key='64aec27dd2e34dfaa3b5296eed4acc20')

        # Adding the Geoprocessed data as rows to the dataframe:
        dataframe['Geocode_Address'] = dataframe['Address'].apply(lambda x :
         geolocator.geocode(x).address)

        dataframe['Latitude'] = dataframe['Address'].apply(lambda x :
         geolocator.geocode(x).latitude)

        dataframe['Longitude'] = dataframe['Address'].apply(lambda x :
         geolocator.geocode(x).longitude)

        return dataframe

    # Function that calculates and adds the Distance from University Campus:
    def Add_University(dataframe):
        # TODO: Add Docstring
        pass



#test_dataframe = Kelowna_Database().Kijiji_Data_query('SELECT * FROM Kijiji_Data')
#df = test_dataframe[0:10]
#Processed_Dataframe.Add_Geotags(df)
