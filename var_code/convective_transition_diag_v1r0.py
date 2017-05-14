# ======================================================================
# convective_transition_diag_v1r0.py
#
#   Convective Transition Diagnostic Package
#   
#   Version 1 revision 0 04/28/2017 Yi-Hung Kuo (UCLA)
#   Contributors: K. A. Schiro (UCLA), B. Langenbrunner (UCLA), F. Ahmed (UCLA), 
#    C. Martinez (UCLA), C.-C. (Jack) Chen (NCAR)
#   PI: J. David Neelin (UCLA)
#
#   Currently consists of following functionalities:
#    (1) Convective Transition Basic Statistics (convecTransBasic.py)
#    (2) Convective Transition Critical Collapse (convecTransCriticalCollape.py)
#    *(3) Moisture Precipitation Joint Probability Density Function (cwvPrecipJPDF.py)
#    *(4) Super Critical Precipitation Probability (supCriticPrecipProb.py)
#    More on the way...(* under development)
#
#   Reference: Kuo et al. (201X)
#
# COPYLEFT Agreement TBD
# ======================================================================
# Import standard Python packages
import os

##### Functionalities in Convective Transition Diagnostic Package #####
# ======================================================================
# Convective Transition Basic Statistics
#  See convecTransBasic.py for detailed info
os.system("python "+os.environ["VARCODE"]+"/"+"convecTransBasic.py")
## ======================================================================
## Convective Transition Critical Collapse
##  Requires output from convecTransBasic.py
##  See convecTransCriticalCollapse.py for detailed info
os.system("python "+os.environ["VARCODE"]+"/"+"convecTransCriticalCollapse.py")

##### THE FOLLOWING FUNCTIONALITIES HAVE NOT BEEN IMPLEMENTED YET!!!#####
## ======================================================================
## Moisture Precipitation Joint Probability Density Function
##  See cwvPrecipJPDF.py for detailed info
#os.system("python "+os.environ["VARCODE"]+"/"+"cwvPrecipJPDF.py")
## ======================================================================
## Super Critical Precipitation Probability
##  Requires output from convecTransBasic.py
##  See supCriticPrecipProb.py for detailed info
#os.system("python "+os.environ["VARCODE"]+"/"+"supCriticPrecipProb.py")
