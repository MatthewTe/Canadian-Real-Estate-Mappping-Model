# Importing db management packages:
import sqlite3
from sqlalchemy import create_engine
import pandas as pd
# Importing the Kijiji class from Kijiji.py package:
from Kijiji import Kijiji



class Kelowna_Database():
    '''
    The Object that represents the Kelowna Database for all CRUD functions.

    Kelowna_Database() is used as a means of accessing the Kelowna database
    and returning queries. All of the CRUD functions are performed via the
    pandas data package. Reading data from the dataframe is done via the
    pd.read_sql() pandas function. Writing data to the dataframe is done via the
    df.to_sql() pandas function.

    '''
    def __init__(self):
        '''Initalizes the class by either creating a local database if none exists
            or creating the connection to said database if the local database already
            exists
        '''

        try:
            conn = sqlite3.connect('Kelowna_Real-Estate_db',check_same_thread=False)
            self.con = conn

        except:
            engine = create_engine('sqlite:///Kelowna_Real-Estate_db')
            conn = sqlite3.connects('Kelowna_Real-Estate_db',check_same_thread=False)
            self.con = conn

    def Kijiji_main_push(self, num_pages):
        '''Reading the Kijiji-listings-data dataframe into the sqlite database

        Parameters
        ----------
        num_pages : int
            The number of Kijiji Real-Estate page data that will be read into the
            dataframe
        '''

        self.num_pages = num_pages
        # url for the first page of the Kelowna Real Estate area listings:
        init_url = 'https://www.kijiji.ca/b-for-sale/kelowna/c30353001l1700228'

        Kijiji.get_data(init_url, num_pages).to_sql('Kijiji_Data', con=self.con,
        if_exists='replace')

    def Kijiji_Data_query(query_string):
        '''Reading data from the Kijiji_Real-Estate_db based on a specific sql
            query

        Parameters
        ----------
        query_string : str
            The query written in SQL query syntax that dictates what data is pulled
            from the database

        Returns
        -------
        df : Pandas dataframe
            The dataframe containing the data that is sql queried from the database
        '''

        df = pd.read_sql(query_string, self.con)

        return df


Kelowna_Database().Kijiji_main_push(200)
