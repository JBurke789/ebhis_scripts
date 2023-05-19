import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np
import scipy as sp
from scipy import optimize
from scipy import integrate

"""
npy file now contains temp and velocity. need to change to flux using conversion.
"""

#load spectral data from file and assign to arrays
array = np.load('spectrum.npy')
velo = array[0]
temp = array[1]

#plot quick spectrum
fig1,ax1 = plt.subplots()
ax1.plot(velo,temp)
ax1.set_xlabel('Velocity [km/s]')
ax1.set_ylabel('Specific flux [Jy/BA]')

#fitting with a single gaussian
def gauss(p,x):#define gaussian function
    return p[0]*np.exp( -(x-p[1])**2 /(2*p[2]**2)) +p[3]
def resids(p):#define vector of residuals
    return gauss(p,velo) - flux
#initial guess of parameters
#p[0]= amplitude- value of peak
#p[1]= mean- peak center velocity
#p[2]= standard deviation, slightly above half of height 
#p[3]= offset
p_init = [610., 160., 60., 0.]
#run optimization
out = sp.optimize.least_squares(resids,p_init)
print(out.x)#print out parameters found by the fitting
ax1.plot(velo,gauss(out.x,velo))#plot fit
plt.show()

#integrate to get total flux
tot_flux = sp.integrate.simps(flux,velo)
print(tot_flux)

H0 = 67.7 #planck collab 2018
r = lambda vel: vel/H0 #give vel in km/s returns distance in Mpc

def mass(vel,flux_int):#returns HI mass in units of solar masses
    return 2.36e5*(r(vel)**2)*flux_int
print(r(out.x[1]))
mass_HI =  "{:.2e}".format(mass(out.x[1],tot_flux))
print('HI mass: ')
print(mass_HI)





