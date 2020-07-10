#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Description
----------
This module gives functions and classes to manipulate the global statistical
properties of the model

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

import random,pygtc
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time

from tqdm       import tqdm
from .functions import distribute_among_walkers, riffle
from scipy      import stats
from os         import path
from numpy      import random


#__RESULTS_DIR__       =  path.join('cov19', '_results')
__ESTIMATE_OUT_FILE__ = 'sigle-parameter-estimates.csv'
__GTC_OUT_FILE__      = 'gtc-graphs.png'
__CRD_OUT_FILE__      = 'crd-curve.png'
__CURVES_PROJ_FILE__  = 'cases_projection.png'
__EP_PARAMETES_FILE__ = 'epidemiological_par.csv'
__TEND__              = 365

class stat_model:
    '''
    Description
    ----------
    The stat_model manipulates the global statistical parameters of the model

    Arguments
    ----------
    dataframe: country.dataframe
        A pandas dataframe with cov19 cases in the specific country

    ep_model:
        Details about the epidemiological model. Models mus bet implemented
        in the models.py module.

    par_labels: list (optional)
        A list of strings labeling the model parameters. If the user choose
        not to pass this, the code must treat it as ['p1',...,'pn'].

    par_est: numpy.array
        Raw estimates to the model parameter's values

    par_min: numpy.array (optional)
        Raw estimates to the model parameter's values

    par_max: numpy.array (optional)
        Raw estimates to the model parameter's values

    rescaling: float (optional)
        factor to reescaling the number of cases

    tend: float (optional)
        The maximum value of time. If the user choose not pass it, the code
        will get the last time from the dataset

    Parameters
    ----------

    self.dataframe: pandas.DataFrame
        Internal DataFrame object with data about covid cases.

    self.ep_model:
        Internal variable with the epidemiological model.

    '''

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

        print('[info]: Defining statistical model.')
        self.dataframe = dataframe
        self.ep_model = ep_model
        self.par_est = par_est
        self.rescale = rescaling_by
        self.sample = []
        self.n = 0

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

        """
        Call the solve method from epidemiological model object e returns it
        updated.

        Arguments
        ----------
        par: numpy.array
            Specific values for parameters

        x0: numpy.array
            Initial conditions for variables to be integrated

        tend: float
            Last value of time

        Parameters
        ----------
        void

        Returns
        -------
        ep_model

        """
        return self.ep_model(par = parameters, x0 = [10**(parameters[-1]),self.rescale,0,0],tend=self.tend)




    def chi_sqrd(self,
                 par,
                 fit_recovered = True,
                 fit_death = True,
                 fit_confirmed = True
                 ):

        """
        Evaluate the chi squared for a parametrical configuration

        Arguments
        ----------
        par: numpy.array
            Specific values for parameters

        fit_confirmed: boolean
            Controls of the chi squared will consider the confirmed cases

        fit_recovered : boolean
            Controls of the chi squared will consider the recovered cases

        fit_death: boolean
            Controls of the chi squared will consider the deaths cases


        Returns
        -------
        Chi2: float
            Value of chi squared

        """

        # model
        model = self.solve(par)
        t_model = model.days_list
        c_model = model.confirmed_list
        r_model = model.recovered_list
        d_model = model.death_list

        #dataset
        t_data = self.dataframe.days_list
        c_data = self.dataframe.confirmed_list
        r_data = self.dataframe.recovered_list
        d_data = self.dataframe.death_list

        # chi2 function
        chi2 = lambda model, data: (model-data)**2

        # stating chi2
        Chi2 = 0;

        # summing confirmed part
        if fit_confirmed:
            Chi2 += sum(list(map(chi2, list(np.interp(t_data, t_model, c_model)), c_data)))

        # summing recovered part
        if fit_recovered:
            Chi2 += sum(list(map(chi2, list(np.interp(t_data, t_model, r_model)), r_data)))

        # summing death part
        if fit_death:
            Chi2 += sum(list(map(chi2, list(np.interp(t_data, t_model, d_model)), d_data)))

        return Chi2




    def log_prob(self,
                 par,
                 fit_recovered = True,
                 fit_death = True,
                 fit_confirmed = True
                 ):
        """
        Evaluate the log o probability

        Arguments
        ----------
        par: numpy.array
            Specific values for parameters

        fit_confirmed: boolean
            Controls of the chi squared will consider the confirmed cases

        fit_recovered : boolean
            Controls of the chi squared will consider the recovered cases

        fit_death: boolean
            Controls of the chi squared will consider the deaths cases


        Returns
        -------
        ln: float
            Value of log P

        """

        lnP = - 0.5 * self.chi_sqrd(par,
                                    fit_recovered = fit_recovered,
                                    fit_death = fit_death,
                                    fit_confirmed = fit_confirmed
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
                            fit_confirmed = True
                            ):
        """
        Generate a MCMC sample through metropolis hasting algorithm and
        save it in a specified file

        Arguments
        ----------
        n_points: int
            Sample length

        par_stp: numpy.array
            The maximum displacement a walker can take at each step

        file_name: str
            A string containing the name of the file where the code will
            append values.

        overwrite: bool
            Variable passed by user controling if old files will be appended
            or overwritten

        n_walkers: int
            Number of random walkers

        fit_confirmed: boolean
            Controls of the chi squared will consider the confirmed cases

        fit_recovered : boolean
            Controls of the chi squared will consider the recovered cases

        fit_death: boolean
            Controls of the chi squared will consider the deaths cases

        Returns
        -------
        void

        """

        print('[info]: Generating a mcmc sample by metropolis-hastings algorithm.')
        time.sleep(1)

        # distributing the points to walkers
        n_walkers_list = distribute_among_walkers(n_points,n_walkers)

        # changing to tables directory
        #set_directory(tables_directory)

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
                                    fit_confirmed = fit_confirmed)

            # looping through the walker amount of points
            for n in tqdm(range(n_walkers_list[ind_walker]),desc='[wlkr'+str(1+ind_walker)+']: '):

                # suggest new candidate from uniform distribution
                PAR_NEW  = list(map(lambda p,h: p + random.uniform(-1, 1)*h ,np.array(PAR),np.array(par_stp)))
                log_PROB_NEW = self.log_prob(PAR_NEW,
                                    fit_recovered = fit_recovered,
                                    fit_death = fit_death,
                                    fit_confirmed = fit_confirmed)

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

        # # updating mcmc_sample variable
        self.mcmc_sample = True




    def import_sample(self,
    	              file_name="mcmc.csv",
    				  filter_outliers = False
    				  ):

        """
        This method imports the file where the sample was saved

        Arguments
        ----------
        file_name: str
            A string containing the name of the file where the code will
            append values.

        Returns
        -------
        :pandas.DataFrame.info()
            Information about the sample imported
        """

        print('[info]: Reading mcmc sample file.')

        # setting tables directory
        #set_directory(tables_directory)

        #importing
        self.raw_sample_df = pd.read_csv(file_name,sep="\t")
        self.raw_sample = self.raw_sample_df.to_numpy()

        # Filtering outliers (WRONG)
        if filter_outliers:

            DIC = self.raw_sample_df.quantile(0.75)-self.raw_sample_df.quantile(0.25)
            beg = self.raw_sample_df.quantile(0.25)-1.75*DIC
            end = self.raw_sample_df.quantile(0.75)+1.75*DIC
            conditions = True
            for lab in self.par_labels:
            	conditions &= self.raw_sample_df[lab].between(beg[lab],end[lab])

            self.sample_df = self.raw_sample_df[conditions]
            self.sample = self.sample_df.to_numpy()
        else:
            self.sample_df = self.raw_sample_df
            self.sample = self.sample_df.to_numpy()


        # updating sample_imported
        self.sample_imported = True

        # number of data
        self.n = len(self.sample_df)


    def data_model_plot(self,par):

        """
        This method plots a graphics comparing the dataset with the curves
        related to the model evaluated with the parameters passed by user

        Arguments
        ----------
        par: numpy.array
            Array containig a specific parametric configuration

        Returns
        -------
        void

        """
        print('[info]: Ploting epidemiological model curves with dataset.')
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
        plt.savefig(__CRD_OUT_FILE__)
        plt.show()




    def single_parameter_estimates(self,alpha=0.3173,est_outfile = __ESTIMATE_OUT_FILE__):

        """
        Returns the interval with confidence alpha.

        Arguments
        ----------
        alpha: float
            Confidence level of interval estimate

        Returns
        -------
        void

        """

        # check if user imported a sample
        if not self.sample_imported:
            print('[error]: you must read a mcmc sample file first.')
            return []

        else:
            print('[info]: Evaluating statistical properties of sample.')
            var = 100*alpha/2

            med = self.raw_sample_df.mean()

            interval = np.array(list(map(lambda index: np.percentile(self.raw_sample[:, index], [50,var, 100-var]),list(range(self.ndim)))))
            df_results = pd.DataFrame({ 'Parameters':self.par_labels,
                                        'Mean': med,
                                        'Medians':interval[:,0],
                                        '1 sig interval min': interval[:,1],
                                        '1 sig interval max': interval[:,2]
                                      })

            df_results .to_csv(est_outfile,sep='\t',index=False)
            #var = list(map(lambda label, estim: label+str(estim[0]))
            self.estimates = df_results
            return df_results




    def gtc_plot(self,
                 truths=None,
                 n_contour_levels=2,
                 figure_size = 8,
                 custom_label_font = {'family':'DejaVu Sans', 'size':10},
                 custom_tick_font = {'family':'DejaVu Sans', 'size':8},
                 save_figure = False,
                 file_name = __GTC_OUT_FILE__,
                 show = True
            ):

        """
        This method plots graphics for each 2-dimensional marginal
        probability density and the 1-dimensional marginal probability
        related to the parameters

        Arguments
        ----------
        ...
        ...


        Returns
        -------
        ...
        ...

        """
        plt.close()
        GTC = pygtc.plotGTC(chains=[self.sample ],
                    truths = truths,
                    paramNames = self.par_labels,
                    nContourLevels = n_contour_levels,
                    figureSize = figure_size,
                    customLabelFont = custom_label_font,
                    customTickFont = custom_tick_font
                   )

        if save_figure:
            GTC.savefig(file_name)

        if show: plt.show()
        plt.close()
        
        return GTC




    def evaluate_epidemiological_parameters(self,
                                            tend = __TEND__,
                                            overwrite = True,
                                            file_name = __EP_PARAMETES_FILE__,
                                            sample = 0.1
                                            ):

        """
        This method gives parametric estimates to parameters

        Arguments
        ----------
        ...
        ...

        Returns
        -------
        ...
        ...

        """

        print('[info]: Generating confidence regions for epidemiological curves.')

        # checking if user want all sample or just a part
        if (type(sample) == int) and (0 < sample < len(self.sample)):
            sample_list = [self.sample[index] for index in list(random.choice(range(len(self.sample)),sample))]

        elif (type(sample) == float) and (0. < sample <= 1.0):
            sample = int(sample*round(len(self.sample)))
            sample_list = [self.sample[index] for index in list(random.choice(range(len(self.sample)),sample))]
        else:
            sample_list = self.sample

        # updating sample_imported
        if not self.sample_imported:
            print('[error]: You need to generate and import a sample.')

        else:

            # changing to tables folder
            #set_directory(tables_directory)

            # cleaning the old file
            if overwrite:
                open(file_name, 'w').close()

            # open a new file to append
            file = open(file_name, 'a')

            # writing the header
            if overwrite:
                PAR_LAB = self.par_labels + ['Confirmed','Deaths']
                file.write(''.join(riffle(PAR_LAB,'\t'))+'\n')

            # loop through the sample parameters
            for par in tqdm(sample_list,desc='[wlkr1]: '):

                # initial conditions
                x0 = [10**(par[-1]),self.rescale,0,0]

                #solving equations
                msird_av = self.ep_model(par, x0,tend)
                msird_av.solve()

                # time list
                t = msird_av.days_list

                # Confirmed Cases Plot
                c_model = msird_av.confirmed_list

                # Recovered Cases Plot
                r_model = msird_av.recovered_list

                # Death Cases Plot
                d_model = msird_av.death_list

                PAR = np.concatenate((par, np.array([np.interp(tend, t, c_model),np.interp(tend, t, d_model)])))

                # writing on file
                file.write(''.join(riffle(list(map(str,PAR)),'\t'))+'\n')

            file.close()




    def plot_curves(self,
    				par_est,
                    tend  = __TEND__,
                    alpha = 0.02,
                    show = True,
                    save_figure = True,
                    file_name = __CURVES_PROJ_FILE__,
                    plot_title = ''
                    ):

        """
        This method gives parametric estimates to parameters

        Arguments
        ----------
        ...
        ...

        Returns
        -------
        ...
        ...

        """

        print('[info]: Plotting curves.')
        plt.close()

        # Solving Equations
        x0 = [10**(par_est[-1]),self.rescale,0,0]
        model = self.ep_model(par_est, x0,tend)
        model.solve()

        # Time list
        t = model.days_list

        #Confirmed Cases Plot
        c_model = model.confirmed_list
        plt.plot(t,c_model,color='#27408B', label='Confirmed',zorder=10)
        plt.scatter(self.dataframe.days_list,
                    self.dataframe.confirmed_list,
                    color='#03254c',
                    s=9,
                    zorder=13)

        # Recovered Cases Plot
        r_model = model.recovered_list
        plt.plot(t,r_model,color='#008B45', label='Recovered',zorder=10)
        plt.scatter(self.dataframe.days_list,
                    self.dataframe.recovered_list,
                    color='#1e663b',
                    alpha=1.,
                    s=9,
                    zorder=12)

        # Death Cases Plot
        d_model = model.death_list
        plt.plot(t,d_model,color='#EE7621', label='Deaths',zorder=10)
        plt.scatter(self.dataframe.days_list,self.dataframe.death_list, color='#FF7F24',alpha=1.,s=9,zorder=11)

        #plt.show()
        final_deaths = []
        final_cases  = []

        for index in tqdm(list(random.choice(range(len(self.sample)),500)),desc='[wlkr1]: '):

            par_rdn = self.sample[index]
            # Solving Equations
            x0 = [10**(par_rdn[-1]),self.rescale,0,0]
            model = self.ep_model(par_rdn, x0,tend)
            model.solve()
            t = model.days_list

            # Confirmed Cases Plot
            c_model = model.confirmed_list
            plt.plot(t,c_model,color='#87CEFA',  alpha=alpha, linewidth=3)

            # Recovered Cases Plot
            r_model = model.recovered_list
            plt.plot(t,r_model,color='#98e0b5',alpha=alpha, linewidth=3)

            # Death Cases Plot
            d_model = model.death_list
            plt.plot(t,d_model,color='#FFDAB9', alpha=alpha, linewidth=3)

        plt.title(plot_title)
        plt.legend(loc="upper left")
        plt.xlabel('days after first case')
        plt.ylabel('number of people [✕'+str(int(1/self.rescale))+']')
        plt.grid()
        if save_figure:
            plt.savefig(file_name)
        if show: plt.show()
        plt.close()
