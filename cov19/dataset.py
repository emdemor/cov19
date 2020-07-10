#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""

Description
----------
The country object contains information and actions 
related the countries that are important to understand 
the Covid dissemination

Informations
----------
    Author: Eduardo M.  de Morais
    Maintainer:
    Email: emdemor415@gmail.com
    Copyright:
    Credits:
    License:
    Version:
    Status: in development
    
"""

import pandas as pd
import numpy as np

from .functions import set_dir_struct, riffle, file_names, set_directory, distribute_among_walkers
from os import path

# empty dataframe to use in case of error
__EMPTY_DATAFRAME__ = pd.DataFrame({'ID' :[],
                                  'Updated' :[],
                                  'Confirmed' :[],
                                  'ConfirmedChange' :[],
                                  'Deaths' :[],
                                  'DeathsChange' :[],
                                  'Recovered' :[],
                                  'RecoveredChange' :[],
                                  'Latitude' :[],
                                  'Longitude' :[],
                                  'ISO2' :[],
                                  'ISO3' :[],
                                  'Country_Region' :[],
                                  'AdminRegion1' :[],
                                  'AdminRegion2' :[]})



# global variables to use as standard 
__DATASET_URL__ = 'https://raw.githubusercontent.com/microsoft/Bing-COVID-19-Data/master/data/Bing-COVID19-Data.csv'

__DATASET_FILENAME__ = 'Bing-COVID19-Data.csv'





def read_dataset(update_data = False,
                 url         = __DATASET_URL__,
                 local_dataset_filename = __DATASET_FILENAME__):
    '''
    Description
    ----------
    This function imports the Microsoft dataset from local source. If
    required, downloads the updated date from online source and saves 
    it on the tables directory, owerwritten the previous file.

    After import, converts the columns to the right types, change the
    name of some countries and creates a new column for active infections.

    Arguments
    ----------
    update_data: bool
        Controls if the data will be updated

    url: str
        URL to download the online sourde

    local_dataset_filename: str
        Name (without path) of localbase dataset

    Return
    ----------
    df: Pandas.DataFrame
        Final dataset
        
    '''

    # join filename with directory
    #filename = path.join(tables_directory, local_dataset_filename)
    filename = local_dataset_filename

    # updating when required
    if update_data:
        update_local_base(url,filename)
    
    #importing dataset
    df = import_from_localbase(filename)[0]

    # Filling NA values
    df[['ISO2','ISO3','Country_Region','AdminRegion1','AdminRegion2']] = df[['ISO2','ISO3','Country_Region','AdminRegion1','AdminRegion2']].fillna('')
    df[['Confirmed','ConfirmedChange','Deaths','DeathsChange','Recovered','RecoveredChange']] = df[['Confirmed','ConfirmedChange','Deaths','DeathsChange','Recovered','RecoveredChange']].fillna(0)
    
    # Type coversion
    df[['Confirmed','ConfirmedChange','Deaths','DeathsChange','Recovered','RecoveredChange']] = df[['Confirmed','ConfirmedChange','Deaths','DeathsChange','Recovered','RecoveredChange']].astype(float)
    df[['ISO2','ISO3','Country_Region','AdminRegion1','AdminRegion2']] = df[['ISO2','ISO3','Country_Region','AdminRegion1','AdminRegion2']].astype(str)
    
    # Replacing Countries names
    df['Country_Region'] = df['Country_Region'].replace('China (mainland)','China')
    
    # Creating a new column
    df['Actives'] = df['Confirmed']-df['Deaths']-df['Recovered']

    return df


def import_from_url(url):
    '''
    Description
    ----------
    
    Arguments
    ----------
        
    '''

    try:
        print('[status]: Downloading dataset from source.')
        dataframe = pd.read_csv(url,sep=",",parse_dates=['Updated'])
        return [dataframe,True]

    except:
        # When occours some
        print('[error]: It was not possible to download data from online source.')
        return [__EMPTY_DATAFRAME__,False]



def import_from_localbase(filename):
    '''
    Description
    ----------
    
    Arguments
    ----------
        
    '''
    try:
        if not path.exists(filename):
            print('[warng]: There is no previous dataset on the localfile. Dataset must be downloaded from online source.')
            print('[mssge]: Getting data from online source :'+__DATASET_URL__+'.')
            update_local_base(__DATASET_URL__,filename)

        print('[status]: Importing dataset from localbase.')
        dataframe = pd.read_csv(filename,sep=",",parse_dates=['Updated'])
        return [dataframe,True]

    except:
        print('[error]: There is no local base file.')
        return [__EMPTY_DATAFRAME__,False]


def export_to_local_base(df,address):
    '''
    Description
    ----------
    
    Arguments
    ----------
        
    '''
    try:
        print('[status]: Updating local dataset base.')
        df.to_csv(address,sep=',',index=False)
    except:
        print('[error]: It was not possible to export data to local base.')


def update_local_base(url,address):
    '''
    Description
    ----------
    
    Arguments
    ----------
        
    '''

    try:
        df,__IMPORT_STATUS__ = import_from_url(url)

        if __IMPORT_STATUS__ :
            export_to_local_base(df,address)
        else:
            if not path.exists(address):
                print('[error]: Is impossible to access the data from local base or online source.')
            else:
                print('[mssge]: Keeping the previous data on local base.')
    except:
        print('[error]: It was not possible update local base.')

