#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 12 02:35:02 2020

@author: eduardo
"""


class country:
    
    def __init__(self,name,population):
        self.name = name
        self.population = population
        
    def dataset(self,df,rescaling_by=1,last_index=-1):
        
        # getting the data from country
        df_Country = df.loc[(df['Country_Region'] == self.name) & (df['AdminRegion1'] == '')]
        
        # getting the first case
        first_case = df_Country['Updated'].min()
        
        # couting teh days after first case
        df_Country['Days'] = (df_Country['Updated'] - first_case).dt.days.astype(float)
        
        # rescaling cases by a factor
        df_Country[['Confirmed','Actives','Deaths','Recovered']] = df_Country[['Confirmed','Actives','Deaths','Recovered']]*rescaling_by
        self.dataframe = df_Country
        
        # converting columns to lists
        self.days_list = df_Country['Days'].to_numpy()
        self.confirmed_list = df_Country['Confirmed'].to_numpy()
        self.death_list = df_Country['Deaths'].to_numpy()
        self.recovered_list = df_Country['Recovered'].to_numpy()
        
        