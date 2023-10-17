import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np


arrays = np.load('NGC4449/spectrum.npy')

low_x = 100.
high_x = 400.
mask = (arrays[0]>=low_x) & (arrays[0]<=high_x)
peak_vels = arrays[0][mask]
peak_flux = arrays[1][mask]

peak_bit = 1.2 * np.max(peak_flux)


w50 = 207.5
rv = 157.16
print(peak_bit)

fig1,ax1 = plt.subplots()
ax1.plot(arrays[0],arrays[1],label='gal')
ax1.set_xlabel('Velocity [km/s]')
ax1.set_ylabel('Flux per Beam Area [Jy/BA]')
#ax1.set_title(name)
ax1.legend()
ax1.set_xlim(rv-w50,rv+w50)
ax1.set_ylim(-peak_bit/5,peak_bit)
#fig1.savefig(name+'/spectrum.png',dpi=600)
plt.show()