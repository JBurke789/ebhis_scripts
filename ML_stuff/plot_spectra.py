import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

def unit_conversion(temp):
  flux_jy = temp/1.28
  flux_BA = flux_jy/8.64
  return flux_BA

def import_data(file_name):
    data= np.genfromtxt(file_name,delimiter=' ')
    vel=[]
    flux=[]
    for datum in data:
        vel.append(datum[0]/1000.)
        flux.append(unit_conversion(datum[1]))
    return vel,flux

def plot_spec(vel,flux):
    fig1,ax1 = plt.subplots()
    ax1.plot(vel,flux,'k',linewidth=0.7,drawstyle='steps-mid')
    #ax1.hlines(0,np.min(array[0]),np.max(array[0]),linestyle='--',linewidth=0.6,alpha=0.6)
    #ax1.set_title('full spectrum')
    ax1.set_xlabel('Velocity [km/s]')
    ax1.set_ylabel('Flux per Beam Area [Jy/BA]')
    ax1.hlines(0,xmin=min(vel),xmax=max(vel),linestyles='dashed',alpha=0.6)
    chunks = [0,2500,5000,7500,10000,12500,15000]
    for vel in chunks:
        ax1.vlines(vel,-0.025,0.13,'r',alpha=0.5)
    plt.show()

def plot_spec_double(vel1,flux1,vel2,flux2):
    fig1,ax1 = plt.subplots()
    ax1.plot(vel1,flux1,linewidth=0.7,drawstyle='steps-mid',label='MW')
    ax1.plot(vel2,flux2,linewidth=0.7,drawstyle='steps-mid',label='EG')
    #ax1.hlines(0,np.min(array[0]),np.max(array[0]),linestyle='--',linewidth=0.6,alpha=0.6)
    ax1.set_title('MW and EG')
    ax1.set_xlabel('Velocity [km/s]')
    ax1.set_ylabel('Flux per Beam Area [Jy/BA]')
    ax1.hlines(0,xmin=min(vel2),xmax=max(vel2),linestyles='dashed',alpha=0.6,colors='gray')
    plt.legend()
    plt.show()


#velsMW,fluxMW = import_data('..\..\..\Desktop\ML_stuff\MW_spectrum.DAT')
#velsEG,fluxEG = import_data('..\..\..\Desktop\ML_stuff\EG_spectrum.DAT')
#plot_spec_double(velsMW,fluxMW,velsEG,fluxEG)
vels, flux = import_data('spec.dat')

plot_spec(vels,flux)
