# ======================================================================

# NOAA Model Diagnotics Task Force (MDTF) Diagnostic Driver
#
# March 6, 2017  Chih-Chieh (Jack) Chen, NCAR
#
# ======================================================================

import os
import subprocess

# ======================================================================
# If using NCL, need to point to it 
#set NCARG_ROOT

#os.environ["NCARG_ROOT"]="/usr/bin/ncl"

# ======================================================================
# delete PS files or not
# 1: delete, otherwise not

os.environ["CLEAN"] = "0"

# ======================================================================
# set case name
# ======================================================================
#os.environ["CASENAME"] = "c192L48_am4b6_DDFull_MDTF"
#os.environ["CASENAME"] = "c96L48_am4b6_DDFull_MDTF"
#os.environ["CASENAME"] = "c96L32_am4g9_fullaero_MDTF"
os.environ["CASENAME"] = "cam5p3"

# ======================================================================
# Year stamp of data
# ======================================================================
# if the time range is different for different frequencies of model output
# set here
#
os.environ["FIRSTYR"] =  "1"
os.environ["LASTYR"] =  "3"

# ======================================================================
# DIRECTORIES: set up locations
# ======================================================================


# ======================================================================
#  Home directory for diagnostic code (needs to have 'var_code' and 'var_data' sub-directories

os.environ["DIAG_HOME"] = os.getcwd()

# ======================================================================
# wkdir (diagnostics should generate .nc files & .ps files here)

os.environ["WKDIR"] = os.getcwd()+"/wkdir/"+os.environ["CASENAME"]

# ======================================================================
# INPUT: directory of model output

#os.environ["DATADIR"] = os.getcwd()+"/"+os.environ["CASENAME"]
os.environ["DATADIR"] = "/home/yhkuo/Downloads/"+os.environ["CASENAME"]
#os.environ["DATADIR"] = "/ninad/baird/"+os.environ["CASENAME"]

# ======================================================================
#OUTPUT
# 1 = create tar file of results, send to webdir if set
os.environ["make_variab_tar"] = "1"
os.environ["WEBDIR"] = os.getcwd()+"/web/"

# ======================================================================
# set variable names and files
# ======================================================================
# Variables for Convective Transition Diagnostics package:
os.environ["TAVE_var"] = "tave" # Mass-Weighted Column Average Tropospheric Temperature
os.environ["QSAT_INT_var"] = "qsat_int" # Vertically-Integrated Saturation Specific Humidity
os.environ["RES"] = "1.00" # Spatial Resolution (degree) for TMI Data (0.25, 0.50, 1.00)

#MODEL
os.environ["model"] = "CESM"
#os.environ["model"] = "AM4"

