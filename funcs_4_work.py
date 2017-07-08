#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Functions for use with the GEOS-Chem chemical transport model (CTM).
NOTE(S):    
 - This module is just under development as original developments used in a branch of AC_tools (https://github.com/tsherwen/AC_tools/blob/master/funcs4GEOSC.py)
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
import time
import calendar
import datetime as datetime
from datetime import datetime as datetime_

# --------------------------------- Section 2 ----------------------------------
# --------------  Data Extractors
#

# ----
# X.XX - Get dictionary of regional sites, within selected predefined regions
# --------


def get_subregion_site_dicts(eu_area = 'UK AND IRELAND', wd = None, filename=None  ):
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
