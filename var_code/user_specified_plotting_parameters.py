###### This is the file that creates the parameters 
##### for use by the binning and plotting scripts.

import json
import os

with open(os.environ["VARCODE"]+"/bin_parameters.json") as outfile:
    bin_data=json.load(outfile)
    
#####################################
###   User-specified Section      ###
###         for plotting script   ###
#####################################

PDF_THRESHOLD=1e-5

## Don"t plot tave with narrow cwv range (< default: 60*0.3 mm)
CWV_RANGE_THRESHOLD=60

## Don"t plot tave with low conditional probability of precipitation
CP_THRESHOLD=0.2

FIG_OUTPUT_DIR=bin_data["BIN_OUTPUT_DIR"]
FIG_OUTPUT_FILENAME="/"+os.environ["CASENAME"]+".onset_diag.png"


#####################################
###   End of                      ###
###     User-specified Section    ###
###         for plotting script   ###
#####################################



data={}

## Don"t plot bins with PDF<PDF_THRESHOLD (default: 1e-5)
data["PDF_THRESHOLD"]=PDF_THRESHOLD

## Don"t plot tave with narrow cwv range (< default: 60*0.3 mm)
data["CWV_RANGE_THRESHOLD"]=CWV_RANGE_THRESHOLD

## Don"t plot tave with low conditional probability of precipitation
data["CP_THRESHOLD"]=CP_THRESHOLD

data["FIG_OUTPUT_DIR"]=FIG_OUTPUT_DIR
data["FIG_OUTPUT_FILENAME"]=FIG_OUTPUT_FILENAME


data["args3"]=[ bin_data["CWV_BIN_WIDTH"],PDF_THRESHOLD,CWV_RANGE_THRESHOLD,\
                CP_THRESHOLD,bin_data["MODEL"],bin_data["REGION_STR"],bin_data["NUMBER_OF_REGIONS"],\
                bin_data["BULK_TROPOSPHERIC_TEMPERATURE_MEASURE"],bin_data["PRECIP_THRESHOLD"],\
                FIG_OUTPUT_DIR,FIG_OUTPUT_FILENAME ]

with open(os.environ["VARCODE"]+"/plot_parameters.json", "w") as outfile:
    json.dump(data, outfile)
