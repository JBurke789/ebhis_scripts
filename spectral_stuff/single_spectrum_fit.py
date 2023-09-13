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

"""
run in directory of galaxy
"""
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
    
    return x_vals, y_vals


array = np.load('spectrum.npy')
velo,flux,bgflux=import_spectrum(array)
x_vals,y_vals= peak_extracting(velo,flux,bgflux)

fig1,ax1 = plt.subplots()
ax1.plot(x_vals,y_vals,label='galaxy')
ax1.set_xlabel('Velocity [km/s]')
ax1.set_ylabel('Flux per Beam Area [Jy/BA]')
ax1.legend()
plt.show(block=False)

#fitting with a single gaussian
def gauss(p,x):#define gaussian function
    return p[0]*np.exp( -(x-p[1])**2 /(2*p[2]**2)) +p[3]
def resids(p):#define vector of residuals
    return gauss(p,x_vals) - y_vals
#initial guess of parameters
#p[0]= amplitude- value of peak
#p[1]= mean- peak center velocity
#p[2]= standard deviation, slightly above half of height 
#p[3]= offset
p_init = [0, 0, 0, 0.]
p_init[0] = input('Amplitude: ')
p_init[1] = input('Mean (peak centre): ')
p_init[2] = input('Standev (50pc bw):')
#run optimization
out = sp.optimize.least_squares(resids,p_init)
print(out.x)#print out parameters found by the fitting
ax1.plot(x_vals,gauss(out.x,x_vals))#plot fit
plt.show()