import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np


array = np.load('man_hanning_spectrum3.npy')

low_x = 100.
high_x = 400.
mask = (array[0]>=low_x) & (array[0]<=high_x)
peak_vels = array[0][mask]
peak_flux = array[1][mask]

peak_bit = 1.2 * np.max(peak_flux)


w50 = 12.9

rv = 418.8

print(peak_bit)
name ='CVnHI'

fig1,ax1 = plt.subplots()
ax1.plot(array[0],array[1],'k',linewidth=0.7,drawstyle='steps-mid')
ax1.hlines(0,np.min(array[0]),np.max(array[0]),linestyle='--',linewidth=0.6,alpha=0.6)
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