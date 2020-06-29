#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 12 02:57:59 2020

@author: eduardo
"""

import warnings

from .functions import set_dir_struct, riffle, file_names, set_directory, distribute_among_walkers
from .dataset import read_dataset
from .country import country
from .models import mod_sird




# neglecting warnings
warnings.filterwarnings('ignore')

# setting directory structure
root_directory,tables_directory = set_dir_struct();     

set_directory(root_directory)