# Import Python Packages
import numpy
import glob
from netCDF4 import Dataset
from convective_onset_diag_util import binning_tave,binning_qsat
from convective_onset_diag_util import generate_region_mask
from convective_onset_diag_util import calc_save_tave_qsat
from convective_onset_diag_util import preprocess_binning_saving
from convective_onset_diag_util import load_binning_output
from convective_onset_diag_util import plot_save_figure
import os
import json

print "LOADING USER SPECIFIED BINNING PARAMETERS"
### Create and read user specified parameters ###
os.system("python "+os.environ["VARCODE"]+"/"+"user_specified_binning_parameters.py")

with open(os.environ["VARCODE"]+"/"+"bin_parameters.json") as outfile:
    bin_data=json.load(outfile)

print "LOADING USER SPECIFIED PLOTTING PARAMETERS"
os.system("python "+os.environ["VARCODE"]+"/"+"user_specified_plotting_parameters.py")

with open(os.environ["VARCODE"]+"/"+"plot_parameters.json") as outfile:
    plot_data=json.load(outfile)

##########

if (bin_data["BIN_ANYWAY"] or len(bin_data["bin_output_list"])==0):

    print "BINNING"

    if bin_data["PREPROCESS_TA"]==1:
        print("Temperature Pre-processing Required!")
    if bin_data["SAVE_TAVE_QSAT"]==1:
        print("Pre-processed Temperature Fields (tave & qsat) will be saved!")

    ## Load & Pre-process Region Mask
    REGION,lat,lon=generate_region_mask(bin_data["REGION_MASK_DIR"]+"/"+bin_data["REGION_MASK_FILENAME"], bin_data["pr_list"][0])
    ret=preprocess_binning_saving(REGION,bin_data["args1"])

else: # BIN_ANYWAY=0 & binning_output exists
    ret=load_binning_output(bin_data["args2"])


# 
print "PLOTTING"
# 
plot_save_figure(ret,plot_data["args3"])
print "PLOTTING COMPLETE"

# move the plot to the proper place
#os.system("mv "+os.environ["WKDIR"]+"/*eof1.ps "+os.environ["WKDIR"]+"/MDTF_"+os.environ["CASENAME"]+"/"+os.environ["CASENAME"]+"/.")
os.system("mv "+ plot_data["FIG_OUTPUT_DIR"]+plot_data["FIG_OUTPUT_FILENAME"]+ " " + os.environ["WKDIR"]+"/MDTF_"+os.environ["CASENAME"]+"/"+os.environ["CASENAME"]+"/.")

print 'CREATING HTML'
# write links to html file (adapted from Jack Chen's code)
os.system("echo '<TABLE>' >> "+os.environ["WKDIR"]+"/MDTF_"+os.environ["CASENAME"]+"/variab.html")
# new row (TR)
os.system("echo '<TR>' >> "+os.environ["WKDIR"]+"/MDTF_"+os.environ["CASENAME"]+"/variab.html")
# header cells (TH)
os.system("echo '<TH ALIGH=LEFT><font color=navy> Convective onset diagnostics (Neelin group at UCLA)' >> "+os.environ["WKDIR"]+"/MDTF_"+os.environ["CASENAME"]+"/variab.html")
# header cells for each column (TH, TH)
os.system("echo '<TH ALIGH=LEFT>casename' >> "+os.environ["WKDIR"]+"/MDTF_"+os.environ["CASENAME"]+"/variab.html")
os.system("echo '<TH ALIGH=LEFT>OBS' >> "+os.environ["WKDIR"]+"/MDTF_"+os.environ["CASENAME"]+"/variab.html")
# new row (TR)
os.system("echo '<TR>' >> "+os.environ["WKDIR"]+"/MDTF_"+os.environ["CASENAME"]+"/variab.html")
# header and links to plots in each column (TH, TH, TH)
os.system("echo '<TH ALIGH=LEFT>Convective Diagnostics' >> "+os.environ["WKDIR"]+"/MDTF_"+os.environ["CASENAME"]+"/variab.html")
os.system("echo '<TH ALIGH=CENTER><A HREF=\"casename/onset_diag_output_AM4-2P_tave.png\">plot</A>' >> "+os.environ["WKDIR"]+"/MDTF_"+os.environ["CASENAME"]+"/variab.html")
os.system("echo '<TH ALIGH=CENTER><A HREF=\"obs/NCEP.natl.eof1.gif\">plot</A>' >> "+os.environ["WKDIR"]+"/MDTF_"+os.environ["CASENAME"]+"/variab.html")
os.system("echo '<TR>' >> "+os.environ["WKDIR"]+"/MDTF_"+os.environ["CASENAME"]+"/variab.html")
