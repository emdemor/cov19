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

def main(file_name):

	# import parameter from configuration file
	param = import_parameters(file_name)
 
	# dimension of parametric space
	# par_dim = len(param['par_labels'])

	df = read_dataset(update_data = param['data_update'],
                	  url         = param['data_url'] ,
                      local_dataset_filename = param['data_filename'])

	# choosing a country
	brasil_df = country(name      = param['country_1'][0],
		                population = param['country_1'][1]
		                )

	brasil_df.dataset(df,rescaling_by=1/param['scl_factor'])



	# defining statistical model
	StatModel = stat_model(brasil_df,
	                       mod_sird,
	                       param['par_est'],
	                       rescaling_by = 1/param['scl_factor'],
	                       par_labels   = param['par_labels']
	                       )
	#StatModel.data_model_plot(param['par_est'])


	# generating a mcmc sample by metropolis-hastings algorithm
	if param['generate_mcmc']:
		StatModel.metropolis_hastings(n_points  = param['sample_length'],
		                              par_stp   = param['par_stp'],
		                              overwrite = param['overwrite_file'],
		                              file_name = param['mcmc_file_name']
		                              )
	
	
	
	StatModel.import_sample(file_name = param['mcmc_file_name'])
	SingleParameterEstimates = StatModel.single_parameter_estimates(alpha=0.3173)
	GTCPlot = StatModel.gtc_plot(save_figure = True)
	#print('\n',SingleParameterEstimates,'\n\n')


	StatModel.evaluate_epidemiological_parameters(SingleParameterEstimates['Mean'].to_list())

	'''

	plt.legend(loc="upper left")
	plt.xlabel('days after first case')
	plt.ylabel('thousands of people')
	plt.grid()

	plt.savefig('results/cases_projection.png')
	#plt.savefig('results/cases_projection.pdf')
	#plt.show()
	print('\n\n')
	'''


if __name__ == "__main__":

	args = sys.argv;

	if (len(sys.argv) != 2):
		print('[Error]: You must pass a parameter file to '+str(args[0]))
	else:
		main(args[1])
	print('[status]: Finished.')