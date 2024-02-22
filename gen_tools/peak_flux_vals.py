import numpy as np
import csv
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

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


mean_fluxes =[]
peak_fluxes =[]

for gal in full_list:
    #change indexes to right vals
    rv = float(gal[9])
    w50 = float(gal[11])
    flux_int = float(gal[4])

    mean_flux = flux_int/w50
    
    
    arrays = get_array(gal[0])
    vel_int = [rv-w50/2,rv+w50/2]

    mask = (arrays[0]>=vel_int[0]) & (arrays[0]<=vel_int[1])
    peak_vels = arrays[0][mask]
    peak_flux = arrays[1][mask]-arrays[2][mask]

   
    max_flux = np.max(np.array(peak_flux))
    if max_flux>0 and max_flux<35:
        mean_fluxes.append(mean_flux)
        peak_fluxes.append(max_flux)

data = np.array([mean_fluxes,peak_fluxes])

#np.save('ebhis_scripts/gen_tools/peaks_data.npy',data)
x_reshaped = data[0].reshape(-1,1)
model = LinearRegression()
model.fit(x_reshaped, data[1])
y_pred = model.predict(x_reshaped)

x_fit = np.linspace(0,20,10)
y_fit = model.coef_[0]*x_fit + model.intercept_

plt.figure()
plt.plot(x_fit, y_fit, linestyle='dashed',alpha=0.7,color='red', label='Linear fit')

plt.scatter(mean_fluxes,peak_fluxes,s=5,color='k')
plt.xlabel('Mean Flux [Jy]')
plt.ylabel('Peak Flux [Jy]')
plt.show()

print('slope:', model.coef_[0])
print('intercept:',model.intercept_)
#slope: 0.918991967786306
#intercept: 2.369921536005469

#median peak flux density
#median mean flux density = 0.72 Jy

val = 0.72/model.coef_[0]
print(val)#3.0315957528116093
