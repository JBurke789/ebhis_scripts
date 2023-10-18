import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np
import csv

def load_array(name,w50_uncert):
    if w50_uncert<2:
        path_man = name + '/man_spectrum.npy'
        path = name +'/spectrum.npy'
    elif w50_uncert>2 and w50_uncert<3:
        path_man = name + '/man_hanning_spectrum1.npy'
        path = name +'/hanning_spectrum1.npy'
    elif w50_uncert>5 and w50_uncert<6:
        path_man = name + '/man_hanning_spectrum2.npy'
        path = name +'/hanning_spectrum2.npy'
    elif w50_uncert>10 and w50_uncert<11:
        path_man = name + '/man_hanning_spectrum3.npy'
        path = name +'/hanning_spectrum3.npy'
    elif w50_uncert>20 and w50_uncert<21:
        path_man = name + '/man_hanning_spectrum4.npy'
        path = name +'/hanning_spectrum4.npy'
    
    try:
        array = np.load(path_man)
    except FileNotFoundError:
        array = np.load(path)

    return array
    


def make_plot(name,rv,w50,array):
    low_x = rv-w50
    high_x = rv+w50
    mask = (array[0]>=low_x) & (array[0]<=high_x)
    peak_vels = array[0][mask]
    peak_flux = array[1][mask]

    peak_bit = 1.05 * np.max(peak_flux)
    fig1,ax1 = plt.subplots()
    ax1.plot(array[0],array[1],'k',linewidth=0.7)
    ax1.set_title(name)
    ax1.set_xlabel('Velocity [km/s]')
    ax1.set_ylabel('Flux per Beam Area [Jy/BA]')
    #ax1.set_xlim(rv-w50*2.5,rv+w50*2.5)
    #ax1.set_ylim(np.min(array[1])*1.2,peak_bit)
    ax1.vlines(rv,np.min(array[1]),np.max(array[1]),'r',linewidth=0.7,alpha=0.5,label='v_r')
    closest_index1 = np.argmin(np.abs(array[0] - rv-0.5*w50))
    closest_index2 = np.argmin(np.abs(array[0] - rv+0.5*w50))
    ax1.plot(array[0][closest_index1],array[1][closest_index1],'.',color='r',label='w50',linewidth=0.001,alpha=0.5)
    ax1.plot(array[0][closest_index2],array[1][closest_index2],'.',color='r',label='w50',linewidth=0.001,alpha=0.5)
    plt.show()




gal_vals =[]
with open('/users/jburke/ebhis_scripts/w50_stuff/fixed_vals.csv', 'r') as f:
    reader = csv.reader(f)
    header = next(reader)
    for row in reader:
        gal_vals.append(row)




for i in gal_vals:
    name=i[0]
    rv = i[1]
    if i[1] =='-':
        print(name, ' no plot made')
    else:
        rv=float(i[1])
        rv_u = float(i[2])
        w50 = float(i[3])
        w50_u = float(i[4])
        array = load_array(name,w50_u)
        make_plot(name,rv,w50,array)