if os.environ["model"] == 'CESM' :
   os.environ["hyam_var"] = "hyam"
   os.environ["hybm_var"] = "hybm"  
   os.environ["lat_coord"] = "lat"
   os.environ["lon_coord"] = "lon"   
   os.environ["lev_coord"] = "lev"
   os.environ["time_coord"] = "time"   
   os.environ["lat_var"] = "lat"   
   os.environ["lon_var"] = "lon"
   os.environ["time_var"] = "time"  
   os.environ["U_var"] = "U"   
   os.environ["Z3_var"] = "Z3"
   #os.environ["PRECT_var"] = "PRECT"   
   os.environ["PRECC_var"] = "PRECC"
   os.environ["PRECL_var"] = "PRECL"
   os.environ["FLUT_var"] = "FLUT"
   os.environ["FSNTOA_var"] = "FSNTOA"
   os.environ["TREFHT_var"] = "TREFHT"
   os.environ["TS_var"] = "TS"
   os.environ["LANDFRAC_var"] = "LANDFRAC"
   os.environ["TAUX_var"] = "TAUX"
   os.environ["CLDTOT_var"] = "CLDTOT"
   os.environ["ICEFRAC_var"] = "ICEFRAC"
   os.environ["PS_var"] = "PS"
   os.environ["PSL_var"] = "PSL"
   os.environ["U200_var"] = "U200"
   os.environ["V200_var"] = "V200"
   os.environ["U850_var"] = "U850"
   os.environ["V850_var"] = "V850"
   os.environ["OMEGA500_var"] = "OMEGA500"
   os.environ["prect_conversion_factor"] = "1000000" #units = m/s
   os.environ["precc_conversion_factor"] = "1" #units = m/s
   os.environ["precl_conversion_factor"] = "1" #units = m/s
   os.environ["file_path"] = os.environ["DATADIR"]
   os.environ["file_Z3"] = os.environ["CASENAME"]+"."+os.environ["Z3_var"]+".nc"
   os.environ["file_PS"] = os.environ["CASENAME"]+"."+os.environ["PS_var"]+".nc"

   # ------------------------------------------------------------------------
   # Variables for Convective Transition Diagnostics package:
   os.environ["T_3D_var"] = "ta" # if 3D temperature exists   
   os.environ["PRECT_var"] = "pr"   
   os.environ["CWV_var"] = "prw" # Column Water Vapor (precipitable water vapor)
   os.environ["file_PRECT"] = "NCAR-CAM5.atmos.*."+os.environ["PRECT_var"]+".nc"
   os.environ["file_CWV"] = "NCAR-CAM5.atmos.*."+os.environ["CWV_var"]+".nc"
   os.environ["file_T_3D"] = "NCAR-CAM5.atmos.*."+os.environ["T_3D_var"]+".nc"
   os.environ["file_TAVE"] = "NCAR-CAM5.atmos.*."+os.environ["TAVE_var"]+".nc"
   os.environ["file_QSAT_INT"] = "NCAR-CAM5.atmos.*."+os.environ["QSAT_INT_var"]+".nc"
   # ------------------------------------------------------------------------


if os.environ["model"] == "AM4" :
   os.environ["lat_coord"] = "lat"
   os.environ["lon_coord"] = "lon"   
   os.environ["lev_coord"] = "level" # must be on pressure levels (hPa)
   os.environ["time_coord"] = "time"   
   os.environ["lat_var"] = "lat"   
   os.environ["lon_var"] = "lon"
   os.environ["time_var"] = "time"
   os.environ["PS_var"] = "PS"
   os.environ["prect_conversion_factor"] = "1" #units = m/s
   os.environ["precc_conversion_factor"] = "1" #units = m/s
   os.environ["precl_conversion_factor"] = "1" #units = m/s
   
   # ------------------------------------------------------------------------
   # Variables for Convective Transition Diagnostics package:
   os.environ["PRECT_var"] = "pr"   
   os.environ["T_3D_var"] = "ta" # if 3D temperature exists
   os.environ["CWV_var"] = "PRW" # Column Water Vapor (precipitable water vapor)
   os.environ["file_PRECT"] = "atmos.*."+os.environ["PRECT_var"]+".nc"
   os.environ["file_CWV"] = "atmos.*."+os.environ["CWV_var"]+".nc"
   os.environ["file_T_3D"] = "atmos.*."+os.environ["T_3D_var"]+".nc"
   os.environ["file_TAVE"] = "atmos.*."+os.environ["TAVE_var"]+".nc"
   os.environ["file_QSAT_INT"] = "atmos.*."+os.environ["QSAT_INT_var"]+".nc"
   # ------------------------------------------------------------------------
 
# ======================================================================
# Software 
# ======================================================================
#
# Diagnostic package location and settings
#
# The environment variable DIAG_HOME must be set to run this script
#    It indicates where the variability package source code lives and should
#    contain the directories var_code and var_data although these can be 
#    located elsewhere by specifying below.

os.environ["VARCODE"] = os.environ["DIAG_HOME"]+"/var_code"
os.environ["VARDATA"] = os.environ["DIAG_HOME"]+"/var_data"
os.environ["RGB"] = os.environ["DIAG_HOME"]+"/rgb"

