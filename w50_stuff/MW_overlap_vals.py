import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np
import csv
from scipy import integrate
import os

"""
Gets RV and w50 vals for spectra with MW overlap
"""

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

def get_vals(spectra,h,low_vel,high_vel):
    mask = (spectra[h][0]>=low_vel) & (spectra[h][0]<=high_vel)
    gal_vels = spectra[h][0][mask]
    gal_flux = spectra[h][1][mask]-spectra[h][2][mask]
    peak_index = np.argmax(gal_flux)
    max_val = gal_flux[peak_index]
    hm = max_val/2.0
    l_index = 0
    while gal_flux[l_index] < hm:
        l_index+=1
    r_index = len(gal_vels)-1
    while gal_flux[r_index]<hm:
        r_index-=1
    fwhm=abs(gal_vels[r_index]-gal_vels[l_index])
    step_size = abs(gal_vels[peak_index]-gal_vels[peak_index-1])
    rad_vel = (gal_vels[r_index]+gal_vels[l_index])/2.0
    print('FWHM: ',fwhm,' +/- ', step_size,' km/s')
    print('RV: ',rad_vel, ' +/- ', step_size*2,' km/s')

    fig2,ax2 = plt.subplots()
    ax2.plot(gal_vels,gal_flux,label='galaxy')
    ax2.set_xlabel('Velocity [km/s]')
    ax2.set_ylabel('flux [Jy/BA]')
    ax2.legend()
    ax2.set_title(name)
    ax2.hlines(hm,gal_vels[l_index],gal_vels[r_index])
    plt.show()
    return fwhm,rad_vel,step_size

def save_results(name,rv,stepsize,fwhm,stepsize2,h):# appends or updates results in array
    new_line = [name,rv,stepsize,fwhm,stepsize2,h]
    if name in gal_names:
        for i,row in enumerate(gal_results):
            if row[0]==name:
                gal_results[i]=new_line
    else:
        gal_results.append(new_line)

#load galaxies already analysed
gal_names=[]
gal_results=[]
with open('/users/jburke/ebhis_scripts/w50_stuff/MW_overlap_results.csv','r') as f:
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
            fwhm,rad_vel,step_size = get_vals(spectra,h,l_vel,h_vel)
            save = input('Save results? (y/n): ')
            if save =='y':
                save_results(name,rad_vel,step_size,fwhm,step_size*2,h)
            else:
                save_results(name,'-','-','-','-','-')

        else:
            print(name+' - no file.')

            #saves results to csv
with open('/users/jburke/ebhis_scripts/w50_stuff/MW_overlap_results.csv','w') as f:
    writer = csv.writer(f)
    writer.writerow(header1)
    writer.writerows(gal_results)