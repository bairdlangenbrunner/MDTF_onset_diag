# ======================================================================
# convective_transition_diag_model_v1r0.py
#
#   Version 1 revision 0 04/28/2017 Yi-Hung Kuo (UCLA)
#   Contributors: K. A. Schiro (UCLA), B. Langenbrunner (UCLA), F. Ahmed (UCLA), 
#    C. Martinez (UCLA), C.-C. (Jack) Chen (NCAR)
#   PI: J. David Neelin (UCLA)
#
#   Computes a set of Convective Transition Statistics following Neelin et al. (2009),
#    Schiro et al. (2016), Kuo et al. (2017, 201?)
#  
#   Generates plots of:
#    (1) conditional average precipitation 
#    (2) conditional probability of precipitation
#    (3) probability density function (PDF) of all events
#    (4) PDF of precipitating events 
#    all as a function of column water vapor (CWV) and bulk tropospheric temperature
#
# Bulk tropospheric temperature measures used include
#  (1) tave: mass-weighted column average temperature
#  (2) qsat: column-integrated saturation specific humidity
#  Choose one by setting BULK_TROPOSPHERIC_TEMPERATURE_MEASURE
#  in user_specified_binning_parameters.py
#
# tave & qsat are not standard model output yet, pre-processing calculates these two 
#  and saves them in the model output directory (if there is a permission issue, 
#  change PREPROCESSING_OUTPUT_DIR with related changes, or simply force 
#  data["SAVE_TAVE_QSAT"]=0, both in user_specified_binning_parameters.py)
#
# Defaults for binning choices, etc. that can be altered by user are in:
#  user_specified_binning_parameters.py
#
# Defaults for plotting choices that can be altered by user are in:
#  user_specified_plotting_parameters.py
# 
# To change regions over which binning computations are done, see
#  user_specified_binning_parameters.py &
#  generate_region_mask in convective_transition_diag_model_util.py
#  (and change var_data/region_0.25x0.25_GOP2.5deg.mat)
#  
# COPYLEFT Agreement TBD
# ======================================================================
# Import standard Python packages
import numpy
import glob
import os
import json
from netCDF4 import Dataset

# Import Python functions specific to Convective Transition Diagnostics
from convective_transition_diag_model_util import generate_region_mask
from convective_transition_diag_model_util import preprocess_binning_saving
from convective_transition_diag_model_util import load_binned_output
from convective_transition_diag_model_util import plot_save_figure

# ======================================================================
# Load user-specified parameters for BINNING and PLOTTING
# This is in the var_code folder under
#  user_specified_binning_parameters.py
#  & user_specified_plotting_parameters.py

print("Load user-specified binning parameters..."),

# Create and read user-specified parameters
os.system("python "+os.environ["VARCODE"]+"/"+"user_specified_binning_parameters.py")
with open(os.environ["VARCODE"]+"/"+"bin_parameters.json") as outfile:
    bin_data=json.load(outfile)
print("...Loaded!")

print("Load user-specified plotting parameters..."),
os.system("python "+os.environ["VARCODE"]+"/"+"user_specified_plotting_parameters.py")
with open(os.environ["VARCODE"]+"/"+"plot_parameters.json") as outfile:
    plot_data=json.load(outfile)
print("...Loaded!")

# ======================================================================
# Binned data, i.e., convective transition statistics binned in specified intervals of 
#  CWV and tropospheric temperature (in terms of tave or qsat), are saved to avoid 
#  redoing binning computation every time
# Check if binned data file exists in wkdir/casename/.../ from a previous computation
#  if so, skip binning; otherwise, bin data using model output
#  (see user_specified_binning_parameters.py for where the model output locate)

