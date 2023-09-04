import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np
import csv


array = np.load('ann_spectrum.npy')

vel = array[0]
inner_flux = array[1]
bg_flux = array[2]


fig1,ax1 = plt.subplots()
ax1.plot(array[0],array[1],label='galaxy')
ax1.plot(vel,bg_flux,label='annulus')
ax1.set_xlabel('Velocity [km/s]')
ax1.set_ylabel('Flux per Beam Area [Jy/BA]')
#ax1.set_xlim(-10,10)
ax1.legend()
#fig1.savefig(name+'/spectrum.png',dpi=600)



def on_click(event):
    if event.inaxes is not None:
        x, y = event.xdata, event.ydata
        print(x,y)

fig1.canvas.mpl_connect('button_press_event', on_click)

plt.show()