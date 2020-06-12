#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 12 02:35:02 2020

@author: eduardo
"""


from covid import read_dataset,country,mod_sird


scl_factor = 1000;
par_est = [0.8244, 0.2656, 0.1029, 0.0149,3.66]

df = read_dataset('Bing-COVID19-Data.csv')
#df = read_dataset('https://raw.githubusercontent.com/microsoft/Bing-COVID-19-Data/master/data/Bing-COVID19-Data.csv',url=True)

my_country = country(name = "Brazil", population = 212000000)
my_country.dataset(df,rescaling_by=1/scl_factor)


model = mod_sird(
    par = par_est,
    x0 = [10**(par_est[-1]),1/scl_factor,0,0],
    tend = 105
    )

print(model.x)
