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
    from MSc_functions import *
 
else:
    from .MSc_functions import *
    
# --------------------------------- Section 1 ----------------------------------
# --------------  Data Extractors
#

# ----
# X.XX - Save filtered dataframe of selected species from large multispecies set of data as a file


# --------
def get_spec_from_large_dataset( wd=None, file=None, save_loc=None, spec=spec, sdate=sdate, edate=edate )
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
    df =df[[,'site',spec.lower()]]
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


def get_runs_percentage_change(data=None, data2=None, change_in=change_in, spec=spec ):
    """ 
    Function to get % change for different PM (and PM components) between two different GEOS-Chem model timeseries output.
    Can get df components extracted with AC_tools function AC.get_LOC_df_from_NetCDF, with indexed timeseries.(https://github.com/tsherwen/AC_tools)
    
    Parameters
    -------
    data (DataFrame) -  of all GEOS output species with column names as GEOS output species names, for GEOS RUN 1
    data2 (DataFrame) - of all GEOS output species with column names as GEOS output species names, for GEOS RUN 2
    change_in (str) - % change in what species? PM, SO4, NIT, NH4
    spec (str) - (PM10 or PM25 where PM25 is PM2.5)
    Returns
    -----
    (DataFrame) 
    Notes
    -- need to make improvements to make this function more versitile for NH4, NIT, SO4
     
    """
    # Get GEOS output dataframe into a more coherent dataframe 
    df = MS.get_PM_from_parts(data=data, spec=spec, keep_components=True)
    df2 = MS.get_PM_from_parts(data=data2, spec=spec, keep_components=True)
  
    # make returning DataFrame
    df3 = pd.DataFrame()
    
    # change_in choice calculations
    if change_in == 'PM':
     # concat relevent dataframes first , then do % calcs for % change
     
        df3['delta_PM'] = df[spec]   
        
    
    # Sum PM componment columns to get PM levels for both runs   
        
       
# ----
# X.XX - Get percentage change in certain species
# --------


def get_PM_from_parts(data=None, spec=spec, keep_components=True):
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
        df['Fine Dust1'] = df['DST1'] + df['DST2']
        df['Fine Sea Salt1'] = df['SALA']
        df['Elemental C1'] = df['BCPO'] + df['BCPI']
        df['Organic C1'] = df['OCPO'] + df['OCPI']
        df['Sulphate1'] = df['SO4']
        df['Ammonium1'] = df['NH4']
        df['Nitrate1'] = df['NIT']
        
        # sum PM2.5 components to make spec column
        df[spec] = df['Fine Dust1'] + df['Fine Sea Salt1'] + df['Elemental C1'] + df['Organic C1'] + df['Sulphate1'] + df['Ammonium1'] + df['Nitrate1']
        df2 = df[spec].copy()
        
        # return requested variables
        if keep_components:
            return df
        else:
            return df2     
           
    elif spec == 'PM10':
    # Sum PM2,5 geos spec outputs to PM components (dust etc)(e.g. 2 GEOS spec output 'bins' for dust PM2.5).  
        df['Fine Dust1'] = df['DST1'] + df['DST2'] + df['DST3'] + df['DST4']
        df['Fine Sea Salt1'] = df['SALA'] + df['SALC']
        df['Elemental C1'] = df['BCPO'] + df['BCPI']
        df['Organic C1'] = df['OCPO'] + df['OCPI']
        df['Sulphate1'] = df['SO4']
        df['Ammonium1'] = df['NH4']
        df['Nitrate1'] = df['NIT']
        
        # sum PM2.5 components
        df[spec] = df['Fine Dust1'] + df['Fine Sea Salt1'] + df['Elemental C1'] + df['Organic C1'] + df['Sulphate1'] + df['Ammonium1'] + df['Nitrate1']
        df2 = df[spec].copy()
          
        # return requested variables
        if keep_components:
            return df
        else:
            return df2    
    else:
        print "Select correct spec, (PM10, PM25) or alter function to develop another spec"
      
      
      

   
