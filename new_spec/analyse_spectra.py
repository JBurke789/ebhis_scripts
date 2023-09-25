import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np
import csv
import os
import scipy as sp
from scipy import integrate
from lmfit.models import PolynomialModel

def import_spectrum(name):
    file = name+'/spectrum.npy'
    array=np.load(file)
    vel = array[0]
    inner_flux = array[1]
    bg_flux = array[2]
    return vel, inner_flux,bg_flux


def coarseBackgroundModel(x,y):
    """
    fits polynomial to data
    """
    #fig1,ax1= plt.subplots()
    #ax1.plot(x,y,label='gal')
    #ax1.legend()
    #plt.show(block=False)
    low_vel = float(input('baseline low velocity: '))
    high_vel =float(input('baseline high velocity: '))
    # set up polynomial model
    poly_mod = PolynomialModel(1, prefix='p1_')
    mask = (vel < low_vel) | (vel > high_vel)  # Create a boolean mask
    filtered_vel = vel[mask]
    filtered_flux = flux_cleaned[mask]
    # let lmfit guess the parameter values:
    p_bg = poly_mod.guess(filtered_flux, x=filtered_vel)
    # set up our background model (only polynomial here):
    mod_bg = poly_mod
    # initialize the model with the guessed parameters:
    init_bg = mod_bg.eval(p_bg, x=filtered_vel)
    # fit the model:
    out_bg = mod_bg.fit(filtered_flux, p_bg, x=filtered_vel)
    return p_bg, out_bg, mod_bg

def baseline(vel,flux_cleaned):
    p_bg, out_bg, mod_bg = coarseBackgroundModel(vel,flux_cleaned)
    baseline= mod_bg.eval(p_bg,x=vel)
    baselined_flux = flux_cleaned-baseline
    return baselined_flux

def integrate_spectrum(vel,flux_cleaned):
    #extract values to integrate
    low_lim = input('integrate low velocity:')
    high_lim = input('integrate high velocity:')
    x_vals=[]
    y_vals=[]
    low = float(low_lim)
    high = float(high_lim)  
    filtered_values = [(x_val, y_val) for x_val, y_val in zip(vel, flux_cleaned) if low <= x_val <= high]
    x_bit,y_bit = zip(*filtered_values)
    for j in x_bit:
        x_vals.append(j)
    for k in y_bit:
        y_vals.append(k)

    #integrate over range
    tot_flux = integrate.simps(y_vals,x_vals)
    rms_jy = 0.09/(1.28*8.64)
    uncert = rms_jy*len(x_vals)
    print('Total Flux:',tot_flux,'+- ',uncert)

    return tot_flux, uncert


#looks for csv file to store spectral results
csvpath = '/users/jburke/ebhis_scripts/new_spec/detailed_results.csv'
if not os.path.exists(csvpath):
    with open('/users/jburke/ebhis_scripts/workflow_results/final_results.csv','r') as f:
        reader = csv.reader(f)
        header = next(reader)
        extra = ['note']
        header = header + extra
        with open(csvpath,'w') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(header)
else:
    pass




with open('/users/jburke/ebhis_scripts/workflow_results/MW_overlap.csv','r') as f:
    reader = csv.reader(f)
    header = next(reader)
    for row in reader:
        name = row[0]
        print('-------',name,'--------')
        ra = row[1]
        dec = row[2]
        rv = float(row[4])
        w50 = row[6]
        if w50 == '':
            w50 = 0
        else:
            w50=float(w50)
        vel,flux_ON,flux_OFF = import_spectrum(name)
        flux_cleaned = flux_ON-flux_OFF
        fig1,ax1 = plt.subplots()
        ax1.plot(vel,flux_cleaned,label='cleaned flux')
        ax1.set_xlabel('Velocity [km/s]')
        ax1.set_ylabel('Flux per Beam Area [Jy/BA]')
        ax1.vlines(rv,-10,+10,'r')
        ax1.vlines(rv-w50/2,-10,+10,'r')
        ax1.vlines(rv+w50/2,-10,+10,'r')
        #ax1.set_ylim(-20,20)
        ax1.set_title(name)
        ax1.legend()
        plt.show(block=False)

        #get details for analysis
        note = input('Note: (1=MW overlap,2=could not see,3=clear) ')
        if note=='1':
            new_row=row + ['n/a','n/a','1']
            with open(csvpath,'a') as f:
                csv_writer = csv.writer(f)
                csv_writer.writerow(new_row)

        elif note== '2':
            baselined_flux = baseline(vel,flux_cleaned)
            tot_flux, uncert = integrate_spectrum(vel,baselined_flux)
            new_row = row +[str(tot_flux),str(uncert),note]
            with open(csvpath,'a') as f:
                csv_writer = csv.writer(f)
                csv_writer.writerow(new_row)
        elif note=='3':
            baselined_flux = baseline(vel,flux_cleaned)
            tot_flux, uncert = integrate_spectrum(vel,baselined_flux)
            with open(csvpath,'a') as f:
                csv_writer = csv.writer(f)
                csv_writer.writerow(new_row)



