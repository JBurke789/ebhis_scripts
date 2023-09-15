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
import warnings
# import fit models from the lmfit package
import lmfit
from lmfit import Model
from lmfit.models import GaussianModel

"""
run script in directory of galaxy


extracting part of spectrum containing galaxy
"""
def import_spectrum(array):
    vel = array[0]
    inner_flux = array[1]
    bg_flux = array[3]
    return vel, inner_flux,bg_flux


def peak_extracting(vel,inner_flux,bg_flux):
    def on_click(event):
        if event.inaxes is not None:
            x = event.xdata
            x_lims.append(x)
            print(x)

    #plot spectrum to select baseline regions
    print('Select region around galaxy peak.')
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
    clean_flux= inner_flux-bg_flux
    x_vals=[]
    y_vals=[]
    for i in pairs:
        low = i[0]
        high = i[1]  
        filtered_values = [(x_val, y_val) for x_val, y_val in zip(vel, clean_flux) if low <= x_val <= high]
        x_bit,y_bit = zip(*filtered_values)
        for j in x_bit:
            x_vals.append(j)
        for k in y_bit:
            y_vals.append(k)
    
    return x_vals, y_vals


array = np.load('spectrum.npy')
velo,flux,bgflux=import_spectrum(array)
x_vals=[]
y_vals=[]
x_vals,y_vals= peak_extracting(velo,flux,bgflux)

fig1,ax1 = plt.subplots()
ax1.plot(x_vals,y_vals,label='galaxy')
ax1.set_xlabel('Velocity [km/s]')
ax1.set_ylabel('Flux per Beam Area [Jy/BA]')
ax1.legend()
plt.show(block=False)


"""
fitting galaxy spectrum
"""

x_vals=np.array(x_vals)
y_vals=np.array(y_vals)

peak = GaussianModel()

pars= peak.guess(y_vals,x=x_vals,amplitude=3)
result = peak.fit(y_vals,pars,x=x_vals)
print(result.fit_report())
ax1.plot(x_vals,result.best_fit)
print('center: ',result.params['center'].value)
print('fwhm: ',result.params['fwhm'].value)

print('max: ',max(y_vals))

plt.show()

