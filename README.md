
# Prediction for the spread of COVID-19 using Epidemiological Models

### Table of Contents
1. [Getting Started](#1-getting-started)
2. [Features](#2-features)
3. [Installation](#3-installation)
4. [Model](#4-model)
5. [Dataset](#5-dataset)



## 1. Getting Started
#### Dependencies
You need Python 3.7 or later to use **pacotepypi**. You can find it at [python.org](https://www.python.org/).
You also need setuptools, wheel and twine packages, which is available from [PyPI](https://pypi.org). If you have pip, just run:
```
pip install setuptools
pip install tqdm
pip install pygtc
```
#### Installation
Clone this repo to your local machine using:
```
git clone https://github.com/emdemor/modelling-sars-covid19
```
## 2. Features
- File structure for PyPI packages
- Setup with package informations
- License example

## 3. Model

Many research teams seek to find an epidemiological model that can describe the spread of SARS-CoV-2. Many gaps in knowledge about the biology of the virus, the difference in social patterns and public policies by countries around the world combined with the many testing approaches causes that the breadth and shape of infection curves do not assume a global behavioral pattern.

If, on the one hand, it is difficult to say precisely which is the best theory, on the other, it is a fact that the direction of public policies depends on future projections of the data observed until then, by applying minimally satisfactory models. This condition motivates researchers to formulate increasingly more intricate models that, although not applicable to all countries of the globe, are quite credible locally. In general, they have a large number of free parameters and differential equations, which makes them inaccessible outside the professional environment.

In this work, a toy model is presented to describe Covid infection data in Brazil during the months of February 2020 until the first week of June 2020. This is based on a SIRD model, with the addition of a parameter for enable its compatibility with the data. This model describes the interaction of four time functions S(t), I(t), R(t) and D(t) that counts the susceptible, active infected, recovered and dead individuals in a specific population. The differential equations are:

<p align="center">
  <img src="https://latex.codecogs.com/svg.latex?%5Clarge%20%5Cbegin%7Bcases%7D%20%5Cfrac%7BdS%7D%7Bdt%7D%20%26%20%3D-%5Cfrac%7B%5Cbeta%7D%7Bs_%7B0%7D%7DS%5Cleft%28t%5Cright%29I%5Cleft%28t%5Cright%29%5E%7B%5Calpha%7D%5C%5C%20%5Cfrac%7BdI%7D%7Bdt%7D%20%26%20%3D%5Cleft%28%5Cfrac%7B%5Cbeta%7D%7Bs_%7B0%7D%7DS%5Cleft%28t%5Cright%29-%5Crho-%5Cdelta%5Cright%29I%5Cleft%28t%5Cright%29%5E%7B%5Calpha%7D%5C%5C%20%5Cfrac%7BdR%7D%7Bdt%7D%20%26%20%3D%5Crho%20I%5Cleft%28t%5Cright%29%5E%7B%5Calpha%7D%5C%5C%20%5Cfrac%7BdD%7D%7Bdt%7D%20%26%20%3D%5Cdelta%20I%5Cleft%28t%5Cright%29%5E%7B%5Calpha%7D%20%5Cend%7Bcases%7D"/>
</p>


This equations must be integrated with inicial conditions given by: s(0)=s_0 , I(0)=1 and R(0)=D(0)=0. The time variable t is defined as the time after first confirmed case. The model have five free parameters (\alpha,\beta,\rho,\delta,s_0), where s_0 is the initial susceptible individuals. Inthe case where \alpha=1, the SIRD model is recovered. As s_0, in general, assumes very large values, lets consider its log value. In this way, the parameters are $(\alpha,\beta,\rho,\delta,\log_{10}s_0).



## 4. Results

The main result in this version is to plot de curves from the model for a specific parameter vector and compare this with dataset. In covid/stat.py, functions has been implemented to generate an MCMC sample, through which it will be possible to make inferences of the parametric intervals.

<p align="center">
  <img src="./results/brazil/cases_projection.png" alt="brazil-cases" />
</p>
<p align="center">
  <img src="./results/india/cases_projection.png" alt="india-cases" />
</p>
<p align="center">
  <img src="./results/russia/cases_projection.png" alt="russia-cases" />
</p>


### 5. Dataset

Here, we are using the Microsoft Data, from the repo https://github.com/microsoft/Bing-COVID-19-Data. 
]