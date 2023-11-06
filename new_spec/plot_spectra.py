import numpy as np
import csv
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

gal_names = []
with open('/users/jburke/ebhis_scripts/new_spec/detailed_results.csv','r')as f:
    reader = csv.reader(f)
    heder = next(reader)
    for row in reader:
        gal_names.append(row[0])

print(gal_names)

def plot_spec(name):
    array = np.load(name+'/spectrum.npy')
    fig1,ax1 = plt.subplots()
    ax1.plot(array[0],array[1],'k',linewidth=0.7,drawstyle='steps-mid')
    #ax1.hlines(0,np.min(array[0]),np.max(array[0]),linestyle='--',linewidth=0.6,alpha=0.6)
    ax1.set_title(name)
    ax1.set_xlabel('Velocity [km/s]')
    ax1.set_ylabel('Flux per Beam Area [Jy/BA]')
        #ax1.set_xlim(rv-w50*2.5,rv+w50*2.5)
        #ax1.set_ylim(np.min(array[1])*1.2,peak_bit)
    #ax1.vlines(rv,np.min(array[1]),np.max(array[1]),'r',linewidth=0.7,alpha=0.5,label='v_r')
    #closest_index1 = np.argmin(np.abs(array[0] - rv-0.5*w50))
    #closest_index2 = np.argmin(np.abs(array[0] - rv+0.5*w50))
    #ax1.plot(array[0][closest_index1],array[1][closest_index1],'.',color='r',label='w50',linewidth=0.001,alpha=0.5)
    #ax1.plot(array[0][closest_index2],array[1][closest_index2],'.',color='r',label='w50',linewidth=0.001,alpha=0.5)
    plt.show(block=False)

    MW_start = float(input('MW start: '))
    MW_end = float(input('MW end: '))
    plt.close()
    #with MW
    mask = (array[0]>=MW_start) & (array[0]<=MW_end)
    MW_vels = array[0][mask]
    MW_flux = array[1][mask]
    #without MW
    mask1 = (array[0]<=MW_start) 
    vels1 = array[0][mask1]
    #vels1 = np.insert(vels1,-1,MW_vels[0])
    flux1 = array[1][mask1]
    #flux1 = np.insert(flux1,-1,MW_flux[0])
    mask2 = (array[0]>=MW_end) 
    vels2 = array[0][mask2]
    vels2 = np.insert(vels2,0,MW_vels[-1])
    flux2 = array[1][mask2]
    flux2 = np.insert(flux2,0,MW_flux[-1])

    MW_vels = np.insert(MW_vels,0,vels1[-1])
    MW_flux = np.insert(MW_flux,0,flux1[-1])


    fig2,ax2 = plt.subplots()
    ax2.plot(MW_vels,MW_flux,'r',alpha=0.7,linewidth=0.7,drawstyle='steps-mid')
    ax2.plot(vels1,flux1,'k',linewidth=0.7,drawstyle='steps-mid')
    ax2.plot(vels2,flux2,'k',linewidth=0.7,drawstyle='steps-mid')
    #ax1.hlines(0,np.min(array[0]),np.max(array[0]),linestyle='--',linewidth=0.6,alpha=0.6)
    ax2.set_title(name)
    ax2.set_xlabel('Velocity [km/s]')
    ax2.set_ylabel('Flux per Beam Area [Jy/BA]')
    ax2.hlines(0,np.min(array[0]),np.max(array[0]),linestyle='--',linewidth=0.6,alpha=0.6)

for name in gal_names:
    plot_spec(name)

