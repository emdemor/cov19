#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""

Description
----------
The region object contains information and actions 
related the regions that are important to understand 
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



class region:
    '''
    Description
    ----------
    The region object contains information and actions related the regions
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
    
    def __init__(self,
        name,
        population,
        df,
        rescaling_by  = 1,
        last_index    = -1,
        confirmed_col = 'Confirmed',
        recovered_col = 'Recovered',
        deaths_col    = 'Deaths',
        actives_col   = 'Actives'
        ):
        
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
        df_Region = df.loc[(df[reg_column] == self.name) & (df['AdminRegion1'] == '')]
        
        # getting the first case
        first_case = df_Region['Updated'].min()
        
        # couting teh days after first case
        df_Region['Days'] = (df_Region['Updated'] - first_case).dt.days.astype(float)
        
        # rescaling cases by a factor
        df_Region[['Confirmed','Actives','Deaths','Recovered']] = df_Region[['Confirmed','Actives','Deaths','Recovered']]*rescaling_by
        self.dataframe = df_Region
        
        # converting columns to lists
        self.days_list = df_Region['Days'].to_numpy()
        self.confirmed_list = df_Region['Confirmed'].to_numpy()
        self.death_list = df_Region['Deaths'].to_numpy()
        self.recovered_list = df_Region['Recovered'].to_numpy()
        
        