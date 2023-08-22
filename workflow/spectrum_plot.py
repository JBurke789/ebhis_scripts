import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np


array = np.load('NGC6946/spectrum.npy')
velo = array[0]
temp = array[1]
temp2 = array[2]




galaxy_flux = temp-temp2
fig1,ax1 = plt.subplots()
ax1.plot(velo,temp)
ax1.plot(velo,temp2)
ax1.plot(velo,galaxy_flux)
ax1.set_xlabel('Velocity [km/s]')
ax1.set_ylabel('Temp [k]')
plt.show()