# Importing the database connectors:
from Kelowna_Database_management import Kelowna_Database

# Importing data manipulation packages:
import pandas as pd
import geopy
from geopy.geocoders import OpenCage
from geopy import distance

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

def Add_University(dataframe):

    ''' The method adds a column in the Processed_Dataframe that contains
    the geodesic distance from a Real_Estate listing to a University campus

    Parameters
    ----------
    dataframe : pandas dataframe
        The dataframe that is read from the Kelowna_Database containing
        Kelowna Real_Estate raw data

        Returns
        -------
        dataframe
        The dataframe with distance from university added to said dataframe
        '''

    # Creating an instance of the University() object for the UBC Okanagan campus:
    UBC_Okanagan = University(49.941015, -119.396914,
    '3333 University Way, Kelowna, BC V1V 1V7, Canada', 'UBC', 'Okanagan')

    Univerity_Location = (UBC_Okanagan.latitude, UBC_Okanagan.longitude)


    # Variables for the Iterative loops:
    Univerity_Distance_List = []
    counter = 0
    l = len(dataframe)
    dataframe.dropna(inplace=True)

    # Creating a loop to iterate through the dataframe adding UBC distance:
    for i in range(l):

        # Creating the location for an address:
        try:
            Real_Estate_location = (dataframe['Latitude'][counter],
            dataframe['Longitude'][counter])

            # Calculating distance:
            Distance_from_University = distance.distance(Real_Estate_location,
             Univerity_Location)

        # If Rea;Real_Estate_location errors out:
        except:
            Distance_from_University = 'NaN'

        Univerity_Distance_List.append(Distance_from_University)

        counter = counter + 1

    dataframe['UBC_Distance'] = Univerity_Distance_List

    return dataframe

def Add_Interest_rates(dataframe):
    # TODO: Write the method that adds interests rates
    pass

class Processed_Dataframe():
    '''
    The object that represents the raw dataframe read from the Kelowna_Database
    and contains all the methods used to produce the final processed dataframe.

    Processed_Dataframe() contains all the methods that modify the raw data read
    from the Kijiji_Database. These methods each add one or several columns
    to the raw dataframe. These columns will all contain data derived from the
    ['Address'] column and subsequent location data.

    Parameters
    ----------
    dataframe : pandas dataframe
        The raw dataframe that is read from the Kelowna_Database
    '''

    def __init__(self, dataframe):

        # Inital raw dataframe:
        self.dataframe = dataframe

        # Creating the Compiled dataframe:
        self.df_final = self.Compile()


    def Compile(self):
        '''Method that applys all the global compile functions to the self.dataframe
            pandas dataframe
        '''
        # Performing the Geotagging function on the inital dataframe:
        df = Add_Geotags(self.dataframe)

        # Performing the Add_University method on the now local df variable:
        df = Add_University(df)

        return df

    def Return_df(self):
        '''Method that returns the final processed dataframe variable
        '''
        return self.df_final



# Code for Testing
test_dataframe = Kelowna_Database().Kijiji_Data_query('SELECT * FROM Kijiji_Data')
df = test_dataframe[0:10]

Processed_Dataframe(df).Return_df()
