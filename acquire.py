#import libraries
import warnings
warnings.filterwarnings("ignore")

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os

# Connection
from env import host, user, password

# Acquire Zillow Data

# Create function to get the necessary connection url.
def get_connection(db, user=user, host=host, password=password):
    '''
    This function uses my info from my env file to
    create a connection url to access the Codeup db. It takes in a string 
    name of a database as an argument
    '''
    return f'mysql+pymysql://{user}:{password}@{host}/{db}'


#create function to retrieve zillow data
def new_zillow_data():
    '''
    This function reads the Telco data from the Codeup db
    and returns a pandas DataFrame with three joined tables and all columns.
    '''
    
    sql_query = '''
   
       SELECT prop.*,
       pred.logerror,
       pred.transactiondate,
       air.airconditioningdesc,
       arch.architecturalstyledesc,
       build.buildingclassdesc,
       heat.heatingorsystemdesc,
       landuse.propertylandusedesc,
       story.storydesc,
       construct.typeconstructiondesc
       FROM   properties_2017 prop
       INNER JOIN (SELECT parcelid,
                   Max(transactiondate) transactiondate
                   FROM   predictions_2017
                   GROUP  BY parcelid) pred
               USING (parcelid)
       JOIN predictions_2017 as pred USING (parcelid, transactiondate)
       LEFT JOIN airconditioningtype air USING (airconditioningtypeid)
       LEFT JOIN architecturalstyletype arch USING (architecturalstyletypeid)
       LEFT JOIN buildingclasstype build USING (buildingclasstypeid)
       LEFT JOIN heatingorsystemtype heat USING (heatingorsystemtypeid)
       LEFT JOIN propertylandusetype landuse USING (propertylandusetypeid)
       LEFT JOIN storytype story USING (storytypeid)
       LEFT JOIN typeconstructiontype construct USING (typeconstructiontypeid)
       WHERE  prop.latitude IS NOT NULL
       AND prop.longitude IS NOT NULL
       '''
    # Read in DataFrame from Codeup db.
    df = pd.read_sql(sql_query, get_connection('zillow'))
    
    return df

# this is to cache a csv file of the data from the db for a quicker read
def get_zillow_data():
    '''
    checks for existing csv file
    loads csv file if present
    if there is no csv file, calls new_zillow_data
    '''
    
    if os.path.isfile('zillow.csv'):
        
        df = pd.read_csv('zillow.csv', index_col=0)
        
    else:
        
        df = new_zillow_data()
        
        df.to_csv('zillow.csv')

    return df


def get_data_summary(df):
    '''
    This function takes in a pandas dataframe and prints out the shape of the dataframe, number of missing values, 
    columns and their data types, summary statistics of numeric columns in the dataframe, as well as the value counts for categorical variables.
    '''
    # Print out the "shape" of our dataframe - the rows and columns we have to work with
    print(f'The zillow dataframe has {df.shape[0]} rows and {df.shape[1]} columns.')
    print('')
    print('-------------------')

    # print the number of missing values in our dataframe
    print(f'There are total of {df.isna().sum().sum()} missing values in the entire dataframe.')
    print('')
    print('-------------------')

    # print some information regarding our dataframe
    df.info()
    print('')
    print('-------------------')
    
    # print out summary stats for our dataset
    print('Here are the summary statistics of our dataset')
    print(df.describe())
    print('')
    print('-------------------')

    print('Here are the categories and their relative proportions')
    # check different categories and proportions of each category for object type cols
    show_vc = ['county','bathrooms','bedrooms', 'year_built']
    for col in df.columns:
        if col in show_vc:
            print(f'value counts of {col}')
            print(df[col].value_counts())
            print('')
            print(f'proportions of {col}')
            print(df[col].value_counts(normalize=True,dropna=False))
            print('-------------------')


