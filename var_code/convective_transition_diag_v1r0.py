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
#    (1) Convective Transition Statistics (convecTransStats.py)
#    *(2) Convective Transition Thermodynamic Critical (convecTransThermoCritic.py)
#    *(3) Moisture Precipitation Joint Probability Density Function (cwvPrecipJPDF.py)
#    *(4) Moisture Precipitation Joint Probability Density Function (supCriticPrecipProb.py)
#    More on the way...(* under development)
#
# COPYLEFT Agreement TBD
# ======================================================================
# Import standard Python packages
import os

##### Functionalities in Convective Transition Diagnostic Package #####
# ======================================================================
# Convective Transition Statistics
#  See convecTransStats.py for detailed info
os.system("python "+os.environ["VARCODE"]+"/"+"convecTransStats.py")
#### THE FOLLOWING FUNCTIONALITIES HAVE NOT BEEN IMPLEMENTED YET!!!####
## ======================================================================
## Convective Transition Thermodynamic Critical
##  See convecTransThermoCritic.py for detailed info
#os.system("python "+os.environ["VARCODE"]+"/"+"convecTransThermoCritic.py")
## ======================================================================
## Moisture Precipitation Joint Probability Density Function
##  See cwvPrecipJPDF.py for detailed info
#os.system("python "+os.environ["VARCODE"]+"/"+"cwvPrecipJPDF.py")
## ======================================================================
## Moisture Precipitation Joint Probability Density Function
##  See supCriticPrecipProb.py for detailed info
#os.system("python "+os.environ["VARCODE"]+"/"+"supCriticPrecipProb.py")
