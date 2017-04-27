###### This is the file that creates the parameters 
##### for use by the binning and plotting scripts.

import json
import os
import glob
data={}

#####################################
###   User-specified Section      ###
###          for binning script   ###
#####################################

### Model output directory & filename ###
MODEL="AM4-DCS"
MODEL_OUTPUT_DIR=os.environ["DATADIR"] # WHERE ORIGINAL MODEL DATA ARE LOCATED

# ======================================================================
# Specify how the model filename is structured below
#MODEL_FILENAME_PREFIX="atmos."

# ======================================================================
# Variable Names (import from mdtf.py)
PR_VAR=os.environ["PRECT_var"]
PRW_VAR=os.environ["CWV_var"]
TA_VAR=os.environ["T_3D_var"]
PRES_VAR=os.environ["level_var"]

# ======================================================================
# Region mask directory & filename
REGION_MASK_DIR=os.environ["VARDATA"]
REGION_MASK_FILENAME="region_0.25x0.25_GOP2.5deg.mat"

# ======================================================================
# Number of Regions
# Use anywhere from 1 to NUMBER_OF_REGIONS (default of 4)
NUMBER_OF_REGIONS=4
REGION_STR=["WPac","EPac","Atl","Ind"]

# ======================================================================
# Directory for saving pre-processed temperature fields
# tave [K]: Mass-weighted column average temperature
# qsat_ave [mm]: Column-integrated saturation specific humidity
PREPROCESSING_OUTPUT_DIR=os.environ["DATADIR"] # USER MUST HAVE WRITE PERMISSION HERE
TAVE_VAR=os.environ["TAVE_var"]
QSAT_AVE_VAR=os.environ["QSAT_AVE_var"]
PRES_VAR=os.environ["level_var"]

##### Give latitude and longitude names in file ####
LAT_VAR=os.environ["lat_var"]
LON_VAR=os.environ["lon_var"]

## Use 1:tave, or 2:qsat as Bulk Tropospheric Temperature Measure 
BULK_TROPOSPHERIC_TEMPERATURE_MEASURE=1

## Directory & Filename for saving binned results (netCDF4)
BIN_OUTPUT_FILENAME=os.environ["CASENAME"]+".onset_diag_output"
    
## Re-do binning even if binning output detected (default: False)
BIN_ANYWAY=False

## Column Water Vapor (CWV in mm) range & bin-width
# CWV bin centers are integral multiples of cwv_bin_width
CWV_BIN_WIDTH=0.3 # default=0.3 (following satellite retrieval product)
CWV_RANGE_MAX=90.0 # default=90 (75 for satellite retrieval product)

## Mass-weighted Column Average Temperature tave [K]
#   With 1K increment and integral bin centers
T_RANGE_MIN=260.0
T_RANGE_MAX=280.0
T_BIN_WIDTH=1.0

## Column-integrated Saturation Specific Humidity qsat [mm]
#   With bin centers = Q_RANGE_MIN + integer*Q_BIN_WIDTH
#  Satellite retrieval suggests T_BIN_WIDTH=1 
#   is approximately equivalent to Q_BIN_WIDTH=4.8
Q_RANGE_MIN=16.0
Q_RANGE_MAX=106.0
Q_BIN_WIDTH=4.5

## Define Column [hPa]
p_lev_bottom=1000
p_lev_top=200
# If model pressure levels are within dp-hPa neighborhood of 
#   column top/bottom, use model levels to define column instead
dp=1.0

## Number of time-steps in Temperature-preprocessing
#   Default: 1000 (use smaller numbers for limited memory)
time_idx_delta=1000

## Threshold value defining precipitating events [mm/hr]
PRECIP_THRESHOLD=0.25

# ======================================================================
# END USER SPECIFIED SECTION
# ======================================================================
#
# ======================================================================
# DO NOT MODIFY CODE BELOW UNLESS
# YOU KNOW WHAT YOU ARE DOING
# ======================================================================

data["MODEL"]=MODEL
data["MODEL_OUTPUT_DIR"]=MODEL_OUTPUT_DIR
data["PREPROCESSING_OUTPUT_DIR"]=PREPROCESSING_OUTPUT_DIR
#data["MODEL_FILENAME_PREFIX"]=MODEL_FILENAME_PREFIX

# data["PR_VAR"]=PR_VAR
# data["PRW_VAR"]=PRW_VAR
# data["TA_VAR"]=TA_VAR
# data["PRES_VAR"]=PRES_VAR

## Region mask directory & filename
data["REGION_MASK_DIR"]=REGION_MASK_DIR
data["REGION_MASK_FILENAME"]=REGION_MASK_FILENAME

## Number of Regions
# Use region 1 to NUMBER_OF_REGIONS in the mask
data["NUMBER_OF_REGIONS"]=NUMBER_OF_REGIONS
data["REGION_STR"]=REGION_STR

## Directory for saving pre-processed temperature fields
# tave [K]: Mass-weighted column average temperature
# qsat [mm]: Column-integrated saturation specific humidity
data["TAVE_VAR"]=TAVE_VAR
data["QSAT_AVE_VAR"]=QSAT_AVE_VAR
data["PRES_VAR"]=PRES_VAR

## Use 1:tave, or 2:qsat as Bulk Tropospheric Temperature Measure 
data["BULK_TROPOSPHERIC_TEMPERATURE_MEASURE"]=BULK_TROPOSPHERIC_TEMPERATURE_MEASURE

## Directory & Filename for saving binned results (netCDF4)
data["BIN_OUTPUT_DIR"] = os.environ["VARDATA"] #os.environ["WKDIR"]+"/MDTF_"+os.environ["CASENAME"]+"/"+os.environ["CASENAME"]#os.environ["VARDATA"]
data["BIN_OUTPUT_FILENAME"]=os.environ["CASENAME"]+".onset_diag_output"


