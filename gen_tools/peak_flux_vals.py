import numpy as np
import csv
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

full_list =[]

with open('/users/jburke/Desktop/results/full_results.csv','r') as f:
    reader = csv.reader(f)
    header = next(reader)
    for row in reader:
        if row[6]=='m' and row[9]!='-':
            full_list.append(row)

def get_array(gal_name):
    path = gal_name +'/spectrum.npy'#spectrum is just unhanning filtered spectrum
    array = np.load(path)
    return array #[vel,ON,OFF]


int_fluxes =[]
peak_fluxes =[]

for gal in full_list:
    #change indexes to right vals
    rv = float(gal[9])
    w50 = float(gal[11])
    flux_int = float(gal[4])

    arrays = get_array(gal[0])
    

    vel_int = [rv-w50/2,rv+w50/2]
    print(vel_int)

    mask = (arrays[0]>=vel_int[0]) & (arrays[0]<=vel_int[1])
    peak_vels = arrays[0][mask]
    peak_flux = arrays[1][mask]-arrays[2][mask]

   
    max_flux = np.max(np.array(peak_flux))
    if max_flux>35:
        print(gal[0])
    if max_flux>0:
        int_fluxes.append(flux_int)
        peak_fluxes.append(max_flux)

data = np.array([int_fluxes,peak_fluxes])
print(data)
np.save('ebhis_scripts/gen_tools/peaks_data.npy',data)

print(min(peak_fluxes))
plt.figure()
plt.scatter(int_fluxes,peak_fluxes)
plt.show()
#carry out linear fit maybe with scikit learn
# https://realpython.com/linear-regression-in-python/
