

#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
# add the 16 types of plots you have scripted for in here --
Functions for plotting with Matplotlib and Seaborn packages, in relation to the GEOS-Chem chemical transport model (CTM).
NOTE(S):    
 - This module is just beginning to be developed, these are being moved across from my developments in a branch of AC_tools (https://github.com/tsherwen/AC_tools/blob/master/funcs4GEOSC.py)
   underdevelopment vestigial/inefficient code is being removed/updated. 
 - Where external code is used credit is given. 
"""

# ----------------------------- Section 0 -----------------------------------
# -------------- Import modules:
#
# -- I/O / Low level                                                                                
import os
import sys
import csv
import glob
import pandas as pd

# -- Math/Analysis                                                                                   
import numpy as np
import scipy.stats as stats
import math

# -- Time                                                                                           
#import time
#import calendar
#import datetime as datetime
#from datetime import datetime as datetime

# --  This needs to be updated, imports should be specific and in individual functions
# import MSc_functions that can be used within other functions.
if __package__ is None:
    from funcs_4_work import *
    from funcs_4_plotting import *
    from math_4_msc import *
   
 
else:
    from .funcs_4_work import *
    from .funcs_4_plotting import *
    from .math_4_msc import *
    
    
# Sections to add... - 1. Timeseries (diurnal, weekly, seasonal) 2. PDF, CDF, 3. HEXBIN, scatter, 4. map plotting ( average, locations of sites, bias , etc) 
# 6. stakced area, 7. delta plots 8. flow charts 9. (2 run comparable plots ).
