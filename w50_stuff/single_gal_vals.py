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

def plot_spectrum(name,nf,h1,h2,h3,h4,rv):
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
   #ax1.set_ylim(-10,40)
   #ax1.set_xlim(float(rv)-200,float(rv)+200)
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
    ax1.set_title(name)
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


    fig1,ax1 = plt.subplots()
    ax1.plot(peak_vels,peak_flux,label='galaxy')
    ax1.set_xlabel('Velocity [km/s]')
    ax1.set_ylabel('flux [Jy/BA]')
    ax1.legend()
    ax1.set_title(name)
    ax1.hlines(hm,peak_vels[l_index],peak_vels[r_index])
    plt.show(block=False)
    return fwhm,rad_vel,step_size



gal_results=[]
with open('/users/jburke/ebhis_scripts/w50_stuff/rv_w50_vals.csv','r') as f:
    reader = csv.reader(f)
    header = next(reader)
    for row in reader:
        gal_results.append(row)


name = input('Galaxy name: ')




with open('/users/jburke/ebhis_scripts/w50_stuff/ready_to_analyse.csv','r') as f:
    reader = csv.reader(f)
    header = next(reader)
    for row in reader:
        if row[0] == name:
            rad_vel_init = row[4]
            nf,h1,h2,h3,h4 = get_spectra(name)
            plot_spectrum(name,nf,h1,h2,h3,h4,rad_vel_init)
            plot = int(input('which level to run analysis? (0 for no hanning) '))
            plt.close()
            arrays = [nf,h1,h2,h3,h4]
            single_spectrum_plot(name,arrays[plot],rad_vel_init)
            fwhm,rad_vel,step_size=get_w50(name)

save = input('Save results? y/n: ')
if save == 'y':
    with open('/users/jburke/ebhis_scripts/workflow_results/final_results.csv','r') as f:#get initial row vals from full list
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            if row[0]==name:
                init_row = row
    #run through gals already analysed and replace values
    gals_analysed=[]
    for i in gal_results:#replaces values if galaxy already analysed
        gals_analysed.append(i[0])
        if i[0]==name:
            i[9]=str(rad_vel)
            i[10]=str(step_size)
            i[11]=str(fwhm)
            i[12]=str(step_size*2)
    #append gal vals if not already analysed
    if name not in gals_analysed:
        adds = ['-','-','-']
        new_row = init_row +adds
        new_row[9] =str(rad_vel)
        new_row[10]=str(step_size)
        new_row[11]=str(fwhm)
        new_row[12]=str(step_size*2)
        new_add = [str(rad_vel),str(step_size),str(fwhm),str(step_size*2)]
        new_row = init_row+new_add
        gal_results.append(new_row)
    
    with open('/users/jburke/ebhis_scripts/w50_stuff/rv_w50_vals.csv','w') as f:
        csv_writer = csv.writer(f)
        header=['name','ra','dec','distance','radial_velocity','h1_21_cm_mag','h1_21_cm_50pc_width','flux [Jy km/s BA^-1]','uncert','RV [km/s]','uncert','w50 [km/s]','uncert']
        csv_writer.writerow(header)
        csv_writer.writerows(gal_results)

