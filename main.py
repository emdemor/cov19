#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 12 02:35:02 2020

@author: eduardo
"""


from covid import read_dataset,country,mod_sird
from covid.stat import stat_model
import numpy as np
import pygtc
import matplotlib.pyplot as plt

# Raw Estimated Parameters
scl_factor = 1000;
par_labels = ['α','β','r','d','log10(S0)']
par_guess = np.array([0.806, 0.268, 0.104, 0.012,3.64])
par_stp = [0.001,0.0004,0.0003,7.25e-05,0.2]

#par_min = [0.821988,0.265467,0.100173,0.014379,2]
#par_max = [0.829652,0.269414,0.104309,0.016515,5]

par_dim = len(par_labels)

# read dataset 
#df = read_dataset('Bing-COVID19-Data.csv')
df = read_dataset('https://raw.githubusercontent.com/microsoft/Bing-COVID-19-Data/master/data/Bing-COVID19-Data.csv',url=True)

# choosing a country
brasil_df = country(name = "Brazil", population = 212000000)
brasil_df.dataset(df,rescaling_by=1/scl_factor)

# defining statistical model
StatModel = stat_model(brasil_df,mod_sird,par_guess,rescaling_by = 1/scl_factor,par_labels=par_labels)
StatModel.data_model_plot(par_guess)

# generating a mcmc sample by metropolis-hastings algorithm
#StatModel.metropolis_hastings(1000,par_stp,overwrite=False,file_name='mcmc_sample_5par.csv')
StatModel.import_sample(file_name='mcmc_sample_5par.csv')
SingleParameterEstimates = StatModel.single_parameter_estimates(alpha=0.3173)
GTCPlot = StatModel.gtc_plot()

plt.show()

StatModel.data_model_plot(SingleParameterEstimates[:,1])