# ======================================================================
# Check directories
# ======================================================================

if not os.path.exists(os.environ["DIAG_HOME"]):
   print "DIAG_HOME directory does not exist $DIAG_HOME"
   exit()
else:
   print "DIAG_HOME is set to "+os.environ["DIAG_HOME"]

if not os.path.exists(os.environ["VARCODE"]):
   print "VARCODE directory $VARCODE does not exist"
#   print "The default setting is \$DIAG_HOME/var_code but user settings can override this"
   exit()
else:
   print "VARCODE is set to "+os.environ["VARCODE"]

if not os.path.exists(os.environ["VARDATA"]):
   print "VARDATA directory $VARDATA does not exist"
   print "The default setting is \$DIAG_HOME/../var_data but user settings can override this"
   exit()
else:
   print "VARDATA is set to "+os.environ["VARDATA"]

if not os.path.exists(os.environ["RGB"]):
   print "RGB directory $RGB does not exist"
   print "The default setting is \$DIAG_HOME/rgb but user settings can override this"
   exit()
else:
   print "RGB is set to "+os.environ["RGB"]

# NCL / NCARG
if not 'NCARG_ROOT' in os.environ:
   print "ERROR: You do not have the environment"
   print "variable NCARG_ROOT not defined, which is used by NCL"
   exit()

if not os.path.exists(os.environ["NCARG_ROOT"]):
   print "NCARG_ROOT directory does not exist $NCARG_ROOT"
   exit()
else:
   print "NCARG_ROOT is set to "+os.environ["NCARG_ROOT"]

ncl_err = os.system("which ncl")
if ncl_err == 0:
   os.environ["NCL"] = subprocess.check_output("which ncl", shell=True)
   print "using ncl "+os.environ["NCL"]
else:
   print "ERROR: ncl not found"
   exit()

# ======================================================================
# DO NOT modify 
# ======================================================================
if os.path.exists(os.environ["WKDIR"]):
   print "using "+os.environ["WKDIR"]
else:
   os.makedirs(os.environ["WKDIR"])

if not os.path.exists(os.environ["WKDIR"]+"/MDTF_"+os.environ["CASENAME"]):
   os.makedirs(os.environ["WKDIR"]+"/MDTF_"+os.environ["CASENAME"])

if not os.path.exists(os.environ["WKDIR"]+"/MDTF_"+os.environ["CASENAME"]+"/"+os.environ["CASENAME"]):
   os.makedirs(os.environ["WKDIR"]+"/MDTF_"+os.environ["CASENAME"]+"/"+os.environ["CASENAME"])

if not os.path.exists(os.environ["WKDIR"]+"/MDTF_"+os.environ["CASENAME"]+"/obs"):
   os.makedirs(os.environ["WKDIR"]+"/MDTF_"+os.environ["CASENAME"]+"/obs")

if not os.path.exists(os.environ["WEBDIR"]):
   os.makedirs(os.environ["WEBDIR"])


os.environ["variab_dir"] = os.environ["WKDIR"]+"/MDTF_"+os.environ["CASENAME"]


# ======================================================================
# set up html file
# ======================================================================
os.system("cp "+os.environ["VARCODE"]+"/html/variab.html "+os.environ["WKDIR"]+"/MDTF_"+os.environ["CASENAME"])
os.system("cp "+os.environ["VARCODE"]+"/html/mdtf_diag_banner.png "+os.environ["WKDIR"]+"/MDTF_"+os.environ["CASENAME"])


# Diagnostics:
os.chdir(os.environ["WKDIR"])

