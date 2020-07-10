#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Description
----------
This module gives functions and classes to manipulate epidemiolgical models

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

import numpy as np
from scipy.integrate import odeint


class mod_sird:
    '''
    Description
    ----------
    This class defines a epidemiological model to explained the total, 
    recovered, active infected and deaths cases of the COVID pandemic desease 
    in a specific country.
    
    Its equations descrive the relations between the 4 functions s,i,r and d 
    describing respectively the number of susceptible, active infected, 
    recovered and dead individual
    
    The diference bewtween Modified SIRD and the usual SIRD model is in the 
    presence of an aditional parameters alpha as a power on i(t) in 
    differential equations 
    
    
    Arguments
    ----------
        par: numpy.array
            Specific values for parameters
            
        x0: numpy.array
            Initial conditions for variables to be integrated
            
        tend: float
            Last value of time
            
        tbeg: float (optional)
            First value of time
            
        tend: float
            Last value of time
            
        npoints: int
            Number of interpolated points evaluated by model
            
        
    Parameters
    ----------
        self.par: numpy.array
            Specific values for parameters

        self.x0: numpy.array
            Initial conditions for variables to be integrated

        self.tbeg: float (optional)
            First value of time 

        self.tend:  float
            Last value of time

        self.npoints: int
            Number of interpolated points evaluated by model

        self.x: numpy.array
            Array with 4 columns and n lines containing the susceptible,
            active infected, recovered and death functions evaluated in
            time.
        
        self.days_list:
            Array with  n lines containing the time values
        
        self.confirmed_list:
            Array with  n lines containing the evaluated confirmed cases

        self.recovered_list:
            Array with  n lines containing the evaluated recovered cases

        self.death_list:
            Array with  n lines containing the evaluated deaths cases
        
    '''
    
    def __init__(self,
                 par,
                 x0,
                 tend,
                 tbeg=0,
                 npoints=100
                 ):
        
        self.par = par
        self.x0 = x0
        self.tbeg = tbeg
        self.tend = tend
        self.npoints = npoints
        self.name = "MSIRD"
        self.solve()




    def diff_eq(self,x,t,par):
        
        """
        Function resturning the differential equations of the model

        Arguments
        ----------
        x: numpy.array
            Array with 4 columns and n lines containing the susceptible,
            active infected, recovered and death functions evaluated in
            time.
            
        t: float
            Time value where the equations will be avaluated
            
        par: numpy.array
            Specific values for parameters
            
        Parameters
        ----------
        void
        
        Returns
        -------
        : list
            Differential equations evaluated for the parameters an time
            passed by user
        
        """
        
        # setting the functions
        s = x[0]
        i = x[1]
        r = x[2]
        d = x[3]
    
        # mathematical equations
        DiffS = -par[1]*(s/10**par[4])*(i**par[0])
        DiffI = (par[1]*(s/10**par[4]) - par[2] - par[3])*(i**par[0])
        DiffR = par[2]*(i**par[0])
        DiffD = par[3]*(i**par[0])
        
        return [DiffS,DiffI,DiffR,DiffD]
    



    def solve(self,
              notifications = False
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

        if notifications:
            print('[info]: Solving differential equations for '+self.name+' model. ')
            

        
        # getting the time values
        self.days_list = np.linspace(self.tbeg,self.tend,self.npoints)

        # calling the odeint method to solve the diff. equations
        self.x = odeint(self.diff_eq,self.x0,self.days_list,args = (self.par,))
        '''
        Its important to note that (par_est,) is the way to define a tuple
        with just one element. When we put (par_est), the  parenteses won't
        indicate a tuple
        '''
        
        #setting the variables
        self.confirmed_list = self.x[:,1] + self.x[:,2] + self.x[:,3]
        self.recovered_list = self.x[:,2]
        self.death_list = self.x[:,3]
    
            

class gmsird:
    '''
    Description
    ----------

    Arguments
    ----------
        par: numpy.array
            Specific values for parameters
            
        x0: numpy.array
            Initial conditions for variables to be integrated
            
        tend: float
            Last value of time
            
        tbeg: float (optional)
            First value of time
            
        tend: float
            Last value of time
            
        npoints: int
            Number of interpolated points evaluated by model
            
        
    Parameters
    ----------
        self.par: numpy.array
            Specific values for parameters

        self.x0: numpy.array
            Initial conditions for variables to be integrated

        self.tbeg: float (optional)
            First value of time 

        self.tend:  float
            Last value of time

        self.npoints: int
            Number of interpolated points evaluated by model

        self.x: numpy.array
            Array with 4 columns and n lines containing the susceptible,
            active infected, recovered and death functions evaluated in
            time.
        
        self.days_list:
            Array with  n lines containing the time values
        
        self.confirmed_list:
            Array with  n lines containing the evaluated confirmed cases

        self.recovered_list:
            Array with  n lines containing the evaluated recovered cases

        self.death_list:
            Array with  n lines containing the evaluated deaths cases
        
    '''
    
    def __init__(self,
                 par,
                 x0,
                 tend,
                 tbeg=0,
                 npoints=100
                 ):
        
        self.par = par
        self.x0 = x0
        self.tbeg = tbeg
        self.tend = tend
        self.npoints = npoints
        self.name = "MSIRD"
        self.solve()




    def diff_eq(self,x,t,par):
        
        """
        Function resturning the differential equations of the model

        Arguments
        ----------
        x: numpy.array
            Array with 4 columns and n lines containing the susceptible,
            active infected, recovered and death functions evaluated in
            time.
            
        t: float
            Time value where the equations will be avaluated
            
        par: numpy.array
            Specific values for parameters
            
        Parameters
        ----------
        void
        
        Returns
        -------
        : list
            Differential equations evaluated for the parameters an time
            passed by user
        
        """
        
        # setting the functions
        s, i, r, d = x

        n = len(par)-1
        # a_s = 0.85
        a_s, v, b, c, d = par[:n]
        v = v/1000
        a_r = a_s
        a_d = a_s
        s0 = 10**par[-1]
    
        # mathematical equations
        DiffS = -b*(s/s0)*(i**a_s)
        DiffI = b*(s/s0)*(i**a_s) - c*(i**(a_s+v*t)) - d*(i**(a_s+v*t))
        DiffR = c*(i**(a_s+v*t))
        DiffD = d*(i**(a_s+v*t))
        
        return [DiffS,DiffI,DiffR,DiffD]
    



    def solve(self,
              notifications = False
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

        if notifications:
            print('[info]: Solving differential equations for '+self.name+' model. ')
            

        
        # getting the time values
        self.days_list = np.linspace(self.tbeg,self.tend,self.npoints)

        # calling the odeint method to solve the diff. equations
        self.x = odeint(self.diff_eq,self.x0,self.days_list,args = (self.par,))
        '''
        Its important to note that (par_est,) is the way to define a tuple
        with just one element. When we put (par_est), the  parenteses won't
        indicate a tuple
        '''
        
        #setting the variables
        self.confirmed_list = self.x[:,1] + self.x[:,2] + self.x[:,3]
        self.recovered_list = self.x[:,2]
        self.death_list = self.x[:,3]
    

class gen_sird:
    '''
    Description
    ----------
    
    Arguments
    ----------
        par: numpy.array
            Specific values for parameters
            
        x0: numpy.array
            Initial conditions for variables to be integrated
            
        tend: float
            Last value of time
            
        tbeg: float (optional)
            First value of time
            
        tend: float
            Last value of time
            
        npoints: int
            Number of interpolated points evaluated by model
            
        
    Parameters
    ----------
        self.par: numpy.array
            Specific values for parameters

        self.x0: numpy.array
            Initial conditions for variables to be integrated

        self.tbeg: float (optional)
            First value of time 

        self.tend:  float
            Last value of time

        self.npoints: int
            Number of interpolated points evaluated by model

        self.x: numpy.array
            Array with 4 columns and n lines containing the susceptible,
            active infected, recovered and death functions evaluated in
            time.
        
        self.days_list:
            Array with  n lines containing the time values
        
        self.confirmed_list:
            Array with  n lines containing the evaluated confirmed cases

        self.recovered_list:
            Array with  n lines containing the evaluated recovered cases

        self.death_list:
            Array with  n lines containing the evaluated deaths cases
        
    '''
    
    def __init__(self,par,x0,tend,tbeg=0,npoints=100):
        
        self.par = par
        self.x0 = x0
        self.tbeg = tbeg
        self.tend = tend
        self.npoints = npoints
        self.solve()




    def diff_eq(self,x,t,par):
        
        """
        Function resturning the differential equations of the model

        Arguments
        ----------
        x: numpy.array
            Array with 4 columns and n lines containing the susceptible,
            active infected, recovered and death functions evaluated in
            time.
            
        t: float
            Time value where the equations will be avaluated
            
        par: numpy.array
            Specific values for parameters
            
        Parameters
        ----------
        void
        
        Returns
        -------
        : list
            Differential equations evaluated for the parameters an time
            passed by user
        
        """
        
        # setting the functions
        s = x[0]
        i = x[1]
        r = x[2]
        d = x[3]

        n = len(par)-1
        # a_s = 0.85
        a_s, a_r, a_d, b, c, d = par[:n]

        s0 = 10**par[-1]
    
        # mathematical equations
        DiffS = -b*(s/s0)*(i**a_s)
        DiffI = b*(s/s0)*(i**a_s) - c*(i**a_r) - d*(i**a_d)
        DiffR = c*(i**a_r)
        DiffD = d*(i**a_d)
        
        return [DiffS,DiffI,DiffR,DiffD]
    



    def solve(self):
        
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
        
        # getting the time values
        self.days_list = np.linspace(self.tbeg,self.tend,self.npoints)

        # calling the odeint method to solve the diff. equations
        self.x = odeint(self.diff_eq,self.x0,self.days_list,args = (self.par,))
        '''
        Its important to note that (par_est,) is the way to define a tuple
        with just ode element. When we put (par_est), the  parenteses won't
        indicate a typle
        '''
        
        #setting the variables
        self.confirmed_list = self.x[:,1] + self.x[:,2] + self.x[:,3]
        self.recovered_list = self.x[:,2]
        self.death_list = self.x[:,3]
    
            