#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 12 02:57:59 2020

@author: eduardo
"""
import pandas as pd
import numpy as np

from .functions import set_dir_struct, riffle, file_names, set_directory, distribute_among_walkers


# setting directory structure
root_directory,tables_directory = set_dir_struct();     

set_directory(root_directory)

def read_dataset(address,url=False):
    
    # Choose to import from a local or a online source
    Import_from_URL_Q = url;
    
    if Import_from_URL_Q:
        df = pd.read_csv(address,sep=",",parse_dates=['Updated'])
        
    else:
        # importing the dataset from local file
        set_directory(tables_directory);
        df = pd.read_csv(address,sep=",",parse_dates=['Updated'])
        set_directory(root_directory);
    
    # Filling NA values
    df[['ISO2','ISO3','Country_Region','AdminRegion1','AdminRegion2']] = df[['ISO2','ISO3','Country_Region','AdminRegion1','AdminRegion2']].fillna('')
    df[['Confirmed','ConfirmedChange','Deaths','DeathsChange','Recovered','RecoveredChange']] = df[['Confirmed','ConfirmedChange','Deaths','DeathsChange','Recovered','RecoveredChange']].fillna(0)
    
    # Type coversion
    df[['Confirmed','ConfirmedChange','Deaths','DeathsChange','Recovered','RecoveredChange']] = df[['Confirmed','ConfirmedChange','Deaths','DeathsChange','Recovered','RecoveredChange']].astype(float)
    df[['ISO2','ISO3','Country_Region','AdminRegion1','AdminRegion2']] = df[['ISO2','ISO3','Country_Region','AdminRegion1','AdminRegion2']].astype(str)
    
    # Replacing Countries names
    df['Country_Region'] = df['Country_Region'].replace('China (mainland)','China')
    
    # Creating a new column
    df['Actives'] = df['Confirmed']-df['Deaths']-df['Deaths']
    
    return df