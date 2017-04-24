import numpy
import numba
from numba import jit,autojit
import scipy.io
from scipy.interpolate import NearestNDInterpolator
from netCDF4 import Dataset
#import matplotlib
import matplotlib.pyplot as mp
import matplotlib.cm as cm

@jit(nopython=True)
def binning_tave(lon_idx, CWV_BIN_WIDTH, NUMBER_OF_REGIONS, NUMBER_TEMP_BIN, NUMBER_CWV_BIN, PRECIP_THRESHOLD, REGION, CWV, RAIN, temp, QSAT, p0, p1, p2, pe, q0, q1):
    for lat_idx in numpy.arange(CWV.shape[1]):
        reg=REGION[lon_idx,lat_idx]
        if (reg>0 and reg<=NUMBER_OF_REGIONS):
            cwv_idx=CWV[:,lat_idx,lon_idx]
            rain=RAIN[:,lat_idx,lon_idx]
            temp_idx=temp[:,lat_idx,lon_idx]
            qsat=QSAT[:,lat_idx,lon_idx]
            for time_idx in numpy.arange(CWV.shape[0]):
                if (temp_idx[time_idx]<NUMBER_TEMP_BIN and temp_idx[time_idx]>=0 and cwv_idx[time_idx]<NUMBER_CWV_BIN):
                    p0[reg-1,cwv_idx[time_idx],temp_idx[time_idx]]+=1
                    p1[reg-1,cwv_idx[time_idx],temp_idx[time_idx]]+=rain[time_idx]
                    p2[reg-1,cwv_idx[time_idx],temp_idx[time_idx]]+=rain[time_idx]**2
                    if (rain[time_idx]>PRECIP_THRESHOLD):
                        pe[reg-1,cwv_idx[time_idx],temp_idx[time_idx]]+=1
                    if (cwv_idx[time_idx]+1>(0.6/CWV_BIN_WIDTH)*qsat[time_idx]):
                        q0[reg-1,temp_idx[time_idx]]+=1
                        q1[reg-1,temp_idx[time_idx]]+=qsat[time_idx]

@jit(nopython=True)
def binning_qsat(lon_idx, NUMBER_OF_REGIONS, NUMBER_TEMP_BIN, NUMBER_CWV_BIN, PRECIP_THRESHOLD, REGION, CWV, RAIN, temp, p0, p1, p2, pe):
    for lat_idx in numpy.arange(CWV.shape[1]):
        reg=REGION[lon_idx,lat_idx]
        if (reg>0 and reg<=NUMBER_OF_REGIONS):
            cwv_idx=CWV[:,lat_idx,lon_idx]
            rain=RAIN[:,lat_idx,lon_idx]
            temp_idx=temp[:,lat_idx,lon_idx]
            for time_idx in numpy.arange(CWV.shape[0]):
                if (temp_idx[time_idx]<NUMBER_TEMP_BIN and temp_idx[time_idx]>=0 and cwv_idx[time_idx]<NUMBER_CWV_BIN):
                    p0[reg-1,cwv_idx[time_idx],temp_idx[time_idx]]+=1
                    p1[reg-1,cwv_idx[time_idx],temp_idx[time_idx]]+=rain[time_idx]
                    p2[reg-1,cwv_idx[time_idx],temp_idx[time_idx]]+=rain[time_idx]**2
                    if (rain[time_idx]>PRECIP_THRESHOLD):
                        pe[reg-1,cwv_idx[time_idx],temp_idx[time_idx]]+=1

def generate_region_mask(region_mask_filename, model_netcdf_filename):
    ## Load & Pre-process Region Mask
    matfile=scipy.io.loadmat(region_mask_filename)
    lat_m=matfile["lat"]
    lon_m=matfile["lon"] # 0.125~359.875 deg
    region=matfile["region"]
    lon_m=numpy.append(lon_m,numpy.reshape(lon_m[0,:],(-1,1))+360,0)
    lon_m=numpy.append(numpy.reshape(lon_m[-2,:],(-1,1))-360,lon_m,0)
    region=numpy.append(region,numpy.reshape(region[0,:],(-1,lat_m.size)),0)
    region=numpy.append(numpy.reshape(region[-2,:],(-1,lat_m.size)),region,0)

    LAT,LON=numpy.meshgrid(lat_m,lon_m,sparse=False,indexing="xy")
    LAT=numpy.reshape(LAT,(-1,1))
    LON=numpy.reshape(LON,(-1,1))
    REGION=numpy.reshape(region,(-1,1))

    LATLON=numpy.squeeze(numpy.array((LAT,LON)))
    LATLON=LATLON.transpose()

    regMaskInterpolator=NearestNDInterpolator(LATLON,REGION)

    # Interpolate Region Mask onto Model Grid
    pr_netcdf=Dataset(model_netcdf_filename,"r")
    lon=numpy.asarray(pr_netcdf.variables["lon"][:],dtype="float")
    lat=numpy.asarray(pr_netcdf.variables["lat"][:],dtype="float")
    pr_netcdf.close()
    if lon[lon<0.0].size>0:
        lon[lon[lon<0.0]]+=360.0
    lat=lat[numpy.logical_and(lat>=-20.0,lat<=20.0)]

    LAT,LON=numpy.meshgrid(lat,lon,sparse=False,indexing="xy")
    LAT=numpy.reshape(LAT,(-1,1))
    LON=numpy.reshape(LON,(-1,1))
    LATLON=numpy.squeeze(numpy.array((LAT,LON)))
    LATLON=LATLON.transpose()
    REGION=numpy.zeros(LAT.size)
    for latlon_idx in numpy.arange(REGION.shape[0]):
        REGION[latlon_idx]=regMaskInterpolator(LATLON[latlon_idx,:])
    REGION=numpy.reshape(REGION.astype(int),(-1,lat.size))

    return REGION, lat, lon

