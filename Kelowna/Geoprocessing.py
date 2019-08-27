# Importing the database connectors:
from Kelowna_Database_management import Kelowna_Database

# Importing data manipulation packages:
import pandas as pd
import geopy
from geopy.geocoders import Nominatim

# Creating the object variable that represents the dataframe that
# will be used for all the main ML processing:
class Processed_Dataframe():
    # TODO: Add Docstring

    # Function that converts address variables and adds lat and long columns:
    def Add_Geotags(dataframe):
        # TODO: Add Docstring

        
        # Creating Nominatim object:
        nom = Nominatim(user_agent = 'Kijij_df_Geoprocessor')
        address = nom.geocode('720 Commonwealth Rd 43, Kelowna, BC V4V 1R8, Canada')


    # Function that calculates and adds the Distance from University Campus:
    def Add_University(dataframe):
        # TODO: Add Docstring
        pass


test_dataframe = Kelowna_Database().Kijiji_Data_query('SELECT * FROM Kijiji_Data')
#print(test_dataframe['Address'][0])

Processed_Dataframe.Add_Geotags(test_dataframe)
