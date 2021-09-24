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
def get_db_url(database):
    from env import host, user, password
    url = f'mysql+pymysql://{user}:{password}@{host}/{db}'
    return url

#def get_connection(db, user=user, host=host, password=password):
    '''
    This function uses my info from my env file to
    create a connection url to access the Codeup db. It takes in a string 
    name of a database as an argument
    '''
    #return f'mysql+pymysql://{user}:{password}@{host}/{db}'
    
def get_zillow(sql):
    url = get_db_url('zillow')
    zillow_df = pd.read_sql(sql_query, url, index_col='id')
    return zillow_df


#create function to retrieve zillow data
#def new_zillow_data():
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
    #df = pd.read_sql(sql, get_connection('zillow'))
    
    #return df

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
        
        df = get_zillow()
        
        df.to_csv('zillow.csv')

    return df




  
   



    