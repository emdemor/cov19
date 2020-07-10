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



class country:
    '''
    Description
    ----------
    The country object contains information and actions related the countries
    that are important to understand the Covid dissemination

    Arguments
    ----------
    name: str
        String passed by the user to label the country
        
    population: int
        Integer number passed by the user counting people in the related 
        country

    Parameters
    ----------
    self.name: str
        String used to label the country.
        
    self.population: int
        Integer number with the number of people in the related country
        
    self.dataframe: pandas.DataFrame
        DataFrame object with data about covid cases.
        
    self.days_list: numpy.ndarray
        Numpy array with the days after first confirmed covid case
        
    self.confirmed_list: numpy.ndarray
        Numpy array with the number of confirmed cases. Must have the same 
        length of self.days_list
        
    self.recovered_list: numpy.ndarray
        Numpy array with the number of recovered cases. Must have the same 
        length of self.days_list
        
    self.death_list: numpy.ndarray
        Numpy array with the number of deaths cases. Must have the same 
        length of self.days_list
        
    '''
    
    def __init__(self,name,population):
        self.name = name
        self.population = population
        
    def dataset(self,df,rescaling_by=1,last_index = 'last'):
        
        """
        Receive a global dataframe with COVID data from microsoft repository,
        select those related to informed country and sets the country class' 
        parameters

        Parameters
        ----------
        df_Country : pandas dataframe
            Filter the information related to the country
            
        first_case : timestamp
            Date of fist covid case
        
        Returns
        -------
        void
        
        """
        
        # getting the data from country
        df_Country = df.loc[(df['Country_Region'] == self.name) & (df['AdminRegion1'] == '')]

        # selecting interval if user requires
        if (not isinstance(last_index,str)) & (isinstance(last_index,int)):
            df_Country = df_Country.iloc[1:last_index,:]
        
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
        
        