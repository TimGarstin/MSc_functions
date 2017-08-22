
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

# -- Plotting
import matplotlib.pyplot as plt

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

# ----------------------------- Section 1 ------------------------------------
# -------------- Common Plotting
#

# ----
# 1.1 - Diurnal
# -----
def diurnal_plot(df=None, color=color, alpha=0.5, lw=0.01, units= 'nmol mol$^{-1}$', f_size=12, frameon=False)
                 
                 
    """
    -current expectation is that that 'Date' column in df is preformatted as datetime 
    
    """
   
    # Drop rows that contain Nan values - kludge to solve ax_fill nan issue
    df = df.dropna()
   
    # Make month and hour columns from datetime column and drop Date 
    df['Date'] = df.index
    df['hour'] =df['Date'].dt.hour
    df = df.drop('Date',1)

    # Groupby hour and do median and standard dev across the all values within hour
    df_m = df.groupby('hour').median()
    df_sd = df.groupby('hour').std()
    del df
                 
    # Concatonate median and standard deviation dataframes
    df1 = pd.concat([df_m, df_sd], axis=1)
    df1.columns = ['median','std']
    
    # Calculate upper and lower standard deviations
    df1['upper_std'] = df1['median'] + df1['std']
    df1['lower_std'] = df1['median'] - df1['std']
                 
    # ---- Plot obs up and return the axis plotted on and correct legend (klunge) ----
    
    # line plot of median
    ax = df1['median'].plot( color = color)
    
    # shade regions between upper and lower standard deviations
    ax.fill_between( df1.index, df1['lower_stf'], df1['upper_std'], color=color, alpha=alpha, lw=lw )
      

    # plotting labelling  
    units = units  
    ax.set_ylabel(units)
    ax.set_xlabel('Hour of Day', fontsize = f_size*1.2)
    ax.set_title("Diurnal", fontsize=f_size*1.3, y=1.04)
    
    # add legend
    L=plt.legend( prop={'size':f_size}, frameon=frameon)
    
    # aesthetic clean up
    ax = get_sb_style( ax=ax, f_size=12 )
    
    # Save figure with Figure.savefig() method
    fig = ax.get_figure()
    fig.savefig("DIURNAL.png", dpi=360 )
    plt.show()
    plt.close(fig)
                 
        
        

        
# ----------------------------- Section X ------------------------------------
# -------------- Common Aesthetics
#

# ----
# X.1 - Seaborn Default style plotting aesthetics with matplotlib axis
# -----
def get_sb_style(f_size=12, ax=ax )
 
    # Change appearance of ticks
    ax.yaxis.set_tick_params(labelsize=f_size*1.2)
    ax.xaxis.set_tick_params(labelsize=f_size*1.2)

    # Background colours, opacity and layering
    ax.patch.set_alpha(0.5)
    ax.set_axis_bgcolor( color='lavender')
    ax.set_axisbelow(True)
                 
    # Gridline white
    ax.grid(b=True, which='major', color='w', linestyle='-', linewidth=1.3, alpha = 0.8)
    
    # remove spines and ticks
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.tick_params(axis=u'both', which=u'both',length=0)
                 
    # return axis
    return ax
