#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 12 02:35:02 2020

@author: eduardo
"""

import numpy as np
from scipy.integrate import odeint

class mod_sird:
    
    def __init__(self,par,x0,tend,tbeg=0,npoints=100):
        
        self.par = par
        self.x0 = x0
        self.tbeg = tbeg
        self.tend = tend
        self.npoints = npoints
        self.solve()

    def diff_eq(self,x,t,par):
        
        s = x[0]
        i = x[1]
        r = x[2]
        d = x[3]
    
        DiffS = -par[1]*(s/10**par[4])*(i**par[0])
        DiffI = (par[1]*(s/10**par[4]) - par[2] - par[3])*(i**par[0])
        DiffR = par[2]*(i**par[0])
        DiffD = par[3]*(i**par[0])
        
        return [DiffS,DiffI,DiffR,DiffD]
    
    def solve(self):
        '''
        Importante notar que (par_est,) é uma tupla de apenas um elemento.
        Caso pusessemos (par_est), os parenteses não indicariam uma tupla
        '''
        self.days_list = np.linspace(self.tbeg,self.tend,self.npoints)
        self.x = odeint(self.diff_eq,self.x0,self.days_list,args = (self.par,))
        
        self.confirmed_list = self.x[:,1] + self.x[:,2] + self.x[:,3]
        self.recovered_list = self.x[:,2]
        self.death_list = self.x[:,3]
    
            