def calc_save_tave_qsat(ta_netcdf_filename,TA_VAR,PRES_VAR,MODEL,\
                        p_lev_bottom,p_lev_top,dp,time_idx_delta,\
                        SAVE_TAVE_QSAT,TAVE_VAR,QSAT_VAR):
    ## Constants for calculating saturation vapor pressure
    Tk0 = 273.15 # Reference temperature.
    Es0 = 610.7 # Vapor pressure [Pa] at Tk0.
    Lv0 = 2500800 # Latent heat of evaporation at Tk0.
    cpv = 1869.4 # Isobaric specific heat capacity of water vapor at tk0.
    cl = 4218.0 # Specific heat capacity of liquid water at tk0.
    R = 8.3144 # Universal gas constant.
    Mw = 0.018015 # Molecular weight of water.
    Rv = R/Mw # Gas constant for water vapor.
    Ma = 0.028964 # Molecular weight of dry air.
    Rd = R/Ma # Gas constant for dry air.
    epsilon = Mw/Ma
    g = 9.80665
    ## Calculate tave & qsat
    # Column: 1000-200mb (+/- dp mb)
    ta_netcdf=Dataset(ta_netcdf_filename,"r")
    lat=numpy.asarray(ta_netcdf.variables["lat"][:],dtype="float")
    pfull=numpy.asarray(ta_netcdf.variables[PRES_VAR][:],dtype="float")
    FLIP_PRES=(pfull[1]-pfull[0]<0)
    if FLIP_PRES:
        pfull=numpy.flipud(pfull)
    tave=numpy.array([])
    qsat=numpy.array([])

    time_idx_start=0

    print("Start pre-processing "+ta_netcdf_filename)

    while (time_idx_start<ta_netcdf.variables[TA_VAR].shape[0]):
        if (time_idx_start+time_idx_delta<=ta_netcdf.variables[TA_VAR].shape[0]):
            time_idx_end=time_idx_start+time_idx_delta
        else:
            time_idx_end=ta_netcdf.variables[TA_VAR].shape[0]

        print("Integrate temperature field over "\
            +str(p_lev_bottom)+"-"+str(p_lev_top)+" hPa "\
            +"for time steps "\
            +str(time_idx_start)+"-"+str(time_idx_end))

        p_min=numpy.sum(pfull<=p_lev_top)-1
        if (pfull[p_min+1]<p_lev_top+dp):
            p_min=p_min+1
        p_max=numpy.sum(pfull<=p_lev_bottom)-1
        if (p_max+1<pfull.size and pfull[p_max]<p_lev_bottom-dp):
            p_max=p_max+1
        plev=numpy.copy(pfull[p_min:p_max+1])
        # ta[time,p,lat,lon]
        if FLIP_PRES:
            ta=numpy.asarray(ta_netcdf.variables[TA_VAR][time_idx_start:time_idx_end,pfull.size-(p_max+1):pfull.size-p_min,numpy.logical_and(lat>=-20.0,lat<=20.0),:],dtype="float")
            ta=numpy.fliplr(ta)
        else:
            ta=numpy.asarray(ta_netcdf.variables[TA_VAR][time_idx_start:time_idx_end,p_min:p_max+1,numpy.logical_and(lat>=-20.0,lat<=20.0),:],dtype="float")
        time_idx_start=time_idx_end
        p_max=p_max-p_min
        p_min=0

        if (plev[p_min]<p_lev_top-dp):
            # Update plev(p_min) <-- p_lev_top
            # AND ta(p_min) <-- ta(p_lev_top) by interpolation
            ta[:,p_min,:,:]=ta[:,p_min,:,:] \
                            +(p_lev_top-plev[p_min]) \
                            /(plev[p_min+1]-plev[p_min]) \
                            *(ta[:,p_min+1,:,:]-ta[:,p_min,:,:])
            plev[p_min]=p_lev_top

        if (plev[p_max]>p_lev_bottom+dp):
            # Update plev(p_max) <-- p_lev_bottom
            # AND Update ta(p_max) <-- ta(p_lev_bottom) by interpolation
            ta[:,p_max,:,:]=ta[:,p_max,:,:] \
                            +(p_lev_bottom-plev[p_max]) \
                            /(plev[p_max-1]-plev[p_max]) \
                            *(ta[:,p_max-1,:,:]-ta[:,p_max,:,:])
            plev[p_max]=p_lev_bottom

        if (plev[p_max]<p_lev_bottom-dp):
            # Update plev(p_max+1) <-- p_lev_bottom
            # AND ta(p_max+1) <-- ta(p_lev_bottom) by extrapolation
            ta=numpy.append(ta,numpy.expand_dims(ta[:,p_max,:,:] \
                            +(p_lev_bottom-plev[p_max]) \
                            /(plev[p_max]-plev[p_max-1]) \
                            *(ta[:,p_max,:,:]-ta[:,p_max-1,:,:]),1), \
                            axis=1)
            plev=numpy.append(plev,p_lev_bottom)
            p_max=p_max+1

        # Integrate between level p_min and p_max
        tave_interim=ta[:,p_min,:,:]*(plev[p_min+1]-plev[p_min])
        for pidx in range(p_min+1,p_max-1+1):
            tave_interim=tave_interim+ta[:,pidx,:,:]*(plev[pidx+1]-plev[pidx-1])
        tave_interim=tave_interim+ta[:,p_max,:,:]*(plev[p_max]-plev[p_max-1])
        tave_interim=numpy.squeeze(tave_interim)/2/(plev[p_max]-plev[p_min])
        if (tave.size==0):
            tave=tave_interim
        else:
            tave=numpy.append(tave,tave_interim,axis=0)

        # Integrate Saturation Specific Humidity between level p_min and p_max 
        Es=Es0*(ta/Tk0)**((cpv-cl)/Rv)*numpy.exp((Lv0+(cl-cpv)*Tk0)/Rv*(1/Tk0-1/ta))
        qsat_interim=Es[:,p_min,:,:]*(plev[p_min+1]-plev[p_min])/plev[p_min]
        for pidx in range(p_min+1,p_max-1+1):
            qsat_interim=qsat_interim+Es[:,pidx,:,:]*(plev[pidx+1]-plev[pidx-1])/plev[pidx]
        qsat_interim=qsat_interim+Es[:,p_max,:,:]*(plev[p_max]-plev[p_max-1])/plev[p_max]
        qsat_interim=(epsilon/2/g)*qsat_interim
        if (qsat.size==0):
            qsat=qsat_interim
        else:
            qsat=numpy.append(qsat,qsat_interim,axis=0)

    ta_netcdf.close()
    # End-while time_idx_start

    print(ta_netcdf_filename+" pre-processed!")

    ## Save Pre-Processed tave & qsat Fields
    if SAVE_TAVE_QSAT==1:
        ta_netcdf=Dataset(ta_netcdf_filename,"r")
        time=ta_netcdf.variables["time"]
        longitude=numpy.asarray(ta_netcdf.variables["lon"][:],dtype="float")
        latitude=numpy.asarray(ta_netcdf.variables["lat"][:],dtype="float")
        latitude=latitude[numpy.logical_and(latitude>=-20.0,latitude<=20.0)]

        # Save 1000-200mb Column Average Temperature as tave
        tave_output_netcdf=Dataset(ta_netcdf_filename.replace(TA_VAR,TAVE_VAR),"w",format="NETCDF4")
        tave_output_description=str(p_lev_bottom)+"-"+str(p_lev_top)+" hPa "\
                                    +"Mass-Weighted Column Average Temperature for "+MODEL
        tave_output_netcdf.source="Convective Onset Statistics Diagnostic Package \
        - as part of the NOAA Model Diagnostic Task Force (MDTF) effort"

        lon_dim=tave_output_netcdf.createDimension("lon",len(longitude))
        lon_val=tave_output_netcdf.createVariable("lon",numpy.float64,("lon",))
        lon_val.units="degree"
        lon_val[:]=longitude

        lat_dim=tave_output_netcdf.createDimension("lat",len(latitude))
        lat_val=tave_output_netcdf.createVariable("lat",numpy.float64,("lat",))
        lat_val.units="degree_north"
        lat_val[:]=latitude

        time_dim=tave_output_netcdf.createDimension("time",None)
        time_val=tave_output_netcdf.createVariable("time",numpy.float64,("time",))
        time_val.units=time.units
        time_val[:]=time[:]

        tave_val=tave_output_netcdf.createVariable("tave",numpy.float64,("time","lat","lon"))
        tave_val.units="K"
        tave_val[:,:,:]=tave

        tave_output_netcdf.close()

        print(ta_netcdf_filename.replace(TA_VAR,TAVE_VAR)+" saved!")

        # Save 1000-200mb Column-integrated Saturation Specific Humidity as qsat
        qsat_output_netcdf=Dataset(ta_netcdf_filename.replace(TA_VAR,QSAT_VAR),"w",format="NETCDF4")
        qsat_output_description=str(p_lev_bottom)+"-"+str(p_lev_top)+" hPa "\
                                    +"Column-integrated Saturation Specific Humidity for "+MODEL
        qsat_output_netcdf.source="Convective Onset Statistics Diagnostic Package \
        - as part of the NOAA Model Diagnostic Task Force (MDTF) effort"

        lon_dim=qsat_output_netcdf.createDimension("lon",len(longitude))
        lon_val=qsat_output_netcdf.createVariable("lon",numpy.float64,("lon",))
        lon_val.units="degree"
        lon_val[:]=longitude

        lat_dim=qsat_output_netcdf.createDimension("lat",len(latitude))
        lat_val=qsat_output_netcdf.createVariable("lat",numpy.float64,("lat",))
        lat_val.units="degree_north"
        lat_val[:]=latitude

        time_dim=qsat_output_netcdf.createDimension("time",None)
        time_val=qsat_output_netcdf.createVariable("time",numpy.float64,("time",))
        time_val.units=time.units
        time_val[:]=time[:]

        qsat_val=qsat_output_netcdf.createVariable("qsat",numpy.float64,("time","lat","lon"))
        qsat_val.units="mm"
        qsat_val[:,:,:]=qsat

        qsat_output_netcdf.close()

        print(ta_netcdf_filename.replace(TA_VAR,QSAT_VAR)+" saved!")

        ta_netcdf.close()
    # End-if SAVE_TAVE_QSAT==1

    return tave, qsat
