#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Functions for use with the GEOS-Chem chemical transport model (CTM).
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
    
    
# --------------------------------- Section 1 ----------------------------------
# --------------  Data Extractors
#

# ----
# X.XX - Save filtered dataframe of selected species from large multispecies set of data as a file


# --------
def get_spec_from_large_dataset( wd=None, file=None, save_loc=None, spec='O3', sdate=None, edate=None ):
    """ 
    Driver to extract needed data (spec and site) information from large data set
    
    Parameters
    -------
    wd (str) - add location of directory of metadata file 
    file (str) - metadata file name
    save_loc (str) - location to save filtered dataframe file 
    spec (str) - spec to chose (e.g. NO2, SO2, O3, CO , PM10, PM25, C2H6, C3H8, PRPE, ALK4, BR, ClO, etc )
    sdate (str) - Datetime format date 
    edate (str) - Datetime format date
    
    Returns
    -------
    N/A - Save file to location
    Notes
    -----
     - site type choices can be altered ['rural', 'background', 'rural_background', 'urban_background','suburban_background','suburban','roadside','kerbside','industry','nan']
     
    """
 
    # Generate DataFrame from overall data set (all species within )                            
    df = pd.read_csv( wd+filename )# o3 left

    # Make Datecolumn datetime format and index by datetime
    df['Date'] = pd.to_datetime(df['date'],format='%Y-%m-%d %H:%M:%S')
    df.index = df['Date'] # Date already in datetime
    
    # Select species and site columns from DataFrame
    df =df[['site',spec.lower()]]
    df['site'] = df['site'].str.lower()

    # Select dataset size of choice by dates filter
    df = df[df.index >= sdate ]
    df = df[df.index < edate ]
    
    # Replace negative and zero value with NaN
    df[df == 0] = np.nan
    df[df.values < 0] = np.nan
    
    # Convert all none float values to NaN
    def convertdata2float(x):
        """
        check if float, if not convert to np.nan
        """
        try:
            return np.float(x)
        except:
            return np.nan
        df = df.applymap(convertdata2float)
    
    # Save dataframe in suitable location
    save_loc ='/work/home/tg706/msc_tools/working_directories/dataframes/'
    df.to_pickle(df_locato+spec+file)

    #df1 = pd.read_pickle(df_locato+spec+file)
    

# ----
# X.XX - Get dictionary of regional sites, within selected predefined regions
# --------


