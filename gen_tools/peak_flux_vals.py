import numpy as np
import csv

full_list =[]
#change address to proper results
with open('/users/jburke/ebhis_scripts/mom_map_analysis/results/final_results.csv','r') as f:
    reader = csv.reader(f)
    header = next(reader)
    for row in reader:
        #change to proper index
        if row[4]=='m':
            full_list.append(row)

def get_array(gal_name):
    #define function that returns spectra arrays for given galaxy name
    #does numpy file contyain all hannings or is it per each one
    pass

int_fluxes =[]
peak_fluxes =[]

for gal in full_list:
    #change indexes to right vals
    rv = float(gal[4])
    w50 = float(gal[6])
    flux_int = float(gal[10])

    arrays = get_array(gal[0])

    vel_int = [rv-w50/2,rv-w50/2]

    mask = (arrays[0]>=vel_int[0]) & (arrays[0]<=vel_int[1])
    peak_vels = arrays[0][mask]
    peak_flux = arrays[1][mask]-arrays[2][mask]

    max_flux = np.nanmax(peak_flux)

    int_fluxes.append(flux_int)
    peak_fluxes.append(max_flux)

#carry out linear fit maybe with scikit learn
# https://realpython.com/linear-regression-in-python/