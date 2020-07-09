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

from covid import read_dataset,country,mod_sird,gmsird
from covid.stat import *
from covid.functions import *
from numpy import random
import numpy as np
import pygtc, configparser, json, sys
import matplotlib.pyplot as plt
import covid.dataset as ds

def main(file_name):

	# import parameter from configuration file
	#param = import_parameters(file_name)
	param = import_parameters('gmsird.ini')

	# reading dataset
	df = read_dataset(update_data = param['data_update'],
                	  url         = param['data_url'] ,
                      local_dataset_filename = param['data_filename'])

	# getting country information
	brasil_df = country(name       = param['country_1'][0],
		                population = param['country_1'][1]
		                )
	brasil_df.dataset(df,rescaling_by=1/param['scl_factor'])

	# defining statistical model
	StatModel = stat_model(brasil_df,
	                       gmsird,#mod_sird,
	                       param['par_est'],
	                       rescaling_by = 1/param['scl_factor'],
	                       par_labels   = param['par_labels']
	                       )
	#print(StatModel.log_prob(param['par_est']))

	# generating a mcmc sample by metropolis-hastings algorithm
	if param['generate_mcmc']:
		StatModel.metropolis_hastings(n_points  = param['sample_length'],
		                              par_stp   = param['par_stp'],
		                              overwrite = param['overwrite_file'],
		                              file_name = param['mcmc_file_name']
		                              )

	# import mcmc sample
	StatModel.import_sample(file_name = param['mcmc_file_name'],
                        	filter_outliers = True)

	# evaluating estimates for parameters
	SingleParameterEstimates = StatModel.single_parameter_estimates(alpha=0.3173)


	if param['ep_par_prop']:
			StatModel.evaluate_epidemiological_parameters(
									overwrite = param['ep_par_overwrite'],
									file_name = param['ep_file_name'],
									sample    = param['ep_par_sample']
	                                )


	# generating GTC plot
	if param['gtc_plot']:
		StatModel.gtc_plot(save_figure=True,show=False)

	# plotting curves
	if param['ep_plot_curves']:
		StatModel.plot_curves(SingleParameterEstimates['Medians'].to_list(),
	                    save_figure = True,
	                    show        = False
	                    )


if __name__ == "__main__":
    main('None')

#	args = sys.argv;
#
#	if (len(sys.argv) != 2):
#		print('[Error]: You must pass a parameter file to '+str(args[0]))
#	else:
#		main(args[1])
#	print('[status]: Finished.')
