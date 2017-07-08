# MSc_functions
Additional tools use in conjunction with AC_tools (https://github.com/tsherwen/AC_tools) functions for my MSc project. 

Abit about me - originally used functions within AC_tools but delevoped my own functions for bespoke issues and developements for my project 

This repository contains a portable collection of functions used for working with global/regional chemical transport model (CTM) ouput and observations.

The module is setup to be used as a submodule, with collections of functions held in module files that can be imported in entirely or seperately.

e.g.

import MSc_tools as MS

MS.get_subregion_site_dicts():

# INSTALL

mkdir -p $HOME/python
cd $HOME/python
git clone --recursive https://github.com/TimGarstin/MSc_tools/
