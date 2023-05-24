import matplotlib
matplotlib.use('tkagg')
import matplotlib.pyplot as plt
import numpy as np
import scipy as sp
from scipy import optimize
from scipy import integrate


#load spectral data from file and assign to arrays
array = np.load('multi_spectrum.npy')
velo = array[0]
temp = array[1]
bg_temp = array[2]
cal_temp = temp-bg_temp#background subtracted temp

#plot quick spectrum
fig1,ax1 = plt.subplots()
ax1.plot(velo,temp)
ax1.set_xlabel('Velocity [km/s]')
ax1.set_ylabel('Temp [k]')
ax1.plot(velo,bg_temp)


fig2,ax2=plt.subplots()
ax2.plot(velo,cal_temp)
ax2.set_xlabel('Velocity [km/s]')
ax2.set_ylabel('Temp [k]')
#plt.show()


#integrate to get total flux
tot_temp = sp.integrate.simps(cal_temp[30:90],velo[30:90])
print(velo[30:90])
print(tot_temp)