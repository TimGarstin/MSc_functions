
#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Miscellaneous code using numpy library that is useful for the project
NOTE(S):    
 - This module is just beginning to be developed, these are being moved across from my developments in a branch of AC_tools (https://github.com/tsherwen/AC_tools/blob/master/funcs4GEOSC.py)
   underdevelopment vestigial/inefficient code is being removed/updated. 
 - Where external code is used credit is given. 
"""

# ----------------------------- Section 0 -----------------------------------
# -------------- Import modules:
#
# -- I/O / Low level                                                                                
import pandas as pd

# -- Math/Analysis                                                                                   
import numpy as np
import scipy.stats as stats


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
    
    
# --------------------------------- Section 1 ----------------------------------
# --------------  Data Extracting/ Storing 
#

# ----
# X.XX - Save dictionary to file location


# --------
"""
Save an array to a binary file in NumPy .npy format.
wd (str)=  'wd_loc/'
filename (str) = 'filename.npy'
arr = array like , e.g. array, dictionary, etc
"""
np.save(wd+filename, arr=None )


# --------------  Data Extracting/ Storing 
#

# ----
# X.XX - Loading dictionary from file location


# --------
"""
Load an array from binary file in NumPy .npy format.
wd (str)=  'wd_loc/'
filename (str) = 'filename.npy'

"""
np.load(wd+filename).item()





