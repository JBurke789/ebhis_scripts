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
    ax1.plot(nf[0],nf[1],label='no filter')
    ax1.plot(h1[0],h1[1],label='hanning 1')
    ax1.plot(h2[0],h2[1],label='hanning 2')
    ax1.plot(h3[0],h3[1],label='hanning 3')
    ax1.plot(h4[0],h4[1],label='hanning 4')
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
    ax1.plot(array[0],array[1],label='galaxy')
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
    peak_flux = arrays[plot][1][mask]
    plt.close()

    peak_index = np.argmax(peak_flux)
    max_val = peak_flux[peak_index]
    hm = max_val/2.0
    l_index = 0
    while peak_flux[l_index] < hm:
        l_index+=1
    r_index = len(peak_vels)-1
    while peak_flux[r_index]<hm:
        r_index-=1
    fwhm=abs(peak_vels[r_index]-peak_vels[l_index])
    step_size = abs(peak_vels[peak_index]-peak_vels[peak_index-1])
    rad_vel = (peak_vels[r_index]+peak_vels[l_index])/2.0
    print('FWHM: ',fwhm,' +/- ', step_size,' km/s')
    print('RV: ',rad_vel, ' +/- ', step_size*2,' km/s')

    fig2,ax2 = plt.subplots()
    ax2.plot(peak_vels,peak_flux,label='galaxy')
    ax2.set_xlabel('Velocity [km/s]')
    ax2.set_ylabel('flux [Jy/BA]')
    ax2.legend()
    ax2.set_title(name)
    ax2.hlines(hm,peak_vels[l_index],peak_vels[r_index])
    plt.show(block=False)
    return fwhm,rad_vel,step_size

def save_csv(name,rv,uncert1,fwhm,uncert2):
    gal_results=[]
    with open('/users/jburke/ebhis_scripts/w50_stuff/new_vals.csv','r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            gal_results.append(row)


    gals_analysed=[]
    for i in gal_results:
        gals_analysed.append(i[0])
        if i[0]==name:
            i[1]=str(rv)
            i[2]=str(uncert1)
            i[3]=str(fwhm)
            i[4]=str(uncert2)
    #append gal vals if not already analysed
    if name not in gals_analysed:
        new_row = [name,str(rv),str(uncert1),str(fwhm),str(uncert2)]
        gal_results.append(new_row)

    with open('/users/jburke/ebhis_scripts/w50_stuff/new_vals.csv','w') as f:
        writer=csv.writer(f)
        header = ['name','rv','+/-','w50','+/-']
        writer.writerow(header)
        writer.writerows(gal_results)

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
            fwhm,rad_vel,step_size=get_w50(name)
            save_vals = input('Save? y/n ')
            if save_vals =='y':
                save_csv(name,fwhm,rad_vel,step_size,step_size*2)
        elif vis =='n':
            save_csv(name,'-','-','-','-')
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