#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Description
----------
This is the main file of aplication

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

from covid import read_dataset,country,mod_sird
from covid.stat import *
from covid.functions import *
from numpy import random
import numpy as np
import pygtc, configparser, json, sys
import matplotlib.pyplot as plt
import covid.dataset as ds

import numpy as np
#from numpy import random
from covid import read_dataset,country,mod_sird
from covid.stat import stat_model
from IPython.display import display, Math
#from tqdm import tqdm,tqdm_notebook
import matplotlib.pyplot as plt


# Raw Estimated Parameters
scl_factor = 1000;
par_labels = ['α','β','ρ','δ','logS0']
par_dim = len(par_labels)
par_est = np.array([0.837,0.260,0.1010,0.011,3.464])
par_stp = [0.001,0.0001,0.0001,7.25e-05,0.2]

#df = read_dataset('Bing-COVID19-Data.csv')
df = read_dataset('https://raw.githubusercontent.com/microsoft/Bing-COVID-19-Data/master/data/Bing-COVID19-Data.csv',url=True)
brasil_df = country(name = "Brazil", population = 212000000)
brasil_df.dataset(df,rescaling_by=1/scl_factor)

StatModel = stat_model(brasil_df,mod_sird,par_est,rescaling_by=1/scl_factor,par_labels=par_labels)
#StatModel.data_model_plot(par_est)


# crea
StatModel.import_sample(file_name='brazil_mcmc_sample_5par.csv');
SingleParameterEstimates = StatModel.single_parameter_estimates(alpha=0.3173)
GTCPlot = StatModel.gtc_plot(save_figure=True)
GTCPlot.show()