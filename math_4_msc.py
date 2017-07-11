

#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
# add math functions relevent to GEOS Chem calculations that have been typically used in my project -- 
Functions for typical math functions required in relation to the GEOS-Chem chemical transport model (CTM).
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
    
    
# select relevent scripting calcs typically applied in geos chem (esp. unit conversion calcs - useful to others )
#1. unit conversion calcs (p mol mol-1 to ug m-3 ) etcc
# store relevant additional math functions at bottom in misc section
