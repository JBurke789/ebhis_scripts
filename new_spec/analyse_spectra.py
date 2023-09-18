import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np
import csv
import os

def import_spectrum(name):
    file = name+'/spectrum.npy'
    array=np.load(file)
    vel = array[0]
    inner_flux = array[1]
    bg_flux = array[2]
    return vel, inner_flux,bg_flux






with open('/users/jburke/ebhis_scripts/workflow_results/MW_overlap.csv','r') as f:
    reader = csv.reader(f)
    header = next(reader)
    for row in reader:
        name = row[0]
        ra = row[1]
        dec = row[2]
        rv = float(row[4])
        w50 = row[6]
        if w50 == '':
            w50 = 0
        else:
            w50=float(w50)
        vel,flux_ON,flux_OFF = import_spectrum(name)
        
        fig1,ax1 = plt.subplots()
        ax1.plot(vel,flux_ON-flux_OFF,label='cleaned flux')
        ax1.set_xlabel('Velocity [km/s]')
        ax1.set_ylabel('Flux per Beam Area [Jy/BA]')
        ax1.vlines(rv,-10,+10)
        ax1.vlines(rv-w50/2,-10,+10)
        ax1.vlines(rv+w50/2,-10,+10)
        ax1.set_ylim(-20,20)
        ax1.set_title(name)
        ax1.legend()
        plt.show()
        