###################################################################################################
###################################################################################################
###################################################################################################
    
def preprocess_binning_saving(REGION,*argsv):
    ## ALLOCATE VARIABLES FOR EACH ARGUMENT ##
    
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
    PREPROCESS_TA, \
    qsat_list, \
    QSAT_VAR, \
    tave_list, \
    TAVE_VAR, \
    ta_list, \
    TA_VAR, \
    PRES_VAR, \
    MODEL, \
    p_lev_bottom, \
    p_lev_top, \
    dp, \
    time_idx_delta, \
    SAVE_TAVE_QSAT, \
    PRECIP_THRESHOLD, \
    BIN_OUTPUT_DIR, \
    BIN_OUTPUT_FILENAME, \
    LAT_VAR, \
    LON_VAR = argsv[0]
    ## Allocate Memory for Arrays for Binning Output
    
    # Define Bin Centers
    cwv_bin_center=numpy.arange(CWV_BIN_WIDTH,CWV_RANGE_MAX+CWV_BIN_WIDTH,CWV_BIN_WIDTH)
    
    # Bulk Tropospheric Temperature Measure (1:tave, or 2:qsat)
    if BULK_TROPOSPHERIC_TEMPERATURE_MEASURE==1:
        tave_bin_center=numpy.arange(T_RANGE_MIN,T_RANGE_MAX+T_BIN_WIDTH,T_BIN_WIDTH)
        temp_bin_center=tave_bin_center
        temp_bin_width=T_BIN_WIDTH
    elif BULK_TROPOSPHERIC_TEMPERATURE_MEASURE==2:
        qsat_bin_center=numpy.arange(Q_RANGE_MIN,Q_RANGE_MAX+Q_BIN_WIDTH,Q_BIN_WIDTH)
        temp_bin_center=qsat_bin_center
        temp_bin_width=Q_BIN_WIDTH
    
    NUMBER_CWV_BIN=cwv_bin_center.size
    NUMBER_TEMP_BIN=temp_bin_center.size
    temp_offset=temp_bin_center[0]-0.5*temp_bin_width

    # Allocate Memory for Arrays
    P0=numpy.zeros((NUMBER_OF_REGIONS,NUMBER_CWV_BIN,NUMBER_TEMP_BIN))
    P1=numpy.zeros((NUMBER_OF_REGIONS,NUMBER_CWV_BIN,NUMBER_TEMP_BIN))
    P2=numpy.zeros((NUMBER_OF_REGIONS,NUMBER_CWV_BIN,NUMBER_TEMP_BIN))
    PE=numpy.zeros((NUMBER_OF_REGIONS,NUMBER_CWV_BIN,NUMBER_TEMP_BIN))
    if BULK_TROPOSPHERIC_TEMPERATURE_MEASURE==1:
        Q0=numpy.zeros((NUMBER_OF_REGIONS,NUMBER_TEMP_BIN))
        Q1=numpy.zeros((NUMBER_OF_REGIONS,NUMBER_TEMP_BIN))

    ## Binning by calling functions in binning_numba_util.py
    # Pre-process temperature fields & save if necessary

    for li in numpy.arange(len(pr_list)):

        pr_netcdf=Dataset(pr_list[li],"r")
        lat=numpy.asarray(pr_netcdf.variables[LAT_VAR][:],dtype="float")
        pr=numpy.asarray(pr_netcdf.variables[PR_VAR][:,:,:],dtype="float")
        pr_netcdf.close()
        pr=pr[:,numpy.logical_and(lat>=-20.0,lat<=20.0),:]*3600
        print(pr_list[li]+" LOADED")
        
        prw_netcdf=Dataset(prw_list[li],"r")
        lat=numpy.asarray(prw_netcdf.variables[LAT_VAR][:],dtype="float")
        prw=numpy.asarray(prw_netcdf.variables[PRW_VAR][:,:,:],dtype="float")
        prw_netcdf.close()
        prw=prw[:,numpy.logical_and(lat>=-20.0,lat<=20.0),:]
        print(prw_list[li]+" LOADED")
        
        if PREPROCESS_TA==0:
            qsat_netcdf=Dataset(qsat_list[li],"r")
            lat=numpy.asarray(qsat_netcdf.variables[LAT_VAR][:],dtype="float")
            qsat=numpy.asarray(qsat_netcdf.variables[QSAT_VAR][:,:,:],dtype="float")
            qsat_netcdf.close()
            qsat=qsat[:,numpy.logical_and(lat>=-20.0,lat<=20.0),:]
            
            print(qsat_list[li]+" LOADED")
            
            if BULK_TROPOSPHERIC_TEMPERATURE_MEASURE==1:
                tave_netcdf=Dataset(tave_list[li],"r")
                lat=numpy.asarray(tave_netcdf.variables[LAT_VAR][:],dtype="float")
                tave=numpy.asarray(tave_netcdf.variables[TAVE_VAR][:,:,:],dtype="float")
                tave_netcdf.close()
                tave=tave[:,numpy.logical_and(lat>=-20.0,lat<=20.0),:]
                
                print(tave_list[li]+" LOADED")
                
        else: # PREPROCESS_TA=1
            tave,qsat=calc_save_tave_qsat(ta_list[li],TA_VAR,PRES_VAR,MODEL,\
                                          p_lev_bottom,p_lev_top,dp,time_idx_delta,\
                                          SAVE_TAVE_QSAT,TAVE_VAR,QSAT_VAR)
        # End-if PREPROCESS_TA==1
        
        print("BINNING...")
        
        ### Start binning
        CWV=prw/CWV_BIN_WIDTH-0.5
        CWV=CWV.astype(int)
        RAIN=pr
        
        ### WHAT ABOUT WHEN THERE IS MISSING RAIN? 
        RAIN[RAIN<0]=0
        QSAT=qsat
        if BULK_TROPOSPHERIC_TEMPERATURE_MEASURE==1:
            TAVE=tave
            temp=(TAVE-temp_offset)/temp_bin_width
        elif BULK_TROPOSPHERIC_TEMPERATURE_MEASURE==2:
            temp=(QSAT-temp_offset)/temp_bin_width
        temp=temp.astype(int)

        for lon_idx in numpy.arange(CWV.shape[2]):
            p0=numpy.zeros((NUMBER_OF_REGIONS,NUMBER_CWV_BIN,NUMBER_TEMP_BIN))
            p1=numpy.zeros((NUMBER_OF_REGIONS,NUMBER_CWV_BIN,NUMBER_TEMP_BIN))
            p2=numpy.zeros((NUMBER_OF_REGIONS,NUMBER_CWV_BIN,NUMBER_TEMP_BIN))
            pe=numpy.zeros((NUMBER_OF_REGIONS,NUMBER_CWV_BIN,NUMBER_TEMP_BIN))
            if BULK_TROPOSPHERIC_TEMPERATURE_MEASURE==1:
                q0=numpy.zeros((NUMBER_OF_REGIONS,NUMBER_TEMP_BIN))
                q1=numpy.zeros((NUMBER_OF_REGIONS,NUMBER_TEMP_BIN))
                binning_tave(lon_idx, CWV_BIN_WIDTH, \
                            NUMBER_OF_REGIONS, NUMBER_TEMP_BIN, NUMBER_CWV_BIN, PRECIP_THRESHOLD, \
                            REGION, CWV, RAIN, temp, QSAT, \
                            p0, p1, p2, pe, q0, q1)
            elif BULK_TROPOSPHERIC_TEMPERATURE_MEASURE==2:
                binning_qsat(lon_idx, \
                            NUMBER_OF_REGIONS, NUMBER_TEMP_BIN, NUMBER_CWV_BIN, PRECIP_THRESHOLD, \
                            REGION, CWV, RAIN, temp, \
                            p0, p1, p2, pe)
            P0+=p0
            P1+=p1
            P2+=p2
            PE+=pe
            if BULK_TROPOSPHERIC_TEMPERATURE_MEASURE==1:
                Q0+=q0
                Q1+=q1
        # end-for lon_idx

        print("BINNING FOR CURRENT FILE COMPLETE")
        
    print("TOTAL BINNING COMPLETE")

    ## Save Binning Results
    if (BULK_TROPOSPHERIC_TEMPERATURE_MEASURE==1):
        bin_output_netcdf=Dataset(BIN_OUTPUT_DIR+"/"+BIN_OUTPUT_FILENAME+".nc","w",format="NETCDF4")
    elif (BULK_TROPOSPHERIC_TEMPERATURE_MEASURE==2):
        bin_output_netcdf=Dataset(BIN_OUTPUT_DIR+"/"+BIN_OUTPUT_FILENAME+".nc","w",format="NETCDF4")
        
    bin_output_description="Convective Onset Statistics for "+MODEL
    bin_output_netcdf.source="Convective Onset Statistics Diagnostic Package \
    - as part of the NOAA Model Diagnostic Task Force (MDTF) effort"

    region=bin_output_netcdf.createDimension("region",NUMBER_OF_REGIONS)
    reg=bin_output_netcdf.createVariable("region",numpy.float64,("region",))
    reg=numpy.arange(1,NUMBER_OF_REGIONS+1)

    cwv=bin_output_netcdf.createDimension("cwv",len(cwv_bin_center))
    prw=bin_output_netcdf.createVariable("cwv",numpy.float64,("cwv",))
    prw.units="mm"
    prw[:]=cwv_bin_center

    if (BULK_TROPOSPHERIC_TEMPERATURE_MEASURE==1):
        tave=bin_output_netcdf.createDimension(TAVE_VAR,len(tave_bin_center))
        temp=bin_output_netcdf.createVariable("tave",numpy.float64,(TAVE_VAR,))
        temp.units="K"
        temp[:]=tave_bin_center

        p0=bin_output_netcdf.createVariable("P0",numpy.float64,("region","cwv",TAVE_VAR))
        p0[:,:,:]=P0

        p1=bin_output_netcdf.createVariable("P1",numpy.float64,("region","cwv",TAVE_VAR))
        p1.units="mm/hr"
        p1[:,:,:]=P1

        p2=bin_output_netcdf.createVariable("P2",numpy.float64,("region","cwv",TAVE_VAR))
        p2.units="mm^2/hr^2"
        p2[:,:,:]=P2

        pe=bin_output_netcdf.createVariable("PE",numpy.float64,("region","cwv",TAVE_VAR))
        pe[:,:,:]=PE

        q0=bin_output_netcdf.createVariable("Q0",numpy.float64,("region",TAVE_VAR))
        q0[:,:]=Q0

        q1=bin_output_netcdf.createVariable("Q1",numpy.float64,("region",TAVE_VAR))
        q1.units="mm"
        q1[:,:]=Q1

    elif (BULK_TROPOSPHERIC_TEMPERATURE_MEASURE==2):
        qsat=bin_output_netcdf.createDimension(QSAT_VAR,len(qsat_bin_center))
        temp=bin_output_netcdf.createVariable("qsat",numpy.float64,(QSAT_VAR,))
        temp.units="mm"
        temp[:]=qsat_bin_center

        p0=bin_output_netcdf.createVariable("P0",numpy.float64,("region","cwv",QSAT_VAR))
        p0[:,:,:]=P0

        p1=bin_output_netcdf.createVariable("P1",numpy.float64,("region","cwv",QSAT_VAR))
        p1.units="mm/hr"
        p1[:,:,:]=P1

        p2=bin_output_netcdf.createVariable("P2",numpy.float64,("region","cwv",QSAT_VAR))
        p2.units="mm^2/hr^2"
        p2[:,:,:]=P2

        pe=bin_output_netcdf.createVariable("PE",numpy.float64,("region","cwv",QSAT_VAR))
        pe[:,:,:]=PE

    bin_output_netcdf.close()

    print("BINNING RESULTS SAVED")

    if (BULK_TROPOSPHERIC_TEMPERATURE_MEASURE==1):    
        return cwv_bin_center,tave_bin_center,P0,P1,P2,PE,Q0,Q1
    elif (BULK_TROPOSPHERIC_TEMPERATURE_MEASURE==2):
        return cwv_bin_center,qsat_bin_center,P0,P1,P2,PE,[],[]
