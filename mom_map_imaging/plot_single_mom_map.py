import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import astropy.io.fits as fits
from matplotlib.colors import LogNorm
import astropy.visualization
from astropy.wcs import WCS
from matplotlib.ticker import ScalarFormatter

def read_data(filepath):
    hdul= fits.open(filepath)
    array = hdul[0].data
    header = hdul[0].header
    hdul.close()
    wcs=WCS(header)
    dropped = wcs.dropaxis(2)
    return(array,header,dropped)

def plot_m0(array,wcs):
    fig = plt.figure()
    
    fig.add_subplot(projection=wcs)
    im1=plt.imshow(array,vmin=np.nanmin(array),vmax=np.nanmax(array))
    plt.xlabel('RA')
    plt.ylabel('Dec')

    
    cbar=plt.colorbar()
    cbar.formatter = ScalarFormatter(useMathText=False)
    cbar.ax.set_ylabel('K km/s')
    cbar.update_ticks()
    plt.show()

def plot_m1(array,wcs):
    fig = plt.figure()
    
    fig.add_subplot(projection=wcs)
    im1=plt.imshow(array,vmin=-606,vmax=-75)
    plt.xlabel('RA')
    plt.ylabel('Dec')

    
    cbar=plt.colorbar()
    cbar.formatter = ScalarFormatter(useMathText=False)
    cbar.ax.set_ylabel(' km/s')
    cbar.update_ticks()
    plt.show()

m0,m0_h,wcs = read_data(r'\Users\jonb7\OneDrive\Desktop\masked_mom0.fits')
m1,m1_h,wcs = read_data(r'\Users\jonb7\OneDrive\Desktop\masked_mom1.fits')

plot_m0(m0[0],wcs)
plot_m1(m1[0],wcs)



