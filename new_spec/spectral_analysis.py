import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np
import csv
from scipy import integrate
import os

'''
Runs through csv of gals with MW overlap not in close groups.
plots all hanning levels. 
replots selected hanning level
integrates over selected vel range
saves results to csv
'''

def load_array(name,spec):
    array = np.load(name+spec)
    return array

def get_spectra(name):#[0]=vel, [1]=ON, [2]=OFF
    h0 = load_array(name,'/man_spec_h0.npy')
    h1 = load_array(name,'/man_spec_h1.npy')
    h2 = load_array(name,'/man_spec_h2.npy')
    h3 = load_array(name,'/man_spec_h3.npy')
    h4 = load_array(name,'/man_spec_h4.npy')
    spectra = [h0,h1,h2,h3,h4]
    return spectra

def plot_spectra(name,h0,h1,h2,h3,h4,rv,w50): #plots all hanning level spectra for selection. returns hanning level intiger
    fig1,ax1 = plt.subplots()
    ax1.plot(h0[0],h0[1]-h0[2],label='no filter')
    ax1.plot(h4[0],h4[2],label='bg')
    ax1.plot(h1[0],h1[1]-h1[2],label='hanning 1')
    ax1.plot(h2[0],h2[1]-h2[2],label='hanning 2')
    ax1.plot(h3[0],h3[1]-h3[2],label='hanning 3')
    ax1.plot(h4[0],h4[1]-h4[2],label='hanning 4')
    ax1.set_title(name)
    ax1.vlines(rv,-20,20,'r')
    ax1.vlines(rv-w50/2.,-20,20,'r')
    ax1.vlines(rv+w50/2.,-20,20,'r')
    ax1.hlines(0,np.min(h0[0]),np.max(h0[0]),linestyle='--',linewidth=0.6,alpha=0.6)
    ax1.set_xlabel('Velocity [km/s]')
    ax1.set_ylabel('flux [Jy/BA]')
    ax1.legend()
    plt.show(block=False)
    h = int(input('hanning level : '))
    plt.close()
    return h

def plot_single(name,spectra,h,rv,w50):#plots spectrumn of selected hanning level for velocity selection. returns vel limits as floats
    fig1,ax1 = plt.subplots()
    #y_hanning = cleaned_gal*np.hanning(len(vel))
    ax1.plot(spectra[h][0],spectra[h][1]-spectra[h][2])
    ax1.set_title(name)
    ax1.vlines(rv,-20,20,'r')
    ax1.vlines(rv-w50/2.,-20,20,'r')
    ax1.vlines(rv+w50/2.,-20,20,'r')
    ax1.hlines(0,np.min(spectra[h][0]),np.max(spectra[h][0]),linestyle='--',linewidth=0.6,alpha=0.6)
    ax1.set_xlabel('Velocity [km/s]')
    ax1.set_ylabel('flux [Jy/BA]')
    ax1.legend()
    plt.show(block=False)
    l_vel = float(input('Low vel: '))
    h_vel = float(input('high vel: '))
    return l_vel,h_vel

def spec_int(spectra,h,low_vel,high_vel):#intigrates spectrum over selected velocity range. returns flux and uncert
    mask = (spectra[h][0]>=low_vel) & (spectra[h][0]<=high_vel)
    gal_vels = spectra[h][0][mask]
    gal_flux = spectra[h][1][mask]-spectra[h][2][mask]
    tot_flux = integrate.simps(gal_flux,gal_vels)
    rms_jy = (0.09+h*0.09)/(1.28*8.64)#accounts for hanning filtering
    uncert = rms_jy*len(gal_vels)
    print('Total Flux:',tot_flux,'+- ',uncert)
    return tot_flux, uncert

def save_results(name,flux,uncert,l_vel,h_vel,h):# appands or updates results in array
    new_line = [name,flux,uncert,l_vel,h_vel,h]
    if name in gal_names:
        for i,row in enumerate(gal_results):
            if row[0]==name:
                gal_results[i]=new_line
    else:
        gal_results.append(new_line)

    #return gal_results
        
#load galaxies already analysed
gal_names=[]
gal_results=[]
with open('/users/jburke/ebhis_scripts/new_spec/results.csv','r') as f:
    reader = csv.reader(f)
    header1 = next(reader)
    for row in reader:
        gal_names.append(row[0])
        gal_results.append(row)

#runs analysis on all galaxies
with open('/users/jburke/ebhis_scripts/catagorisation/cat_results/MW_overlap.csv','r') as f:
    reader = csv.reader(f)
    header = next(reader)
    for row in reader:
        print('-------',row[0],'-------')
        plt.close()
        name= row[0]
        rv = float(row[4])
        if row[5]=='':
            w50 = 0
        else:
            w50 = float(row[5])
        if os.path.isfile(name+'/man_spec_h0.npy'):
            spectra= get_spectra(name)
            h=plot_spectra(name,spectra[0],spectra[1],spectra[2],spectra[3],spectra[4],rv,w50)
            l_vel,h_vel = plot_single(name,spectra,h,rv,w50)
            flux,uncert = spec_int(spectra,h,l_vel,h_vel)
            save = input('Save results? (y/n): ')
            if save =='y':
                save_results(name,flux,uncert,l_vel,h_vel,h)
            else:
                pass
        else:
            print(name+' - no file.')

#saves results to csv
with open('/users/jburke/ebhis_scripts/new_spec/results.csv','w') as f:
    writer = csv.writer(f)
    writer.writerow(header1)
    writer.writerows(gal_results)

