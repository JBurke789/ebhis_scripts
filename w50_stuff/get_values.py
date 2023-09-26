import csv
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt


def load_array(name):
    array = np.load(name+'/spectrum.npy')
    return array[0],array[1],array[2]

def plot_spectrum(name,vel,cleaned_gal,bg,rv):
    fig1,ax1 = plt.subplots()
    y_hanning = cleaned_gal*np.hanning(len(vel))
    ax1.plot(vel,cleaned_gal,label='gal')
    #ax1.plot(vel,bg,label='bg')
    ax1.plot(vel,y_hanning,label='hanning')
    ax1.set_title(name)
    ax1.vlines(float(rv),-20,20,'r')
    ax1.set_xlabel('Velocity [km/s]')
    ax1.set_ylabel('flux [Jy/BA]')
    ax1.set_ylim(-10,40)
    ax1.set_xlim(float(rv)-200,float(rv)+200)
    ax1.legend()
    plt.show()

with open('/users/jburke/ebhis_scripts/w50_stuff/ready_to_analyse.csv','r') as f:
    reader = csv.reader(f)
    header = next(reader)
    for row in reader:
        name = row[0]
        rad_vel_init = row[4]

        vel,gal_flux,bg_flux = load_array(name)
        plot_spectrum(name,vel,gal_flux-bg_flux,bg_flux,rad_vel_init)

