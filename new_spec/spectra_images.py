import numpy as np
import csv
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

'''
Plots spectra to be saved as png
'''

def load_array(name):
    array = np.load(name+'/man_spec_h0.npy')
    return array

def plot_spectrum(name,array,l_vel,h_vel):
    mask = (array[0]>=l_vel) & (array[0]<=h_vel)
    gal_vels = array[0][mask]
    gal_flux = array[1][mask]-array[2][mask]    

    fig1,ax1 = plt.subplots()
    ax1.plot(array[0],array[1]-array[2],'k', linewidth=0.7,alpha=0.5, drawstyle='steps-mid')
    ax1.plot(gal_vels,gal_flux,'k',linewidth=0.7,drawstyle='steps-mid')
    ax1.hlines(0,np.min(array[0]),np.max(array[0]),linestyle='--',linewidth=0.6,alpha=0.6)
    ax1.vlines(l_vel,-100,200,alpha=0.5,linestyle = 'dashed' , color = 'black' )
    ax1.vlines(h_vel,-100,200,alpha=0.5,linestyle = 'dashed' , color = 'black' )    
    ax1.set_title(name)
    ax1.set_xlabel('Velocity [km/s]')
    ax1.set_ylabel('Flux per Beam Area [Jy/BA]')
    plt.show()


with open('/users/jburke/ebhis_scripts/new_spec/results.csv','r') as f:
    reader = csv.reader(f)
    header = next(reader)
    for row in reader:
        if row[0] == 'IC0342':
            name = row[0]
            l_vel = float(row[3])
            h_vel = float(row[4])
            array = load_array(name)
            plot_spectrum(name,array,l_vel,h_vel)
