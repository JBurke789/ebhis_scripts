import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np
import csv
import scipy as sp
from scipy import optimize
from scipy import integrate
from scipy import stats
import os

def import_spectrum(array):
    vel = array[0]
    inner_flux = array[1]
    bg_flux = array[2]
    return vel, inner_flux,bg_flux

def on_click(event):
    if event.inaxes is not None:
        x = event.xdata
        x_lims.append(x)
        print(x)

def baselining(vel,inner_flux,bg_flux):
    def on_click(event):
        if event.inaxes is not None:
            x = event.xdata
            x_lims.append(x)
            print(x)

    #plot spectrum to select baseline regions
    print('Select limits for baseline fitting.')
    fig1,ax1 = plt.subplots()
    ax1.plot(vel,inner_flux-bg_flux,label='galaxy')
    ax1.set_xlabel('Velocity [km/s]')
    ax1.set_ylabel('Flux per Beam Area [Jy/BA]')
    ax1.legend()
    #process values from baseline regions
    x_lims=[]
    fig1.canvas.mpl_connect('button_press_event', on_click)
    plt.show()
    pairs = list(zip(x_lims[::2], x_lims[1::2]))
    x_vals=[]
    y_vals=[]
    for i in pairs:
        low = i[0]
        high = i[1]  
        filtered_values = [(x_val, y_val) for x_val, y_val in zip(vel, inner_flux) if low <= x_val <= high]
        x_bit,y_bit = zip(*filtered_values)
        for j in x_bit:
            x_vals.append(j)
        for k in y_bit:
            y_vals.append(k)

    slope, intercept, _, _, _ = stats.linregress(x_vals, y_vals)

    y_baseline = slope*vel + intercept
    baselined_flux = (inner_flux-bg_flux)-y_baseline
    return baselined_flux

def sum_spectrum(vel,baselined_flux):
    def on_click(event):
        if event.inaxes is not None:
            x = event.xdata
            x_sum_lims.append(x)
            print(x)
    #plot spectrum to get region to integrate
    print('Select region to integrate')
    fig2,ax2 = plt.subplots()
    ax2.plot(vel,baselined_flux,label='baselined flux')
    ax2.set_xlabel('Velocity [km/s]')
    ax2.set_ylabel('Flux per Beam Area [Jy/BA]')
    ax2.set_ylim(-10,10)
    ax2.legend()
    x_sum_lims=[]
    fig2.canvas.mpl_connect('button_press_event', on_click)
    plt.show()

    sum_pairs = list(zip(x_sum_lims[::2], x_sum_lims[1::2]))
    print(sum_pairs)
    x_sum_vals=[]
    y_sum_vals=[]
    for i in sum_pairs:
        low = i[0]
        high = i[1]
        filtered_values = [(x_val, y_val) for x_val, y_val in zip(vel, baselined_flux) if low <= x_val <= high]
        x_bit, y_bit = zip(*filtered_values)
        for j in x_bit:
            x_sum_vals.append(j)
        for k in y_bit:
            y_sum_vals.append(k)

    #integrate to get total flux
    tot_flux = sp.integrate.simps(y_sum_vals,x_sum_vals)
    rms_jy = 0.09/(1.28*8.64)
    uncert = rms_jy*len(x_sum_vals)
    print('Total Flux:',tot_flux,'+- ',uncert)
    #print(x_sum_vals)
    #print(y_sum_vals)
    return tot_flux,uncert


array = np.load('spectrum.npy')
vel, inner_flux,bg_flux = import_spectrum(array)
baselined_flux = baselining(vel,inner_flux,bg_flux)
total_flux,uncert = sum_spectrum(vel,baselined_flux)

save = input('Save results: y/n ')
if save == 'y':
    name = input('galaxy name: ')    
    #looks for csv file to store spectral results
    csvpath = '/users/jburke/ebhis_scripts/workflow_results/spectral_lower_lim_results.csv'
    if not os.path.exists(csvpath):
        with open('/users/jburke/ebhis_scripts/workflow_results/final_results.csv','r') as f:
            reader = csv.reader(f)
            header = next(reader)
            with open('/users/jburke/ebhis_scripts/workflow_results/spectral_lower_lim_results.csv','w') as csv_file:
                csv_writer = csv.writer(csv_file)
                csv_writer.writerow(header)
    else:
        pass

    #get galaxy data from full list
    with open('/users/jburke/Desktop/full_gal_list.csv','r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            ra = row[1]
            dec=row[2]
            dist= row[3]
            rad_vel=row[4]
            mag = row[5]
            w50 = row[6]
            if row[0]==name:
                with open('/users/jburke/ebhis_scripts/workflow_results/spectral_lower_lim_results.csv','a') as file:
                    lines = [name,
                            ra,
                            dec,
                            dist,
                            rad_vel,
                            mag,
                            w50,
                            str(total_flux),
                            str(uncert),
                            '\n']
                    file.write(','.join(lines))





