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
#   Reference: 
#    (?)Kuo, Y.-H., J. D. Neelin, and K. A. Schiro: Convective transition
#      statistics for climate model diagnostic. Part I. Observational
#      baseline. In preparation.
#    (?)Kuo, Y.-H., J. D. Neelin, and K. A. Schiro: Convective transition
#      statistics for climate model diagnostic. Part II. GCM performance.
#      In preparation.
#    Neelin, J. D., O. Peters, and K. Hales, 2009: The transition to strong
#      convection. J. Atmos. Sci., 66, 2367–2384, doi:10.1175/2009JAS2962.1.
#    Sahany, S., J. D. Neelin, K. Hales, and R. B. Neale, 2012:
#      Temperature–moisture dependence of the deep convective
#      transition as a constraint on entrainment in climate models.
#      J. Atmos. Sci., 69, 1340–1358, doi:10.1175/JAS-D-11-0164.1.
#    Schiro, K. A., J. D. Neelin, D. K. Adams, and B. R. Linter, 2016:
#      Deep convection and column water vapor over tropical land
#      versus tropical ocean: A comparison between the Amazon and
#      the tropical western Pacific. J. Atmos. Sci., 73, 4043–4063,
#      doi:10.1175/JAS-D-16-0119.1.
#    Kuo, Y.-H., J. D. Neelin, and C. R. Mechoso, 2017: Tropical Convective 
#      Transition Statistics and Causality in the Water Vapor–Precipitation
#      Relation. J. Atmos. Sci., 74, 915-931, doi:10.1175/JAS-D-16-0182.1.
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
