
# rAthena
[![Build Status](https://travis-ci.org/rathena/rathena.png?branch=master)](https://travis-ci.org/rathena/rathena) 
[![Build status](https://ci.appveyor.com/api/projects/status/8574b8nlwd57loda/branch/master?svg=true)](https://ci.appveyor.com/project/rAthenaAPI/rathena/branch/master) [![Total alerts](https://img.shields.io/lgtm/alerts/g/rathena/rathena.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/rathena/rathena/alerts/) [![Language grade: C/C++](https://img.shields.io/lgtm/grade/cpp/g/rathena/rathena.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/rathena/rathena/context:cpp) ![GitHub](https://img.shields.io/github/license/rathena/rathena.svg) ![GitHub repo size](https://img.shields.io/github/repo-size/rathena/rathena.svg)
> rAthena is a collaborative software development project revolving around the creation of a robust massively multiplayer online role playing game (MMORPG) server package. Written in C, the program is very versatile and provides NPCs, warps and modifications. The project is jointly managed by a group of volunteers located around the world as well as a tremendous community providing QA and support. rAthena is a continuation of the eAthena project.

[Forum](https://rathena.org/board)|[Discord](https://rathena.org/discord)|[Wiki](https://github.com/rathena/rathena/wiki)|[FluxCP](https://github.com/rathena/FluxCP)|[Crowdfunding](https://rathena.org/board/crowdfunding/)|[Fork and Pull Request Q&A](https://rathena.org/board/topic/86913-pull-request-qa/)
--------|--------|--------|--------|--------|--------

### Table of Contents
1. [Prerequisites](#1-prerequisites)
2. [Installation](#2-installation)
3. [Troubleshooting](#3-troubleshooting)
4. [More Documentation](#4-more-documentation)
5. [How to Contribute](#5-how-to-contribute)
6. [License](#6-license)

# Introduction

Many research teams seek to find an epidemiological model that can describe the spread of SARS-CoV-2. Many gaps in knowledge about the biology of the virus, the difference in social patterns and public policies by countries around the world combined with the many testing approaches causes that the breadth and shape of infection curves do not assume a global behavioral pattern.

If, on the one hand, it is difficult to say precisely which is the best theory, on the other, it is a fact that the direction of public policies depends on future projections of the data observed until then, by applying minimally satisfactory models. This condition motivates researchers to formulate increasingly more intricate models that, although not applicable to all countries of the globe, are quite credible locally. In general, they have a large number of free parameters and differential equations, which makes them inaccessible outside the professional environment.

In this work, a toy model is presented to describe Covid infection data in Brazil during the months of February 2020 until the first week of June 2020. This is based on a SIRD model, with the addition of a parameter for enable its compatibility with the data. This model describes the interaction of four time functions S(t), I(t), R(t) and D(t) that counts the susceptible, active infected, recovered and dead individuals in a specific population. The differential equations are:


![equation](https://latex.codecogs.com/gif.latex?%5Cbegin%7Bcases%7D%20%5Cfrac%7BdS%7D%7Bdt%7D%3D%20%26%20-%5Cfrac%7B%5Cbeta%7D%7Bs_%7B0%7D%7DS%5Cleft%28t%5Cright%29I%5Cleft%28t%5Cright%29%5E%7B%5Calpha%7D%5C%5C%20%5Cfrac%7BdI%7D%7Bdt%7D%3D%20%26%20%5Cleft%28%5Cfrac%7B%5Cbeta%7D%7Bs_%7B0%7D%7DS-%5Crho-%5Cdelta%5Cright%29i%5Cleft%28t%5Cright%29%5E%7B%5Calpha%7D%5C%5C%20%5Cfrac%7BdR%7D%7Bdt%7D%3D%20%26%20%5Crho%5C%2CI%5Cleft%28t%5Cright%29%5E%7B%5Calpha%7D%5C%5C%20%5Cfrac%7BdD%7D%7Bdt%7D%3D%20%26%20%5Cdelta%5C%2CI%5Cleft%28t%5Cright%29%5E%7B%5Calpha%7D%20%5Cend%7Bcases%7D)

This equations must be integrated with inicial conditions given by: s(0)=s_0 , I(0)=1 and R(0)=D(0)=0. The time variable t is defined as the time after first confirmed case. The model have five free parameters (\alpha,\beta,\rho,\delta,s_0), where s_0 is the initial susceptible individuals. Inthe case where \alpha=1, the SIRD model is recovered. As s_0, in general, assumes very large values, lets consider its log value. In this way, the parameters are $(\alpha,\beta,\rho,\delta,\log_{10}s_0).

# Results

The main result in this version is to plot de curves from the model for a specific parameter vector and compare this with dataset. In covid/stat.py, functions has been implemented to generate an MCMC sample, through which it will be possible to make inferences of the parametric intervals.

![image](./tables/crd-curve.png)

# Dataset

Here, we are using the Microsoft Data, from the repo https://github.com/microsoft/Bing-COVID-19-Data. 



## 1. Prerequisites
Before installing rAthena there are certain tools and applications you will need which
differs between the varying operating systems available.

### Hardware
Hardware Type | Minimum | Recommended
------|------|------
CPU | 1 Core | 2 Cores
RAM | 1 GB | 2 GB
Disk Space | 300 MB | 500 MB

### Operating System & Preferred Compiler
Operating System | Compiler
------|------
Linux  | [gcc-5 or newer](https://www.gnu.org/software/gcc/gcc-5/) / [Make](https://www.gnu.org/software/make/)
Windows | [MS Visual Studio 2013, 2015, 2017](https://www.visualstudio.com/downloads/)

### Required Applications
Application | Name
------|------
Database | [MySQL 5 or newer](https://www.mysql.com/downloads/) / [MariaDB 5 or newer](https://downloads.mariadb.org/)
Git | [Windows](https://gitforwindows.org/) / [Linux](https://git-scm.com/download/linux)

### Optional Applications
Application | Name
------|------
Database | [MySQL Workbench 5 or newer](http://www.mysql.com/downloads/workbench/)

## 2. Installation 

### Full Installation Instructions
  * [Windows](https://github.com/rathena/rathena/wiki/Install-on-Windows)
  * [CentOS](https://github.com/rathena/rathena/wiki/Install-on-Centos)
  * [Debian](https://github.com/rathena/rathena/wiki/Install-on-Debian)
  * [FreeBSD](https://github.com/rathena/rathena/wiki/Install-on-FreeBSD)

## 3. Troubleshooting

If you're having problems with starting your server, the first thing you should
do is check what's happening on your consoles. More often that not, all support issues
can be solved simply by looking at the error messages given. Check out the [wiki](https://github.com/rathena/rathena/wiki)
or [forums](https://rathena.org/forum) if you need more support on troubleshooting.

## 4. More Documentation
rAthena has a large collection of help files and sample NPC scripts located in the /doc/
directory. These include detailed explanations of NPC script commands, atcommands (@),
group permissions, item bonuses, and packet structures, among many other topics. We
recommend that all users take the time to look over this directory before asking for
assistance elsewhere.

## 5. How to Contribute
Details on how to contribute to rAthena can be found in [CONTRIBUTING.md](https://github.com/rathena/rathena/blob/master/.github/CONTRIBUTING.md)!

## 6. License
Copyright (c) rAthena Development Team - Licensed under [GNU General Public License v3.0](https://github.com/rathena/rathena/blob/master/LICENSE)
