# Importing the database connectors:
from Kelowna_Database_management import Kelowna_Database

# Importing data manipulation packages:
import pandas as pd
import geopy
from geopy.geocoders import OpenCage
from geopy import distance


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
            A dataframe containing Kelowna Real-Estate data from the local
             database.

        Raises
        ------
        SettingWithCopyWarning
            A value is trying to be set on a copy of a slice from a Dataframe.

        Returns
        -------
        dataframe
            The dataframe with the Geocode_Address, lat and long co-ordinates
            added to said dataframe.
        '''

        # Adding/Importing API. Will be using the Open Cage API for now:
        geolocator = OpenCage(api_key='64aec27dd2e34dfaa3b5296eed4acc20')

        # Adding the Geoprocessed data as rows to the dataframe:
        dataframe['Geocode_Address'] = dataframe['Address'].apply(geolocator.geocode)
        dataframe.dropna(inplace=True)

        # Extracting the latitude from the Geocode_Address object:
        dataframe['Latitude'] = df['Geocode_Address'].apply(lambda x: x.latitude)

        # Extracting the longitude from the Geocode_Address object:
        dataframe['Longitude'] = df['Geocode_Address'].apply(lambda x: x.longitude)

        return dataframe

    def Add_University(dataframe, University):
        ''' The method adds a column in the Processed_Dataframe that contains
        the geodesic distance from a Real_Estate listing to a University campus

    Parameters
    ----------
    dataframe : pandas dataframe
        The dataframe that is read from the Kelowna_Database containing
        Kelowna Real_Estate raw data

    University : University(object)
        The University object that contains the geospatial data for the
        University campus that is being compared to the Real_Estate data

    Returns
    -------
    dataframe
        The dataframe with distance from university added to said dataframe
        '''

    # TODO: Write Iterative loop / lamda function to calculate the university
    # distance.

    pass


class University(object):
    '''
    The University object contains relevant geospatial data about a campus.

    Parameters
    -----------
    latitude : float
        The latitude variable stores the latitude co-ordinate for the centre of
        campus

    longitude : float
        The longitude variable stores the longitude co-ordinate for the
        centre of campus

    Address : str
        The string contains the offical full address of the University campus

    University_name : str
        The string contains the name of the University

    Campus : str
        THe string contains the specific campus that the object represents
    '''
    def __init__(self, latitude, longitude, Address, University_name, Campus):
        self.latitude = latitude
        self.longitude = longitude
        self.University_name = University_name
        self.Campus = Campus
        self.Address = Address

# Creating an instance of the University() object for the UBC Okanagan campus:
UBC_Okanagan = University(49.941015, -119.396914,
 '3333 University Way, Kelowna, BC V1V 1V7, Canada', 'UBC', 'Okanagan')



# Code for Testing
test_dataframe = Kelowna_Database().Kijiji_Data_query('SELECT * FROM Kijiji_Data')
df = test_dataframe[0:10]
df = Processed_Dataframe.Add_Geotags(df)
#df = Processed_Dataframe.Add_University(df, UBC_Okanagan)
print(df)