# ======================================================================
# 1. SAMPLE: EOF of geopotential height anomalies of 500 hPa
# ======================================================================
# Call a piece of python code that: 
#   (A) Calls NCL to generate plots (PS)
#   (B) Converts plots to png
#   (C) Adds plot links to HTML file
#os.system("python "+os.environ["VARCODE"]+"/eof_plots.py")
# ======================================================================
# ADD USER CODE HERE: code will
# (a) call plotting routine and (b) move plots and add to web page
# python my_great_plots.py
# ======================================================================
# Convective Transition Diagnostics
#   Depends on the following scripts/files:
#     (1) var_code/convective_transition_diag_v1r0.py
#     (2) var_code/convecTransStats_util.py
#     (3) var_code/convecTransStats_usp_calc.py
#     (4) var_code/convecTransStats_usp_plot.py
#     (5) var_data/region_0.25x0.25_GOP2.5deg.mat
#     (6) R2_TMIv7r1_..._onset_diag_....png
#   This package requires 3 2-D model fields (or 3-D input to create these):
#     (1) precipitation rate
#     (2) vertically-averaged temperature or vertically-integrated saturation specific humidity
#     (3) column water vapor (CWV, or precipitable water vapor)
#   For further documentation & user options, see comments in convective_transition_diag_v1r0.py
os.system("python "+os.environ["VARCODE"]+"/convective_transition_diag_v1r0.py")

# ======================================================================
#  DO NOT modify: finish html file
# ======================================================================
os.system("echo '</BODY>' >> "+os.environ["WKDIR"]+"/MDTF_"+os.environ["CASENAME"]+"/variab.html")
os.system("echo '</HTML>' >> "+os.environ["WKDIR"]+"/MDTF_"+os.environ["CASENAME"]+"/variab.html")
os.system("cp "+os.environ["WKDIR"]+"/MDTF_"+os.environ["CASENAME"]+"/variab.html "+os.environ["WKDIR"]+"/MDTF_"+os.environ["CASENAME"]+"/tmp.html")
os.system("cat "+os.environ["WKDIR"]+"/MDTF_"+os.environ["CASENAME"]+"/variab.html "+"| sed -e s/casename/"+os.environ["CASENAME"]+"/g > "+os.environ["WKDIR"]+"/MDTF_"+os.environ["CASENAME"]+"/tmp.html")
os.system("cp "+os.environ["WKDIR"]+"/MDTF_"+os.environ["CASENAME"]+"/tmp.html "+os.environ["WKDIR"]+"/MDTF_"+os.environ["CASENAME"]+"/variab.html")
os.system("rm -f "+os.environ["WKDIR"]+"/MDTF_"+os.environ["CASENAME"]+"/tmp.html")

if os.environ["make_variab_tar"] == "1":
   if os.path.isfile( os.environ["variab_dir"]+".tar" ):
      os.system("mv -f "+os.environ["variab_dir"]+".tar "+os.environ["variab_dir"]+".tar_old")
      os.chdir(os.environ["WKDIR"])
      status = os.system("tar cf MDTF_"+os.environ["CASENAME"]+".tar MDTF_"+os.environ["CASENAME"])
      if not status == 0:
         print "ERROR $0"
         print "trying to do:     tar cf "+os.environ["variab_dir"]+".tar "+os.environ["variab_dir"]
         exit()
   else:
      os.chdir(os.environ["WKDIR"])
      status = os.system("tar cf MDTF_"+os.environ["CASENAME"]+".tar MDTF_"+os.environ["CASENAME"])
      if not status == 0:
         print "ERROR $0"
         print "trying to do:     tar cf "+os.environ["variab_dir"]+".tar "+os.environ["variab_dir"]
         exit()
      if os.path.exists(os.environ["WEBDIR"]):
         status = os.system("mv "+os.environ["variab_dir"]+".tar "+os.environ["WEBDIR"])
         if status == 0:
            os.chdir(os.environ["WEBDIR"])
            status = os.system("tar xf MDTF_"+os.environ["CASENAME"]+".tar")
         else:
            cwd = os.getcwd()
            os.system("ls -l "+cwd+os.environ["variab_dir"]+".tar")
      else:
         print "no WEBDIR set so leaving tar file here"
         cwd = os.getcwd()
         os.system("ls -l "+cwd+os.environ["variab_dir"]+".tar")
     

exit()
