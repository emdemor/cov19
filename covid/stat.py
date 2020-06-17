#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 12 02:35:02 2020

@author: eduardo
"""


import random,pygtc
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from tqdm import tqdm
from .functions import distribute_among_walkers, riffle,notebook_directory,set_directory
from scipy import stats
from covid import root_directory,tables_directory



class stat_model:
    
    def __init__(self,
                 dataframe,
                 ep_model,
                 par_est,
                 par_min=False,
                 par_max=False,
                 par_labels = False,
                 rescaling_by=1,
                 tend=False
                 ):
        
        self.dataframe = dataframe
        self.ep_model = ep_model
        self.par_est = par_est
        self.rescale = rescaling_by
        
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
        self.ndim = len(par_est)
        
        
    def solve(self,parameters):
        return self.ep_model(par = parameters, x0 = [10**(parameters[-1]),self.rescale,0,0],tend=self.tend)
       
    def chi_sqrd(self,
                 par,
                 fit_recovered = True,
                 fit_death = True,
                 fit_comfirmed = True
                 ):

        '''
        Importante notar que (par_est,) é uma tupla de apenas um elemento.
        Caso pusessemos (par_est), os parenteses não indicariam uma tupla
        
        Aqui existe um problemanNos casos em que o valor temporal dos dados
        é maior do que o valor tend fornecido pelo usuário. É preciso realizar 
        o tratamento de erros
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
        
        Chi2 = 0;
        
        if fit_comfirmed:
            Chi2 += sum(list(map(chi2, list(np.interp(t_data, t_model, c_model)), c_data)))
            
        if fit_recovered:
            Chi2 += sum(list(map(chi2, list(np.interp(t_data, t_model, r_model)), r_data)))
            
        if fit_death:
            Chi2 += sum(list(map(chi2, list(np.interp(t_data, t_model, d_model)), d_data)))



        return Chi2

    
    def log_prob(self,
                 par,
                 fit_recovered = True,
                 fit_death = True,
                 fit_comfirmed = True
                 ):
        
        lnP = - 0.5 * self.chi_sqrd(par,
                                    fit_recovered = fit_recovered,
                                    fit_death = fit_death,
                                    fit_comfirmed = fit_comfirmed
                                    )

        return lnP


    def metropolis_hastings(self,
                            n_points,
                            par_stp,
                            file_name = "mcmc.csv",
                            overwrite = False,
                            n_walkers = 1,
                            fit_recovered = True,
                            fit_death = True,
                            fit_comfirmed = True
                            ):
        
        # distributing the points to walkers
        n_walkers_list = distribute_among_walkers(n_points,n_walkers)
        
        # changing to tables directory
        set_directory(tables_directory)
        
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
            log_PROB = self.log_prob(PAR,
                                    fit_recovered = fit_recovered,
                                    fit_death = fit_death,
                                    fit_comfirmed = fit_comfirmed)

            # looping through the walker amount of points
            for n in tqdm(range(n_walkers_list[ind_walker]),desc='walker '+str(1+ind_walker)+': '):

                # suggest new candidate from uniform distribution
                PAR_NEW  = list(map(lambda p,h: p + random.uniform(-1, 1)*h ,np.array(PAR),np.array(par_stp)))
                log_PROB_NEW = self.log_prob(PAR_NEW,
                                    fit_recovered = fit_recovered,
                                    fit_death = fit_death,
                                    fit_comfirmed = fit_comfirmed)

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
        
        # returning to root directory
        set_directory(tables_directory)
        
        # updating mcmc_sample variable
        self.mcmc_sample = True
        
    def import_sample(self,file_name="mcmc.csv"):
        
        # setting tables directory
        set_directory(tables_directory)
        
        #importing
        self.raw_sample_df = pd.read_csv(file_name,sep="\t")
        self.raw_sample = self.raw_sample_df.to_numpy()
        
        # removing outliers
        self.sample_df = self.raw_sample_df[(np.abs(stats.zscore(self.raw_sample_df)) < 3.1).all(axis=1)]
        self.sample = self.sample_df.to_numpy()
        
        # updating sample_imported
        self.sample_imported = True
        
        # returning to root directory
        set_directory(root_directory)
        
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
        set_directory(tables_directory)
        plt.savefig("crd-curve.png")
        set_directory(root_directory)
        plt.show()
        
    def single_parameter_estimates(self,alpha=0.3173):
        if not self.sample_imported:
            print('Error: you must read a mcmc sample file first.')
            return []
        else:
            var = 100*alpha/2
            interval = np.array(list(map(lambda index: np.percentile(self.raw_sample[:, index], [var, 50,100-var]),list(range(self.ndim)))))
            return interval
            
        
    def gtc_plot(self,
                 truths=None,
                 n_contour_levels=2, 
                 figure_size = 8, 
                 custom_label_font = {'family':'DejaVu Sans', 'size':10}, 
                 custom_tick_font = {'family':'DejaVu Sans', 'size':8},
                 save_figure = False,
                 file_name = 'figGTC.png'
            ):
        
        GTC = pygtc.plotGTC(chains=[self.sample ],
                    truths = truths,
                    paramNames = self.par_labels,
                    nContourLevels = n_contour_levels,
                    figureSize = figure_size,
                    customLabelFont = custom_label_font,
                    customTickFont = custom_tick_font 
                   )
        
        if save_figure:
            set_directory(tables_directory)
            GTC.savefig('GTC.png')
            set_directory(root_directory)
        
        return GTC
            
            
          
        