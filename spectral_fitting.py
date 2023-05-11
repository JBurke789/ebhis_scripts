import matplotlib.pyplot as plt
import numpy as np
import scipy as sp
import warnings
from astropy import units as u
from astropy.modeling import models
import specutils




#load spectral data from file and assign to arrays
array = np.load('spectrum.npy')
velo = array[0]
temp = array[1]

#plot quick spectrum
fig1,ax1 = plt.subplots()
ax1.plot(velo,temp)
ax1.set_xlabel('velocity [km/s]')
ax1.set_ylabel('brightness temp [K]')
plt.show()

#baseline correction
spectrum = specutils.spectra.Spectrum1D(flux=temp*u.Jy,spectral_axis=velo*u.um)
with warnings.catch_warnings():
    warnings.simplefilter('ignore')
    gl_fit = fit_generic_continuum(spectrum)