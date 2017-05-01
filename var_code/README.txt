**************************************************************
PRECIP_ANALYSIS_PACKAGE
**************************************************************
Package of scripts to analyze and plot fast-process diagnostics for the transition to strong convection associated with the pickup of precipitation as a function of water vapor for a given temperature. Developed and used in references listed below (please cite the appropriate ones when user adaptation of this code leads to publication; Neelin et al. 2009 is the main reference for the temperature dependence of the precipitation onset).
An important interpretation to keep in mind is that under most of the conditions for which this is applied, the vertically integrated water vapor (column water vapor) is a proxy for the effect of water vapor on conditional instability of entraining convection (see Holloway and Neelin 2009 for examination of this in DOE ARM site in situ data, including vertical structures of water vapor). As a result, the water vapor value at which convective onset statistically occurs (as a function of temperature) provides a strong constraint on the representation of conditional instability, including entrainment in a model convective parameterization (Sahany et al. 2012, 2014).
It is important also to keep in mind that microwave precipitation rate retrievals are based on an empirical relationship associated with the effects of cloud water (Hilburn and Wentz 2008), and that the retrievals that high rain rate are not necessarily calibrated. Comparisons to models should be based on the intermediate interval of precipitation rate pickup, hence the use of the restricted range fit in this code. 

Original code written by Ole Peters (2008/2009 including binning script written in MATLAB and structure 
of plotting scripts in gnuplot).
Modifications and additions by Katrina Hales (2009-2014).

Overall there are two main sub-directories:
	PROCESS: read in model data, process into bins by region of temperature and water vapor 
		and write out to files in format ready for plotting
	FIT_and_PLOT: fit processed data to find critical values and plot key figures

**************************************************************
Steps:
**************************************************************
***
1) preprocess input data
***
The model output netcdf files are produced by script gen_6hrly.ncl 
(a copy included here for reference in directory PROCESS/INPUT_DATA, author: R.Neale).   
In this version of the analysis, 
the netcdf files (one variable, one year per file) are rewritten to MATLAB-format .mat 
files before running the analysis script, so those datafiles 
are included in PROCESS/INPUT_DATA/CCSM_MAT.  Can skip this step if modify binning script
to read netcdf files directly.

@@need to ssh the CCSM_MAT data to git.

***
2) bin data
***
This step runs the MATLAB script 'bin.m' in directory 'PROCESS'.  In 'PROCESS' directory with 'bin.m' need
regions map. This is a .mat formatted file that defines the desired regions on the same 
grid resolution as model data.  
The file included here uses tropical ocean basins, 20N-20S, 
excluding land points with 1-Western Pacific, 2-Eastern Pacific, 3-Atlantic, 4-Indian, 0-other.  
To use different regions, modify/replace REGIONS_ccsm4_288x86.mat. 
Also in directory with 'bin.m', need directory of model data input files in annual .mat file format 
named e.g. 'INPUT_DATA/CCSM_MAT/PREC_1992.mat' (from step 1).

To run bin.m there are several parameters that can be modified in the script. The default values 
and descriptions are in comments in the script.

Bin.m will produce binned data in two formats: (1) matlab-format .mat file of the main array 
containing the binned data and (2) column ascii files formatted for analysis/plotting with 
gnuplot (one file per region and temperature bin).

@@need to ssh regions file to git. And find regions_288x192.mat file to 
replace REGIONS_ccsm4_288x86.mat (same
information in file, but had tidied up).

***
3) quick look at data as needed
***
For most experiments, the default values are likely sufficient.  However, we currently take a quick look at the
temperature-precip bins to see the most populous temperature bins to find the appropriate range of temperature-
bins to plot.  Our plan is to automate this step by selecting the most populous temperature-bin and from that
value, include 2 temperature-bins less than it and 4 greater than it as a general guide.

***
4) calculate the 'restricted-range-fit'
***
The output of the binning (step 2) produces column ascii files ready for analysis/plotting with gnuplot 
(they are in directory: FIT_and_PLOT/GNUPLOTready*timerange*/).  
In directory FIT_and_PLOT, edit dataname, region and timerange settings in DATASETTINGS.gp.
The script calculate_fit.gp calculates 
the least squares fit for precipitation as a function of column water vapor and temperature
over the range of precipitation from 2.5mm/h to 6.0mm/h with a minimum
of 3 points and over a maximum range of CWV of 5mm [note, the minimum point requirement as been implemented
case-by-case so far and is not currently coded in the script].

The 'calculate_fit.gp' script saves the calculated critical values and 
amplitudes into files in directory 'FIT_VALUES' (it loads script 'print_fit_values.gp') and also plots the 
precipitation pickups and fits.

An alternate fitting method is included in script @alternate_fit.gs.  This requires more consideration of 
parameter selection on a case by case basis.  @This script needs more clean up.

***
5) plot figures
***
In directory FIT_and_PLOT, there are separate scripts for each of the three main figures:
	1) PLOTFIG_pickup.gp: plots pickup of precipitation vs cwv for the 
		temperatures selected along with the restricted range fit lines
	2) PLOTFIG_wc_qsh.gp: plots critical water vapor values and saturation values vs temperature
	3) PLOTFIG_num_precip.gp: plots number precipitating with Gaussian fits for the selected temperature bins

Each script looks to file 'DATASETTINGS.gp' to set parameters for selected region, dataset and timerange.
There are also supporting scripts of 'linesettings.gp' to set color and line characteristics for plotting and 
'cleanup_wcs.gp' to clear values of the fittings when iterating over multiple regions, etc.


**************************************************************
References:
Peters, O. and J. D. Neelin, 2006: Critical phenomena in atmospheric precipitation. Nature Physics, 2, 393-396, doi:10.1038/nphys314.

Holloway, C. E. and J. D. Neelin, 2009: Moisture vertical structure, column water vapor, and tropical deep convection. J. Atmos. Sci., 66, 1665-1683. doi: 10.1175/2008JAS2806.1

Neelin, J. D., O. Peters, and K. Hales, 2009: The transition to strong convection. J. Atmos. Sci., 66, 2367-2384.doi: 10.1175/2009JAS2962.1

Neelin, J. D., O. Peters, J. W.-B. Lin, K. Hales and C. E. Holloway, 2009: Rethinking convective quasi-equilibrium: observational constraints for stochastic convective schemes in climate models In Stochastic Physics and Climate Modelling, T. N. Palmer and P. D. Williams, eds. Cambridge University Press, Cambridge.

Sahany, S., J. D. Neelin, K. Hales, and R. Neale, 2012: Temperature-moisture dependence of the deep convective transition as a constraint on entrainment in climate models. J. Atmos. Sci., 69, 1340–1358, doi:10.1175/JAS-D-11-0164.1. [NSF AGS-1102838, NOAA NA11OAR4310099, DOE DE-SC0006739]

Sahany, S., J. D. Neelin, K. Hales and R. B. Neale, 2013: Deep Convective Onset Characteristics in the Community Climate System Model and Changes Under Global Warming. J. Clim., under review.
        
**************************************************************