###################################################################################################
###################################################################################################
###################################################################################################
def load_binning_output(*argsv):

    bin_output_list,\
    TAVE_VAR,\
    QSAT_VAR,\
    BULK_TROPOSPHERIC_TEMPERATURE_MEASURE=argsv[0]
    bin_output_netcdf=Dataset(bin_output_list[0],"r")

    cwv_bin_center=numpy.asarray(bin_output_netcdf.variables["cwv"][:],dtype="float")
    P0=numpy.asarray(bin_output_netcdf.variables["P0"][:,:,:],dtype="float")
    P1=numpy.asarray(bin_output_netcdf.variables["P1"][:,:,:],dtype="float")
    P2=numpy.asarray(bin_output_netcdf.variables["P2"][:,:,:],dtype="float")
    PE=numpy.asarray(bin_output_netcdf.variables["PE"][:,:,:],dtype="float")

    if (BULK_TROPOSPHERIC_TEMPERATURE_MEASURE==1):
        temp_bin_center=numpy.asarray(bin_output_netcdf.variables[TAVE_VAR][:],dtype="float")
        Q0=numpy.asarray(bin_output_netcdf.variables["Q0"][:,:],dtype="float")
        Q1=numpy.asarray(bin_output_netcdf.variables["Q1"][:,:],dtype="float") 
    elif (BULK_TROPOSPHERIC_TEMPERATURE_MEASURE==2):
        temp_bin_center=numpy.asarray(bin_output_netcdf.variables[QSAT_VAR][:],dtype="float")
        Q0=[]
        Q1=[]

    bin_output_netcdf.close()

    print("Binning Results Loaded!") 

    return cwv_bin_center,temp_bin_center,P0,P1,P2,PE,Q0,Q1