def get_subregion_site_dicts(eu_area='UK AND IRELAND', wd=None, filename=None  ):
    """ 
    Driver to extract data requested ( as families have differing diagnostic units)
    
    Parameters
    -------
    eu_area(str) - define area for site region extraction (e.g BELENUX, EU, NORTH MEDDITERANEAN, SCANDINAVIA, WEST, UK, UK AND IRELAND)
    wd (str) - working directory of metadata file
    filename (str) - metadatafile
    Returns
    -------
    (dictionary) , dictionary keys are the regions. within are sites names, country origin of site and for site type.
    Notes
    -----
     - site type choices can be altered ['rural', 'background', 'rural_background', 'urban_background','suburban_background','suburban','roadside','kerbside','industry','nan']
     
    """
    
    # Initialise dataset of regional sites 
    df=pd.read_csv( wd+filename )
    
    # Initialise dictionary
    subregion_dict = {}
    
    # Find sites for region and relevant columns
    df_c = df[['site','country','site_type']]
    
    # Loop all sites and check if they are in region
    sites = sorted(set(df_c['site']))
    
    # Selecting site type choices
    site_typelist = ['rural', 'background', 'rural_background', 'urban_background','suburban_background']
    new_siteslist = []
    
    # Select sites for those site types
    for site in sites:
        tmp_sitetype = df_c[df_c['site'] == site].site_type.values[0]
        if tmp_sitetype in site_typelist:
            new_siteslist += [site]
            
    # Generate new list of given sites of correct site type
    sites = new_siteslist
    # Select relevent rows of datafame from list of site names
    df_c = df_c[df_c['site'].isin(sites)]
    
    # --- WEST
    if eu_area == 'WEST':
        country_typelist = ['spain','france','portugal']
        def country_in_list(site, my_countries=country_typelist):
            return (site in my_countries)
        # Get sites
        tmp_sites = df_c[df_c['country'].apply(country_in_list)]
        #add to dictionary
        subregion_dict[eu_area] = tmp_sites
    
    # --- BELENUX
    if eu_area == 'BELENUX':
        country_typelist = ['belgium','luxembourg','netherlands'] # belenux
        def country_in_list(site, my_countries=country_typelist):
            return (site in my_countries)
        # Get sites
        tmp_sites = df_c[df_c['country'].apply(country_in_list)]
        #add to dictionary
        subregion_dict[eu_area] = tmp_sites
  
    # --- UK AND IRELAND
    if eu_area == 'UK AND IRELAND':
        country_typelist = ['united_kingdom','ireland'] #ukire
        def country_in_list(site, my_countries=country_typelist):
            return (site in my_countries)
        # Get sites
        tmp_sites = df_c[df_c['country'].apply(country_in_list)]
        #add to dictionary
        subregion_dict[eu_area] = tmp_sites
    
    # --- UK
    if eu_area == 'UK':
        country_typelist = ['united_kingdom']
        def country_in_list(site, my_countries=country_typelist):
            return (site in my_countries)
        # Get sites
        tmp_sites = df_c[df_c['country'].apply(country_in_list)]
         #add to dictionary
        subregion_dict[eu_area] = tmp_sites
    
    # --- NORTH MEDITERRANEAN
    if eu_area == 'NORTH MEDITERANNEAN':
        country_typelist = ['spain','italy','malta','slovenia','croatia','bosnia_and_herzegovina','montenegro','albania','greece','turkey','cyprus'] #northmed, exclude france
        def country_in_list(site, my_countries=country_typelist):
            return (site in my_countries)
        # Get sites
        tmp_sites = df_c[df_c['country'].apply(country_in_list)]
        #add to dictionary
        subregion_dict[eu_area] = tmp_sites
    
    # --- SCANDINAVIA
    if eu_area == 'SCANDINAVIA':
        country_typelist = ['denmark','norway','sweden','finland'] #scandinavia
        def country_in_list(site, my_countries=country_typelist):
            return (site in my_countries)
        # Get sites
        tmp_sites = df_c[df_c['country'].apply(country_in_list)]
        #add to dictionary
        subregion_dict[eu_area] = tmp_sites
    
    # --- EU
    if eu_area == 'EU':
        country_typelist = ['albania','andorra','austria','belgium','bosnia_and_herzegovina','bulgaria','croatia','cyprus','czech_republic','denmark','estonia','finland','france','germany','greece','hungary','iceland','ireland','italy','kosovo','latvia','liechtenstein','lithuania','luxembourg','macedonia','malta','montenegro','netherlands','norway','poland','portugal','romania','serbia','slovakia','slovenia','spain','sweden','switzerland','turkey','united_kingdom']
        def country_in_list(site, my_countries=country_typelist):
            return (site in my_countries)
        # Get sites
        tmp_sites = df_c[df_c['country'].apply(country_in_list)]
        #add to dictionary
        subregion_dict[eu_area] = tmp_sites
    
    else:
        print ("Correct region not selected \nREGIONS: BELENUX, EU, NORTH MEDDITERANEAN, SCANDINAVIA, WEST, UK, UK AND IRELAND \nOR add a custom region in github")
    #return
    return subregion_dict 
   
# --------------------------------- Section 2 ----------------------------------
# --------------  Data Manipulations
#

# ----
# X.XX - Get percentage change in certain species
# --------