if (len(bin_data["bin_output_list"])==0 or bin_data["BIN_ANYWAY"]):

    print("Starting binning procedure...")

    if bin_data["PREPROCESS_TA"]==1:
        print("   Atmospheric temperature pre-processing required")
    if bin_data["SAVE_TAVE_QSAT"]==1:
        print("      Pre-processed temperature fields ("\
            +os.environ["TAVE_var"]+" & "+os.environ["QSAT_AVE_var"]\
            +") will be saved to "+bin_data["PREPROCESSING_OUTPUT_DIR"]+"/")

    # Load & pre-process region mask
    REGION=generate_region_mask(bin_data["REGION_MASK_DIR"]+"/"+bin_data["REGION_MASK_FILENAME"], bin_data["pr_list"][0])

    # Pre-process temperature (if necessary) & bin & save binned results
    binned_output=preprocess_binning_saving(REGION,bin_data["args1"])

else: # Binned data file exists & BIN_ANYWAY=False
    print("Binned output detected..."),
    binned_output=load_binned_output(bin_data["args2"])
    print("...Loaded!")
# ======================================================================
# Plot binning results & save the figure in wkdir/casename/.../
plot_save_figure(binned_output,plot_data["args3"])

# ======================================================================
# Create HTML linking to plots.
#  Done in working directory, moved to final location by mdtf.py
# Code below adapted from MDTF example by Chih-Chieh (Jack) Chen, NCAR
print('Creating HTML...'),

# remove binned outputs, if CLEAN = 1
if os.environ["CLEAN"] == "1":
    os.system("rm -f "+os.environ["WKDIR"]+"/MDTF_"+os.environ["CASENAME"]+"/"+os.environ["CASENAME"]+"/"+data["BIN_OUTPUT_FILENAME"]+".nc")

# copy plots of OBS 
os.system("cp "+os.environ["VARDATA"]+"/R2_TMIv7r1_200206_201405_res="+os.environ["RES"]+"_fillNrCWV_onset_diag_"+bin_data["TEMP_VAR"]+".png "+os.environ["WKDIR"]+"/MDTF_"+os.environ["CASENAME"]+"/obs/")

# write links to html file
os.system("echo '<TABLE>' >> "+os.environ["WKDIR"]+"/MDTF_"+os.environ["CASENAME"]+"/variab.html")
os.system("echo '<TR>' >> "+os.environ["WKDIR"]+"/MDTF_"+os.environ["CASENAME"]+"/variab.html")

os.system("echo '<TH ALIGH=LEFT><font color=navy> Convective Transition Statistics' >> "+os.environ["WKDIR"]+"/MDTF_"+os.environ["CASENAME"]+"/variab.html")
os.system("echo '<TH ALIGH=LEFT>casename' >> "+os.environ["WKDIR"]+"/MDTF_"+os.environ["CASENAME"]+"/variab.html")
os.system("echo '<TH ALIGH=LEFT>OBS' >> "+os.environ["WKDIR"]+"/MDTF_"+os.environ["CASENAME"]+"/variab.html")
os.system("echo '<TR>' >> "+os.environ["WKDIR"]+"/MDTF_"+os.environ["CASENAME"]+"/variab.html")
os.system("echo '<TH ALIGH=LEFT>Tropical Ocean Basins' >> "+os.environ["WKDIR"]+"/MDTF_"+os.environ["CASENAME"]+"/variab.html")
os.system("echo '<TH ALIGH=CENTER><A HREF=\"casename/"+plot_data["FIG_OUTPUT_FILENAME"]+"\">plot</A>' >> "+os.environ["WKDIR"]+"/MDTF_"+os.environ["CASENAME"]+"/variab.html")
os.system("echo '<TH ALIGH=CENTER><A HREF=\"obs/R2_TMIv7r1_200206_201405_res="+os.environ["RES"]+"_fillNrCWV_onset_diag_"+bin_data["TEMP_VAR"]+".png\">plot</A>' >> "+os.environ["WKDIR"]+"/MDTF_"+os.environ["CASENAME"]+"/variab.html")
os.system("echo '<TR>' >> "+os.environ["WKDIR"]+"/MDTF_"+os.environ["CASENAME"]+"/variab.html")
print('...Created!')