###################################################################################################
###################################################################################################
###################################################################################################
def plot_save_figure(ret,*argsv1):

    cwv_bin_center,\
    temp_bin_center,\
    P0,\
    P1,\
    P2,\
    PE,\
    Q0,\
    Q1=ret
    
    CWV_BIN_WIDTH,\
    PDF_THRESHOLD,\
    CWV_RANGE_THRESHOLD,\
    CP_THRESHOLD,\
    MODEL,\
    REGION_STR,\
    NUMBER_OF_REGIONS,\
    BULK_TROPOSPHERIC_TEMPERATURE_MEASURE,\
    PRECIP_THRESHOLD,\
    FIG_OUTPUT_DIR,\
    FIG_OUTPUT_FILENAME=argsv1[0]

    ## Post-binning Processing before Plotting
    P0[P0==0.0]=numpy.nan
    P=P1/P0
    CP=PE/P0
    PDF=numpy.zeros(P0.shape)
    for reg in numpy.arange(P0.shape[0]):
        PDF[reg,:,:]=P0[reg,:,:]/numpy.nansum(P0[reg,:,:])/CWV_BIN_WIDTH
    # Bins with PDF>PDF_THRESHOLD
    pdf_gt_th=numpy.zeros(PDF.shape)
    with numpy.errstate(invalid="ignore"):
        pdf_gt_th[PDF>PDF_THRESHOLD]=1

    # Indicator of (temp,reg) with wide CWV range
    t_reg_I=(numpy.squeeze(numpy.sum(pdf_gt_th,axis=1))>CWV_RANGE_THRESHOLD)

    # Copy P1, CP into p1, cp for (temp,reg) with "wide CWV range" & "large PDF"
    p1=numpy.zeros(P1.shape)
    cp=numpy.zeros(CP.shape)
    for reg in numpy.arange(P1.shape[0]):
        for Tidx in numpy.arange(P1.shape[2]):
            if t_reg_I[reg,Tidx]:
                p1[reg,:,Tidx]=P[reg,:,Tidx]
                cp[reg,:,Tidx]=CP[reg,:,Tidx]
    p1[pdf_gt_th==0]=numpy.nan
    cp[pdf_gt_th==0]=numpy.nan
    pdf=PDF

    for reg in numpy.arange(P1.shape[0]):
        for Tidx in numpy.arange(P1.shape[2]):
            if (t_reg_I[reg,Tidx] and cp[reg,:,Tidx][cp[reg,:,Tidx]>=0.0].size>0):
                if (numpy.max(cp[reg,:,Tidx][cp[reg,:,Tidx]>=0])<CP_THRESHOLD):
                    t_reg_I[reg,Tidx]=False
            else:
                t_reg_I[reg,Tidx]=False
                
    for reg in numpy.arange(P1.shape[0]):
        for Tidx in numpy.arange(P1.shape[2]):
            if (~t_reg_I[reg,Tidx]):
                p1[reg,:,Tidx]=numpy.nan
                cp[reg,:,Tidx]=numpy.nan
                pdf[reg,:,Tidx]=numpy.nan
    pdf_pe=pdf*cp

    # Temperature range for plotting
    TEMP_MIN=numpy.where(numpy.sum(t_reg_I,axis=0)>=2)[0][0]
    TEMP_MAX=numpy.where(numpy.sum(t_reg_I,axis=0)>=2)[0][-1]

    ##### Plot #####
    # create color map
    # choose from maps here:
    # http://matplotlib.org/examples/color/colormaps_reference.html
    scatter_colors = cm.jet(numpy.linspace(0,1,TEMP_MAX-TEMP_MIN+1,endpoint=True))
    # scatter_colors = cm.plasma(numpy.linspace(0,1,number_of_bins+1,endpoint=True))

    axes_fontsize = 12 # size of font in all plots
    legend_fontsize = 9
    marker_size = 40 # size of markers in scatter plots
    xtick_pad = 10 # padding between x tick labels and actual plot

    # create figure canvas
    fig = mp.figure(figsize=(14,12))

    for reg in numpy.arange(NUMBER_OF_REGIONS):
        # create figure 1
        ax1 = fig.add_subplot(NUMBER_OF_REGIONS,4,1+reg*NUMBER_OF_REGIONS)
        ax1.set_xlim(10,80)
        ax1.set_ylim(0,8)
        ax1.set_xticks([10,20,30,40,50,60,70,80])
        ax1.set_yticks([0,1,2,3,4,5,6,7,8])
        ax1.tick_params(labelsize=axes_fontsize)
        ax1.tick_params(axis="x", pad=10)
        for Tidx in numpy.arange(TEMP_MIN,TEMP_MAX+1):
            if t_reg_I[reg,Tidx]:
                if (BULK_TROPOSPHERIC_TEMPERATURE_MEASURE==1):
                    ax1.scatter(cwv_bin_center,p1[reg,:,Tidx],\
                                edgecolor="none",facecolor=scatter_colors[Tidx-TEMP_MIN,:],\
                                s=marker_size,clip_on=True,zorder=3,\
                                label="{:.0f}".format(temp_bin_center[Tidx]))
                elif (BULK_TROPOSPHERIC_TEMPERATURE_MEASURE==2):
                    ax1.scatter(cwv_bin_center,p1[reg,:,Tidx],\
                                edgecolor="none",facecolor=scatter_colors[Tidx-TEMP_MIN,:],\
                                s=marker_size,clip_on=True,zorder=3,\
                                label="{:.1f}".format(temp_bin_center[Tidx]))
        ax1.set_ylabel("Precip (mm hr$^-$$^1$)", fontsize=axes_fontsize)
        ax1.set_xlabel("CWV (mm)", fontsize=axes_fontsize)
        ax1.grid()
        ax1.set_axisbelow(True)

        handles, labels = ax1.get_legend_handles_labels()
        leg = ax1.legend(handles, labels, fontsize=axes_fontsize, bbox_to_anchor=(0.05,0.95), \
                        bbox_transform=ax1.transAxes, loc="upper left", borderaxespad=0, labelspacing=0.1, \
                        fancybox=False,scatterpoints=1,  framealpha=0, borderpad=0, \
                        handletextpad=0.1, markerscale=1, ncol=1, columnspacing=0.25)

        # create figure 2 (probability pickup)
        ax2 = fig.add_subplot(NUMBER_OF_REGIONS,4,2+reg*NUMBER_OF_REGIONS)
        ax2.set_xlim(10,80)
        ax2.set_ylim(0,1)
        ax2.set_xticks([10,20,30,40,50,60,70,80])
        ax2.set_yticks([0.0,0.2,0.4,0.6,0.8,1.0])
        ax2.tick_params(labelsize=axes_fontsize)
        ax2.tick_params(axis="x", pad=xtick_pad)
        for Tidx in numpy.arange(TEMP_MIN,TEMP_MAX+1):
            if t_reg_I[reg,Tidx]:
                ax2.scatter(cwv_bin_center,cp[reg,:,Tidx],\
                            edgecolor="none",facecolor=scatter_colors[Tidx-TEMP_MIN,:],\
                            s=marker_size,clip_on=True,zorder=3)
        ax2.set_ylabel("Probability of Precip", fontsize=axes_fontsize)
        ax2.set_xlabel("CWV (mm)", fontsize=axes_fontsize)
        ax2.text(0.05, 0.95, MODEL, transform=ax2.transAxes, fontsize=12, fontweight="bold", verticalalignment="top")
        ax2.text(0.05, 0.85, REGION_STR[reg], transform=ax2.transAxes, fontsize=12, fontweight="bold", verticalalignment="top")
        ax2.grid()
        ax2.set_axisbelow(True)

        # create figure 3 (normalized PDF)
        ax3 = fig.add_subplot(NUMBER_OF_REGIONS,4,3+reg*NUMBER_OF_REGIONS)
        ax3.set_yscale("log")
        ax3.set_ylim(1e-5,5e-2)
        ax3.set_xlim(10,80)
        ax3.set_xticks([10,20,30,40,50,60,70,80])
        ax3.tick_params(labelsize=axes_fontsize)
        ax3.tick_params(axis="x", pad=xtick_pad)
        for Tidx in numpy.arange(TEMP_MIN,TEMP_MAX+1):
            if t_reg_I[reg,Tidx]:
                ax3.scatter(cwv_bin_center,PDF[reg,:,Tidx],\
                            edgecolor="none",facecolor=scatter_colors[Tidx-TEMP_MIN,:],\
                            s=marker_size,clip_on=True,zorder=3)
        ax3.set_ylabel("PDF (mm$^-$$^1$)", fontsize=axes_fontsize)
        ax3.set_xlabel("CWV (mm)", fontsize=axes_fontsize)
        ax3.grid()
        ax3.set_axisbelow(True)

        # create figure 4 (normalized PDF - precipitation)
        ax4 = fig.add_subplot(NUMBER_OF_REGIONS,4,4+reg*NUMBER_OF_REGIONS)
        ax4.set_yscale("log")
        ax4.set_ylim(1e-5,5e-2)
        ax4.set_xlim(10,80)
        ax4.set_xticks([10,20,30,40,50,60,70,80])
        ax4.tick_params(labelsize=axes_fontsize)
        ax4.tick_params(axis="x", pad=xtick_pad)
        for Tidx in numpy.arange(TEMP_MIN,TEMP_MAX+1):
            if t_reg_I[reg,Tidx]:
                ax4.scatter(cwv_bin_center,pdf_pe[reg,:,Tidx],\
                            edgecolor="none",facecolor=scatter_colors[Tidx-TEMP_MIN,:],\
                            s=marker_size,clip_on=True,zorder=3)
        ax4.set_ylabel("PDF (mm$^-$$^1$)", fontsize=axes_fontsize)
        ax4.set_xlabel("CWV (mm)", fontsize=axes_fontsize)
        ax4.text(0.05, 0.95, "Precip > "+str(PRECIP_THRESHOLD)+" mm hr$^-$$^1$" , transform=ax4.transAxes, fontsize=12, verticalalignment="top")
        ax4.grid()
        ax4.set_axisbelow(True)

    # set layout to tight (so that space between figures is minimized)
    fig.tight_layout()
    print FIG_OUTPUT_DIR+FIG_OUTPUT_FILENAME
    fig.savefig(FIG_OUTPUT_DIR+FIG_OUTPUT_FILENAME, bbox_inches="tight", bbox_extra_artists=(leg,))
    print("FIGURE SAVED")