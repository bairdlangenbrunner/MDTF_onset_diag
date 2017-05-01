###### This is the file that creates the parameters 
##### for use by the binning and plotting scripts.

import json
import os

with open(os.environ["VARCODE"]+"/bin_parameters.json") as outfile:
    bin_data=json.load(outfile)
    
# ======================================================================
# START USER SPECIFIED SECTION
# ======================================================================
# Don't plot bins with PDF<PDF_THRESHOLD
PDF_THRESHOLD=1e-5 # default: 1e-5

# Don't plot tave/qsat with narrow cwv range (< CWV_RANGE_THRESHOLD*0.3 mm)
CWV_RANGE_THRESHOLD=60 # default: 60

# Don't plot tave/qsat with low conditional probability of precipitation
CP_THRESHOLD=0.2

FIG_OUTPUT_DIR=bin_data["BIN_OUTPUT_DIR"]
FIG_OUTPUT_FILENAME=bin_data["BIN_OUTPUT_FILENAME"]+".png"

# ======================================================================
# END USER SPECIFIED SECTION
# ======================================================================
#
# ======================================================================
# DO NOT MODIFY CODE BELOW UNLESS
# YOU KNOW WHAT YOU ARE DOING
# ======================================================================

data={}

data["PDF_THRESHOLD"]=PDF_THRESHOLD

data["CWV_RANGE_THRESHOLD"]=CWV_RANGE_THRESHOLD

data["CP_THRESHOLD"]=CP_THRESHOLD

data["FIG_OUTPUT_DIR"]=FIG_OUTPUT_DIR
data["FIG_OUTPUT_FILENAME"]=FIG_OUTPUT_FILENAME

data["args3"]=[ bin_data["CWV_BIN_WIDTH"],PDF_THRESHOLD,CWV_RANGE_THRESHOLD,\
                CP_THRESHOLD,bin_data["MODEL"],bin_data["REGION_STR"],bin_data["NUMBER_OF_REGIONS"],\
                bin_data["BULK_TROPOSPHERIC_TEMPERATURE_MEASURE"],bin_data["PRECIP_THRESHOLD"],\
                FIG_OUTPUT_DIR,FIG_OUTPUT_FILENAME ]

with open(os.environ["VARCODE"]+"/plot_parameters.json", "w") as outfile:
    json.dump(data, outfile)
