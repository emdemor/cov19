
# Prediction for the spread of COVID-19 using Epidemiological Models
The purpose of the cov19 package is to integrate the differential equations of epidemiological models and adjust their respective parameters with data using MCMC approach.


### Table of Contents
1. [Getting Started](#1-getting-started)
2. [Features](#2-features)
3. [Results](#3-results)
4. [Dataset](#4-dataset)



## 1. Getting Started
#### Dependencies
You need Python 3.7 or later to use **cov19**. You can find it at [python.org](https://www.python.org/).
You also need setuptools, wheel and twine packages, which is available from [PyPI](https://pypi.org). If you have pip, just run:
```
pip install pandas
pip install pygtc
pip install setuptools
pip install tqdm
```
#### Installation
Clone this repo to your local machine using:
```
git clone https://github.com/emdemor/cov19
```
## 2. Features
- Support for different epidemiological models
- Monte Carlo Markov Chains (MCMC) approach to fit patameters
- Data from multiple trusted and reliable sources compiled by Microsoft and accessible in www.bing.com/covid.

## 3. Results

The main result in this version is to plot de curves from the model for a specific parameter vector and compare this with dataset. In covid/stat.py, functions has been implemented to generate an MCMC sample, through which it will be possible to make inferences of the parametric intervals.

<p align="center">
  <img src="https://raw.githubusercontent.com/emdemor/cov19/master/results/brazil/cases_projection.png" alt="brazil-cases" />
</p>
<p align="center">
  <img src="https://raw.githubusercontent.com/emdemor/cov19/master/results/india/cases_projection.png" alt="india-cases" />
</p>
<p align="center">
  <img src="https://raw.githubusercontent.com/emdemor/cov19/master/results/russia/cases_projection.png" alt="russia-cases" />
</p>


### 4. Dataset

Here, we are using the Microsoft Data, from the repo https://github.com/microsoft/Bing-COVID-19-Data. 
]