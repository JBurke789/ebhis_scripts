import csv
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt


def load_array(name,spec):
    array = np.load(name+spec)
    return array

def get_spectra(name):
    nf= load_array(name,'/spectrum.npy')
    
    h1 = load_array(name,'/hanning_spectrum1.npy')
    h2 = load_array(name,'/hanning_spectrum2.npy')
    h3 = load_array(name,'/hanning_spectrum3.npy')
    h4 = load_array(name,'/hanning_spectrum4.npy')
    return nf,h1,h2,h3,h4

def plot_all_spectra(name,nf,h1,h2,h3,h4,rv):
    fig1,ax1 = plt.subplots()
    #y_hanning = cleaned_gal*np.hanning(len(vel))
    ax1.plot(nf[0],nf[1]-nf[2],label='no filter')
    ax1.plot(h4[0],h4[2],label='bg')
    ax1.plot(h1[0],h1[1]-h1[2],label='hanning 1')
    ax1.plot(h2[0],h2[1]-h2[2],label='hanning 2')
    ax1.plot(h3[0],h3[1]-h3[2],label='hanning 3')
    ax1.plot(h4[0],h4[1]-h4[2],label='hanning 4')
    ax1.set_title(name)
    ax1.vlines(float(rv),-20,20,'r')
    ax1.set_xlabel('Velocity [km/s]')
    ax1.set_ylabel('flux [Jy/BA]')
    ax1.set_ylim(-10,40)
    ax1.set_xlim(float(rv)-200,float(rv)+200)
    ax1.legend()
    plt.show(block=False)

def single_spectrum_plot(name,array,rv):
    fig1,ax1 = plt.subplots()
    ax1.plot(array[0],array[1]-array[2],label='galaxy')
    ax1.plot(array[0],array[2],label='background')
    ax1.vlines(float(rv),-20,20,'r')
    ax1.set_xlabel('Velocity [km/s]')
    ax1.set_ylabel('flux [Jy/BA]')
    ax1.set_ylim(-10,40)
    ax1.set_xlim(float(rv)-200,float(rv)+200)
    ax1.legend()
    ax1.set_title(name)
    plt.show(block=False)

def get_w50(name):
    low_x = float(input('low vel val: '))
    high_x = float(input('high vel val: '))
    mask = (arrays[plot][0]>=low_x) & (arrays[plot][0]<=high_x)
    peak_vels = arrays[plot][0][mask]
    peak_flux = arrays[plot][1][mask]-arrays[plot][2][mask]
    plt.close()
    fig1,ax1 = plt.subplots()
    ax1.plot(peak_vels,peak_flux,label='galaxy')
    ax1.set_xlabel('Velocity [km/s]')
    ax1.set_ylabel('flux [Jy/BA]')
    ax1.legend()
    ax1.set_title(name+'SECOND?')
    plt.show(block=False)

    peak_index = np.argmax(peak_flux)
    max_val = peak_flux[peak_index]
    hm = max_val/2.0
    l_index = peak_index
    while peak_flux[l_index]>hm:
        l_index-=1
    r_index = peak_index
    while peak_flux[r_index]>hm:
        r_index+=1
    fwhm=abs(peak_vels[r_index]-peak_vels[l_index])
    step_size = abs(peak_vels[peak_index]-peak_vels[peak_index-1])
    rad_vel = (peak_vels[r_index]+peak_vels[l_index])/2.0
    print('FWHM: ',fwhm,' +/- ', step_size,' km/s')
    print('RV: ',rad_vel, ' +/- ', step_size*2,' km/s')
    plt.close()


    fig2,ax2 = plt.subplots()
    ax2.plot(peak_vels,peak_flux,label='galaxy')
    ax2.set_xlabel('Velocity [km/s]')
    ax2.set_ylabel('flux [Jy/BA]')
    ax2.legend()
    ax2.set_title(name)
    ax2.hlines(hm,peak_vels[l_index],peak_vels[r_index])
    plt.show(fig2,block=False)


with open('/users/jburke/ebhis_scripts/w50_stuff/ready_to_analyse.csv','r') as f:
    reader = csv.reader(f)
    header = next(reader)
    for row in reader:
        name = row[0]
        rad_vel_init = row[4]
        print('-----',name,'-----')

        nf,h1,h2,h3,h4 = get_spectra(name)
        plot_all_spectra(name,nf,h1,h2,h3,h4,rad_vel_init)  
        plot = int(input('which level to run analysis? (0 for no hanning) '))
        plt.close()
        arrays = [nf,h1,h2,h3,h4]
        single_spectrum_plot(name,arrays[plot],rad_vel_init)
        vis = input('Get vals? y/n ')
        if vis == 'y':
            get_w50(name)
            save_vals = input('Save? ')
        plt.close()

        




        '''condition = input('Run hanning? y/n')
        if condition == 'n':
            print('extract values')
        elif condition == 'y':
            repeat = 'y'
            while repeat=='y':
                plotting_flux = plotting_flux*np.hanning(len(vel))
                plot_spectrum(name,vel,cleaned_flux,plotting_flux,rad_vel_init)
                repeat = input('Repeat? y/n')
            extract = input('extract values? y/n')
            if extract == 'y':
                print('extract values')
            else:
                print('cannot extract values')
        
'''