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
from covid.stat import stat_model
from tqdm import tqdm
from numpy import random
import numpy as np
import pygtc, configparser, json, sys
import matplotlib.pyplot as plt


def main(file_name):

	# reading config file
	config = configparser.ConfigParser()
	config.read(file_name)

	#import parameters
	scl_factor 		= json.loads(config.get("MODEL", "scl_factor"))
	par_labels 		= json.loads(config.get("MODEL", "par_labels"))
	par_est    		= json.loads(config.get("MODEL", "par_est"))
	par_stp    		= json.loads(config.get("MODEL", "par_stp"))
	data_url   		= json.loads(config.get("DATASET", "data_url"))
	country_1  		= json.loads(config.get("COUNTRY", "country_1"))
	mcmc_file_name 	= json.loads(config.get("MCMC", "file_name"))
	generate_mcmc 	= json.loads(config.get("MCMC", "generate_mcmc"))
	overwrite_file 	= json.loads(config.get("MCMC", "overwrite_file"))
	sample_length  	= json.loads(config.get("MCMC", "sample_length"))
	n_walkers		= json.loads(config.get("MCMC", "n_walkers"))
	fit_confirmed  	= json.loads(config.get("MCMC", "fit_confirmed"))
	fit_death      	= json.loads(config.get("MCMC", "fit_death"))
	fit_recovered  	= json.loads(config.get("MCMC", "fit_recovered"))


	# dimension of parametric space
	par_dim = len(par_labels)

	# read dataset
	print('[info]: Downloading dataset from source.\n')
	df = read_dataset(data_url,url=True)

	# choosing a country
	brasil_df = country(name = country_1[0], population = country_1[1])
	brasil_df.dataset(df,rescaling_by=1/scl_factor)



	# defining statistical model
	print('[info]: Defining statistical model.\n')
	StatModel = stat_model(brasil_df,
	                       mod_sird,
	                       par_est,
	                       rescaling_by = 1/scl_factor,
	                       par_labels   = par_labels
	                       )
	#StatModel.data_model_plot(par_est)


	# generating a mcmc sample by metropolis-hastings algorithm
	if generate_mcmc:
		print('[info]: Generating a mcmc sample by metropolis-hastings algorithm.\n')
		StatModel.metropolis_hastings(n_points  = sample_length,
		                              par_stp   = par_stp,
		                              overwrite = overwrite_file,
		                              file_name = mcmc_file_name
		                              )
	
	'''
	print('[info]: Reading mcmc sample.\n')	
	StatModel.import_sample(file_name = mcmc_file_name)
	SingleParameterEstimates = StatModel.single_parameter_estimates(alpha=0.3173)
	GTCPlot = StatModel.gtc_plot()
	#print(SingleParameterEstimates)




	print('[info]: Generating a confidence region for the curves.\n')
	TEND = 365;
	ALPHA = 0.02;
	    
	# Raw Estimated Parameters
	par_est = SingleParameterEstimates[:,1]

	# Solving Equations
	x0 = [10**(par_est[-1]),1/scl_factor,0,0]


	msird_av = mod_sird(par_est, x0,TEND)
	msird_av.solve()

	t = msird_av.days_list

	# Confirmed Cases Plot
	c_model = msird_av.confirmed_list
	plt.plot(t,c_model,color='#27408B', label='Confirmed',zorder=10)
	plt.scatter(brasil_df.days_list,brasil_df.confirmed_list, color='#03254c',s=9,zorder=13)


	# Recovered Cases Plot
	r_model = msird_av.recovered_list
	plt.plot(t,r_model,color='#008B45', label='Recovered',zorder=10)
	plt.scatter(brasil_df.days_list,brasil_df.recovered_list, color='#1e663b',alpha=1.,s=9,zorder=12)

	# Death Cases Plot
	d_model = msird_av.death_list
	plt.plot(t,d_model,color='#EE7621', label='Deaths',zorder=10)
	plt.scatter(brasil_df.days_list,brasil_df.death_list, color='#FF7F24',alpha=1.,s=9,zorder=11)


	final_deaths = []
	final_cases  = []

	for index in tqdm(list(random.choice(range(len(StatModel.sample)),500))):
	    
	    par_rdn = StatModel.sample[index]
	    

	    # Solving Equations
	    x0 = [10**(par_rdn[-1]),1/scl_factor,0,0]
	    msird_av = mod_sird(par_rdn, x0,TEND)
	    msird_av.solve()
	    
	    t = msird_av.days_list
	    
	    # Confirmed Cases Plot
	    c_model = msird_av.confirmed_list
	    plt.plot(t,c_model,color='#87CEFA',  alpha=ALPHA, linewidth=3)
	    
	    # Recovered Cases Plot
	    r_model = msird_av.recovered_list
	    plt.plot(t,r_model,color='#98e0b5',alpha=ALPHA, linewidth=3)
	    
	    # Death Cases Plot
	    d_model = msird_av.death_list
	    plt.plot(t,d_model,color='#FFDAB9', alpha=ALPHA, linewidth=3)
	    
	    final_cases.append(np.interp(TEND, t, c_model))
	    final_deaths.append(np.interp(TEND, t, d_model))
	    


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
		print('Error. You must pass a parameter file to '+str(args[0]))
	else:
		main(args[1])