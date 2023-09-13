import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np
import csv

galaxy = 'NGC1156'

def load_npy(name):
    array = np.load(name + '/spectrum.npy')
    return array

def plot_spectrum(name, array,radvel,w50):
    fig1,ax1 = plt.subplots()
    ax1.plot(array[0],array[1]-array[2])
    ax1.axvline(radvel, color='red', linestyle='--',label='Rad vel')
    if w50!= 0:
        ax1.axvline(radvel+w50,color='red',linestyle='--',label='w50',alpha=0.4)
        ax1.axvline(radvel-w50,color='red',linestyle='--',alpha=0.4)
    ax1.set_xlabel('Velocity [km/s]')
    ax1.set_ylabel('Flux per Beam Area [Jy/BA]')
    ax1.set_title(name)
    ax1.legend()
    fig1.savefig(name+'/spectrum.png',dpi=600)
    plt.show()

with open('/users/jburke/ebhis_scripts/workflow_results/MW_overlap.csv','r') as f:
   reader = csv.reader(f)
   header = next(reader)
   for row in reader:
        name = row[0]
        ra = row[1]
        dec = row[2]
        dist = float(row[3])
        radvel = float(row[4])
        #mag21 = float(row[5])
        w50 = row[6]
        if w50 =='':
            w50 = 0
        else:
            w50 = float(w50)

        array=load_npy(name)
        plot_spectrum(name,array,radvel,w50)
        print('Spectrum for '+ name + ' generated.') 








'''
array = np.load(galaxy + '/spectrum.npy')
velo = array[0]
temp = array[1]
temp2 = array[2]

galaxy_flux = temp-temp2
fig1,ax1 = plt.subplots()
ax1.plot(velo,temp)
ax1.plot(velo,temp2)
ax1.plot(velo,galaxy_flux)
ax1.set_xlabel('Velocity [km/s]')
ax1.set_ylabel('Temp [k]')
plt.show()
'''