def get_runs_percentage_change(data=None, data2=None, change_in='PM25', spec='PM25', keep_components=True ):
    """ 
    Function to get % change for different PM (and PM components) between two different GEOS-Chem model timeseries output.
    Can get df components extracted with AC_tools function AC.get_LOC_df_from_NetCDF, with indexed timeseries.(https://github.com/tsherwen/AC_tools)
    
    Parameters
    -------
    data (DataFrame) -  of all GEOS output species with column names as GEOS output species names, for GEOS RUN 1
    data2 (DataFrame) - of all GEOS output species with column names as GEOS output species names, for GEOS RUN 2
    change_in (str) - % change in what species? ( PM25, PM10, SO4, NIT, NH4 ) - SO4, NIT and NH4 are PM parts
    spec (str) - (PM10 or PM25 where PM25 is PM2.5)
    keep_componments (booleon) - once Pm calc done keep component data? (NIT, SO4 etc). 
    Returns
    -----
    (DataFrame) 
    Notes
    -- works but this function can be shrinked further. 
     
    """
    # Get GEOS output dataframe into a more coherent dataframe  - pulls out PM2.5 or PM10 comonent and summed data.
    df = get_PM_from_parts(data=data, spec=spec, keep_components=True)
    df2 = get_PM_from_parts(data=data2, spec=spec, keep_components=True)
    
    # Kludge - both dataframes of same column names need to differentiate, add string to each column in df2
    df2.columns = [str(col) + '_df2' for col in df2.columns]
    print df.head()
    print df2.head()
    sys.exit()
    # Concatonate DataFrame on columns
    df_c = pd.concat([df, df2], axis=1)
    print df_c.head()
    #sys.exit()
    # make returning DataFrame
    df3 = pd.DataFrame()
    print df_c.head()
    # Get difference between two runs  
    df_c['dif'] = df_c[change_in] /df_c[change_in+'_df2'] 
       
    # get fractional change from difference (change / run1)
    df_c['f_change'] = df_c['dif'].div(df_c[spec], axis=0)
                                          
    # Multiply fraction column by 100 to get %
    #df_c[change_in+'fractional_change'] = df_c.loc[:,'f_change'] *= 100 
    print df_c.head()
    df_c[change_in+'fractional_change'] = df_c['f_change'].multiply(100)
    print df_c.head()
        
    # Return DataFrame
    return df3 
       
       
# ----
# X.XX - Get percentage change in certain species
# --------


def get_PM_from_parts(data=None, spec='PM25', keep_components=True):
    """ 
    Function to get PM spec total the components that make it up (sulphates, dust, nitrates, ammonium etc)
    Can get df components from GEOS model timeseires output from AC_tools component extractor function
    AC.get_LOC_df_from_NetCDF, with indexed timeseries.(https://github.com/tsherwen/AC_tools)
    
    Parameters
    -------
    data (dataframe) -
    spec (str) - species which we want to sum its components for (e.g. PM10, PM25)
    keep_components (booleon ) - keep PM component columns once PM calculated?
    Returns
    -------
    (dataframe) 
    Notes
    -- need to make improvements to make this function versitile to any scenario 
     
    """
    # working with pandas 
    df = data
    if spec == 'PM25':
    # Sum PM2,5 geos spec outputs to PM components (dust etc)(e.g. 2 GEOS spec output 'bins' for dust PM2.5).  
        df['Fine Dust'] = df['DST1'] + df['DST2']
        df['Fine Sea Salt'] = df['SALA']
        df['Elemental C'] = df['BCPO'] + df['BCPI']
        df['Organic C'] = df['OCPO'] + df['OCPI']
        df['Sulphate'] = df['SO4']
        df['Ammonium'] = df['NH4']
        df['Nitrate'] = df['NIT']
        
        # sum PM2.5 components to make spec column
        df[spec] = df['Fine Dust'] + df['Fine Sea Salt'] + df['Elemental C'] + df['Organic C'] + df['Sulphate'] + df['Ammonium'] + df['Nitrate']
        df2 = df[spec].copy()
        
        # return requested variables
        if keep_components:
            return df
        else:
            return df2     
           
    elif spec == 'PM10':
    # Sum PM2,5 geos spec outputs to PM components (dust etc)(e.g. 2 GEOS spec output 'bins' for dust PM2.5).  
        df['Coarse Dust'] = df['DST1'] + df['DST2'] + df['DST3'] + df['DST4']
        df['Coarse Sea Salt'] = df['SALA'] + df['SALC']
        df['Elemental C'] = df['BCPO'] + df['BCPI']
        df['Organic C'] = df['OCPO'] + df['OCPI']
        df['Sulphate'] = df['SO4']
        df['Ammonium'] = df['NH4']
        df['Nitrate'] = df['NIT']
        
        # sum PM2.5 components
        df2[spec] = df['Coarse Dust'] + df['Coarse Sea Salt'] + df['Elemental C'] + df['Organic C'] + df['Sulphate'] + df['Ammonium'] + df['Nitrate']
        df2 = df[spec].copy()
          
        # return requested variables
        if keep_components:
            return df
        else:
            return df2    
    else:
        print "Select correct spec, (PM10, PM25) or alter function to develop another spec"
      
      
      

   
