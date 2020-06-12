#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 12 02:35:02 2020

@author: eduardo
"""


import numpy as np
import pandas as pd
import random
from tqdm import tqdm,tqdm_notebook
from .functions import distribute_among_walkers, riffle
from scipy import stats
import matplotlib.pyplot as plt



class stat_model:
    
    def __init__(self,dataframe,ep_model,par_est,
                 par_min=False,par_max=False,
                 par_labels = False,rescale=1,tend=False):
        
        self.dataframe = dataframe
        self.ep_model = ep_model
        self.par_est = par_est
        self.rescale = rescale
        
        if tend == False:
            self.tend = dataframe.days_list[-1]
        else:
            self.tend = tend
            
        if par_labels == False:
            self.par_labels = list(map(lambda a: 'p'+a,list('12345')))
        else:
            self.par_labels = par_labels
            
        self.mcmc_sample = False
        self.sample_imported = False
        
        
    def solve(self,parameters):
        return self.ep_model(par = parameters, x0 = [10**(parameters[-1]),self.rescale,0,0],tend=self.tend)
       
    def chi_sqrd(self,par):

        '''
        Importante notar que (par_est,) é uma tupla de apenas um elemento.
        Caso pusessemos (par_est), os parenteses não indicariam uma tupla
        '''
        model = self.solve(par)
      
        t_model = model.days_list      
        c_model = model.confirmed_list
        r_model = model.recovered_list
        d_model = model.death_list
        
        t_data = self.dataframe.days_list    
        c_data = self.dataframe.confirmed_list
        r_data = self.dataframe.recovered_list
        d_data = self.dataframe.death_list

        chi2 = lambda model, data: (model-data)**2

        Chi2_c = sum(list(map(chi2, list(np.interp(t_data, t_model, c_model)), c_data)))
        Chi2_r = sum(list(map(chi2, list(np.interp(t_data, t_model, r_model)), r_data)))
        Chi2_d = sum(list(map(chi2, list(np.interp(t_data, t_model, d_model)), d_data)))

        return Chi2_c+Chi2_r+Chi2_d

    
    def log_prob(self,par):
        lnP = - 0.5 * self.chi_sqrd(par)

        return lnP


    def metropolis_hastings(self,n_points,par_stp,file_name="mcmc.csv",overwrite=False,n_walkers=1):
        
        # distributing the points to walkers
        n_walkers_list = distribute_among_walkers(n_points,n_walkers)
        
        # cleaning the old file
        if overwrite:
            open(file_name, 'w').close()

        # open a new file to append
        file = open(file_name, 'a')

        # writing the header
        if overwrite:
            file.write(''.join(riffle(self.par_labels,'\t'))+'\n')


        # looping through the walkers
        for ind_walker in range(len(n_walkers_list)):

            # evaluating the log-probability of the guess
            PAR = self.par_est
            log_PROB = self.log_prob(PAR)

            # looping through the walker amount of points
            for n in tqdm(range(n_walkers_list[ind_walker]),desc='walker '+str(1+ind_walker)+': '):

                # suggest new candidate from uniform distribution
                PAR_NEW  = list(map(lambda p,h: p + random.uniform(-1, 1)*h ,np.array(PAR),np.array(par_stp)))
                log_PROB_NEW = self.log_prob(PAR_NEW)

                # accept new candidate in Monte-Carlo fashing.
                if (log_PROB_NEW > log_PROB):
                    PAR  = PAR_NEW
                    log_PROB = log_PROB_NEW
                else:
                    u = random.uniform(0.0,1.0)
                    if (u < np.exp(log_PROB_NEW - log_PROB)):
                        PAR  = PAR_NEW
                        log_PROB = log_PROB_NEW

                # writing on file
                file.write(''.join(riffle(list(map(str,PAR)),'\t'))+'\n')

        file.close()
            
        self.mcmc_sample = True
        
    def import_sample(self,file_name="mcmc.csv"):
        
        #importing
        raw_sample_df = pd.read_csv(file_name,sep="\t")
        
        # removing outliers
        self.sample_df = raw_sample_df[(np.abs(stats.zscore(raw_sample_df)) < 3.1).all(axis=1)]
        self.sample = self.sample_df.to_numpy()
        
        self.sample_imported = True
        
        return self.sample_df.info()
    
    def data_model_plot(self,par):
        model = self.solve(par)

        # Confirmed Cases Plot
        plt.plot(model.days_list,model.confirmed_list,color='#27408B', label='Confirmed')
        plt.scatter(self.dataframe.days_list,self.dataframe.confirmed_list, color='#436EEE',alpha=0.9,s=5)

        # Recovered Cases Plot
        plt.plot(model.days_list,model.recovered_list,color='#008B45', label='Recovered')
        plt.scatter(self.dataframe.days_list,self.dataframe.recovered_list, color='#00CD66',alpha=0.9,s=5)

        # Death Cases Plot
        plt.plot(model.days_list,model.death_list,color='#EE7621', label='Deaths')
        plt.scatter(self.dataframe.days_list,self.dataframe.death_list, color='#FF7F24',alpha=0.9,s=5)


        plt.legend(loc="upper left")
        plt.xlabel('days after first case')
        plt.ylabel('thousands of people')
        plt.grid()
        plt.savefig("crd-curve.png")
        plt.show()

        