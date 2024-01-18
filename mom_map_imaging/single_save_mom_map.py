import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import astropy.io.fits as fits
from matplotlib.colors import LogNorm
import astropy.visualization
from astropy.wcs import WCS
from matplotlib.ticker import ScalarFormatter

"""
makes mom map from fits file for single galaxy.
run in full list directory
"""
name = 'EG'
max_val=3.2
zoom_level = 1 #change  to zoom in. Always odd to have centered
#peak_val = 8 #include if brighter gal in field of view



def crop_array(array,wcs):
    #crops to center of image 
    orig_shape = array.shape
    new_shape = (orig_shape[0]//zoom_level,orig_shape[1]//zoom_level)
    start_indices = ((orig_shape[0]-new_shape[0]) // 2, (orig_shape[1] - new_shape[1]) // 2)
    crop_array = array[start_indices[0]:start_indices[0]+new_shape[0],start_indices[1]:start_indices[1]+new_shape[1]]
    crop_wcs = wcs[start_indices[0]:start_indices[0]+new_shape[0],start_indices[1]:start_indices[1]+new_shape[1]]
    return crop_array,crop_wcs

def visualize_image(array,name,wcs):
    #rescaled_array = (array+abs(np.min(array))*1.00001)
    rescaled_array = array
    fig = plt.figure()
    ax=plt.subplot(projection=wcs)  
    plt.imshow(rescaled_array)#comment out if brighter gal in field of view
    #plt.imshow(rescaled_array,vmin = 0.2*peak_val, vmax=peak_val
    ax.set_xlabel('Right Ascension')
    ax.set_ylabel('Declination')
    ax.set_title('MW moment 0')
    cbar=plt.colorbar()
    cbar.formatter = ScalarFormatter(useMathText=False)
    cbar.ax.set_ylabel(' K km/s')
    cbar.update_ticks()
    #contours = plt.contour(rescaled_array, levels=[0.5*np.max(rescaled_array)], colors='red', linewidths=1)#comment out if brighter gal in FOV
    #contours = plt.contour(rescaled_array, levels=[0.5*peak_val], colors='red', linewidths=1)
    #fig_name = '/users/jburke/Desktop/results/mom0_maps/'+name+'.png'
    plt.show()

def read_data(filepath):
    hdul= fits.open(filepath)
    array = hdul[0].data
    header = hdul[0].header
    hdul.close()
    wcs=WCS(header)
    dropped = wcs.dropaxis(2)
    return(array,header,dropped)

path = 'MW_m0_map.fits'
data,header,wcs = read_data(path)
new_array,new_wcs=crop_array(data[0],wcs)
print(new_array.shape)
visualize_image(new_array,name,new_wcs)