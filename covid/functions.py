#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""

Description
----------
This module gives general functions
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

import os, pygtc, configparser, json, sys
from os import path


# getting notebook directory
notebook_directory = os.getcwd()


    
def import_parameters(file_name: str):
    """
    Description
    ----------
    This function returns the directory address of notebook 
    and the tables directories.
    """

    # reading config file
    if path.exists(file_name):
        config = configparser.ConfigParser()
        config.read(file_name)

        #import parameters
        result = {'scl_factor'      : json.loads(config.get("MODEL", "scl_factor")),
                  'par_labels'      : json.loads(config.get("MODEL", "par_labels")),
                  'par_dim'         : len(json.loads(config.get("MODEL", "par_labels"))),
                  'par_est'         : json.loads(config.get("MODEL", "par_est")),
                  'par_stp'         : json.loads(config.get("MODEL", "par_stp")),
                  'data_filename'   : json.loads(config.get("DATASET", "data_filename")),
                  'data_url'        : json.loads(config.get("DATASET", "data_url")),
                  'data_update'     : json.loads(config.get("DATASET", "update")),
                  'country_1'       : json.loads(config.get("COUNTRY", "country_1")),
                  'mcmc_file_name'  : json.loads(config.get("MCMC", "file_name")),
                  'generate_mcmc'   : json.loads(config.get("MCMC", "generate_mcmc")),
                  'overwrite_file'  : json.loads(config.get("MCMC", "overwrite_file")),
                  'sample_length'   : json.loads(config.get("MCMC", "sample_length")),
                  'n_walkers'       : json.loads(config.get("MCMC", "n_walkers")),
                  'fit_confirmed'   : json.loads(config.get("MCMC", "fit_confirmed")),
                  'fit_death'       : json.loads(config.get("MCMC", "fit_death")),
                  'fit_recovered'   : json.loads(config.get("MCMC", "fit_recovered"))
                  }

    else:
        result = {}

    return result



    
def set_dir_struct():
    """
    Description
    ----------
    This function returns the directory address of notebook 
    and the tables directories.
    """
    
    lista=[];
    lista.append(notebook_directory);
    lista.append(os.path.join(notebook_directory, "tables"));
    return lista




def file_names(direct = os.getcwd()):
    """
    Description
    ----------
    This function receive a directory address as argument
    and return a list of strings with the names of all files
    inside it.
    """
    print(direct)
    return os.listdir(direct)




def riffle(lst, item):
    """
    Description
    ----------
    Put the item between each element of the list "lst".
    """
    result = [item] * (len(lst) * 2 - 1)
    result[0::2] = lst
    return result




def set_directory(direc):
    """
    Description
    ----------
    This function receive a directory addres as argument
    and set this as the current work directory.
    """
    os.chdir(direc)
    
    
    
    
def distribute_among_walkers(quantity,walkers):
    
    '''
    Description
    ----------
    This function returns a list with size equal to "walkers".
    Its divide the "quantity" for the number of walkers keeping
    the modules on the firsts.
    '''
    
    div_int = quantity//walkers
    div_mod = quantity%walkers

    walkers_list = []
    
    for index in range(walkers):
        mod_sum = 1 if index < div_mod else 0
        walker_stps = div_int + mod_sum
        walkers_list.append(walker_stps)
        
    return(walkers_list)