if BULK_TROPOSPHERIC_TEMPERATURE_MEASURE==1:
    data["BIN_OUTPUT_FILENAME"]+="_"+TAVE_VAR
    data["TEMP_VAR"]=TAVE_VAR
elif BULK_TROPOSPHERIC_TEMPERATURE_MEASURE==2:
    data["BIN_OUTPUT_FILENAME"]+="_"+QSAT_AVE_VAR
    data["TEMP_VAR"]=QSAT_AVE_VAR

## Re-do binning even if binning output detected (default: 0)
data["BIN_ANYWAY"]=BIN_ANYWAY
    
## Column Water Vapor (CWV in mm) range & bin-width
# CWV bin centers are integral multiples of cwv_bin_width
data["CWV_BIN_WIDTH"]=CWV_BIN_WIDTH 
data["CWV_RANGE_MAX"]=CWV_RANGE_MAX

## Mass-weighted Column Average Temperature tave [K]
#   With 1K increment and integral bin centers
data["T_RANGE_MIN"]=T_RANGE_MIN
data["T_RANGE_MAX"]=T_RANGE_MAX
data["T_BIN_WIDTH"]=T_BIN_WIDTH

## Column-integrated Saturation Specific Humidity qsat [mm]
#   With bin centers = Q_RANGE_MIN + integer*Q_BIN_WIDTH
#  Satellite retrieval suggests T_BIN_WIDTH=1 
#   is approximately equivalent to Q_BIN_WIDTH=4.8
data["Q_RANGE_MIN"]=Q_RANGE_MIN
data["Q_RANGE_MAX"]=Q_RANGE_MAX
data["Q_BIN_WIDTH"]=Q_BIN_WIDTH

## Define Column [hPa]
data["p_lev_bottom"]=p_lev_bottom
data["p_lev_top"]=p_lev_top
# If model pressure levels are within dp-hPa neighborhood of 
#   column top/bottom, use model levels to define column instead
data["dp"]=dp

## Number of time-steps in Temperature-preprocessing
#   Default: 1000 (use smaller numbers for limited memory)
data["time_idx_delta"]=time_idx_delta

## Threshold value defining precipitating events [mm/hr]
data["PRECIP_THRESHOLD"]=PRECIP_THRESHOLD
data["bin_output_list"]=sorted(glob.glob(data["BIN_OUTPUT_DIR"]+"/"+data["BIN_OUTPUT_FILENAME"]+".nc"))

## List available netCDF files
# Assumes that the corresponding files in each list
#  have the same spatial/temporal coverage/resolution
pr_list=sorted(glob.glob(MODEL_OUTPUT_DIR+"/"+"*"+PR_VAR+"*"+".nc"))
prw_list=sorted(glob.glob(MODEL_OUTPUT_DIR+"/"+"*"+PRW_VAR+"*"+".nc"))
ta_list=sorted(glob.glob(MODEL_OUTPUT_DIR+"/"+"*"+TA_VAR+"*"+".nc"))

data["pr_list"] = pr_list
data["prw_list"] = prw_list
data["ta_list"] = ta_list

## Check for pre-processed TAVE & QSAT data
data["tave_list"]=sorted(glob.glob(MODEL_OUTPUT_DIR+"/"+"*"+TAVE_VAR+"*"+".nc"))
data["qsat_list"]=sorted(glob.glob(MODEL_OUTPUT_DIR+"/"+"*"+QSAT_AVE_VAR+"*"+".nc"))

if (BULK_TROPOSPHERIC_TEMPERATURE_MEASURE==1 and len(data["tave_list"])==0) \
    or (BULK_TROPOSPHERIC_TEMPERATURE_MEASURE==2 and len(data["qsat_list"])==0):
    data["PREPROCESS_TA"]=1
    data["SAVE_TAVE_QSAT"]=1 # default:1 (save pre-processed tave & qsat)
else:
    data["PREPROCESS_TA"]=0
    data["SAVE_TAVE_QSAT"]=0

### Taking care of function arguments for binning
data["args1"]=[ \
BULK_TROPOSPHERIC_TEMPERATURE_MEASURE, \
CWV_BIN_WIDTH, \
CWV_RANGE_MAX, \
T_RANGE_MIN, \
T_RANGE_MAX, \
T_BIN_WIDTH, \
Q_RANGE_MIN, \
Q_RANGE_MAX, \
Q_BIN_WIDTH, \
NUMBER_OF_REGIONS, \
pr_list, \
PR_VAR, \
prw_list, \
PRW_VAR, \
data["PREPROCESS_TA"], \
MODEL_OUTPUT_DIR, \
data["qsat_list"], \
QSAT_AVE_VAR, \
data["tave_list"], \
TAVE_VAR, \
ta_list, \
TA_VAR, \
PRES_VAR, \
MODEL, \
p_lev_bottom, \
p_lev_top, \
dp, \
time_idx_delta, \
data["SAVE_TAVE_QSAT"], \
PRECIP_THRESHOLD, \
data["BIN_OUTPUT_DIR"], \
data["BIN_OUTPUT_FILENAME"], \
LAT_VAR, \
LON_VAR ]

data["args2"]=[ \
data["bin_output_list"],\
TAVE_VAR,\
QSAT_AVE_VAR,\
BULK_TROPOSPHERIC_TEMPERATURE_MEASURE ]

with open(os.environ["VARCODE"]+"/bin_parameters.json", "w") as outfile:
    json.dump(data, outfile)
