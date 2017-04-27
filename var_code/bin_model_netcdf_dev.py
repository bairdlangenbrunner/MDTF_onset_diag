# Import Python Packages
import numpy
import glob
import os
import json
from netCDF4 import Dataset
from convective_onset_diag_util import generate_region_mask
from convective_onset_diag_util import preprocess_binning_saving
from convective_onset_diag_util import load_binning_output
from convective_onset_diag_util import plot_save_figure

# ======================================================================
# load user-specified parameters for BINNING and PLOTTING
# this is in the var_code folder under
# user_specified_binning_parameters.py and
# user_specified_plotting_parameters.py

print("Load user-specified binning parameters..."),
### Create and read user specified parameters ###
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
# check if binned data file exists in var_code
# if so, skip
# otherwise, bin data using the full files
if (bin_data["BIN_ANYWAY"] or len(bin_data["bin_output_list"])==0):

    print("Starting binning procedure...")

    if bin_data["PREPROCESS_TA"]==1:
        print("   Atmospheric temperature pre-processing required")
    if bin_data["SAVE_TAVE_QSAT"]==1:
        print("      Pre-processed temperature fields ("\
            +os.environ["TAVE_var"]+" & "+os.environ["QSAT_AVE_var"]\
            +") will be saved to "+bin_data["PREPROCESSING_OUTPUT_DIR"])

    ## Load & Pre-process Region Mask
    REGION,lat,lon=generate_region_mask(bin_data["REGION_MASK_DIR"]+"/"+bin_data["REGION_MASK_FILENAME"], bin_data["pr_list"][0])

    binning_output=preprocess_binning_saving(REGION,bin_data["args1"])

else: # BIN_ANYWAY=True & binning_output exists
    print("Binned output detected")
    binning_output=load_binning_output(bin_data["args2"])
    
# ======================================================================
# create plot
plot_save_figure(binning_output,plot_data["args3"])

# ======================================================================
# code below adapted from MDTF example by Chih-Chieh (Jack) Chen, NCAR

print('Creating HTML...'),
# remove binning outputs, if CLEAN = 1
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
