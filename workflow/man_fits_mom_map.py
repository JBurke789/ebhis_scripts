import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import astropy.io.fits as fits
from matplotlib.colors import LogNorm
import astropy.visualization
from astropy.wcs import WCS
from matplotlib.ticker import ScalarFormatter





def crop_array(array,wcs):
    #crops to center of image 
    orig_shape = array.shape
    new_shape = (orig_shape[0]//5,orig_shape[1]//5)
    start_indices = ((orig_shape[0]-new_shape[0]) // 2, (orig_shape[1] - new_shape[1]) // 2)
    crop_array = array[start_indices[0]:start_indices[0]+new_shape[0],start_indices[1]:start_indices[1]+new_shape[1]]
    crop_wcs = wcs[start_indices[0]:start_indices[0]+new_shape[0],start_indices[1]:start_indices[1]+new_shape[1]]
    return crop_array,crop_wcs

def visualize_image(array,name,wcs):
    rescaled_array = (array+abs(np.min(array))*1.00001)
    fig = plt.figure()
    ax=plt.subplot(projection=wcs)  
    plt.imshow(rescaled_array,vmin = 10, vmax=50)
    ax.set_xlabel('Right Ascension')
    ax.set_ylabel('Declination')
    ax.set_title(name)
    cbar=plt.colorbar()
    cbar.formatter = ScalarFormatter(useMathText=False)
    cbar.ax.set_ylabel('K km/s')
    cbar.update_ticks()
    contours = plt.contour(rescaled_array, levels=[0.5*np.max(rescaled_array)], colors='red', linewidths=1)
    fig_name = '/users/jburke/Desktop/results/mom0_maps/'+name+'.png'
    #plt.show()
    #plt.savefig(fig_name)
    plt.show()

def read_data(filepath):
    hdul= fits.open(filepath)
    array = hdul[0].data
    header = hdul[0].header
    hdul.close()
    wcs=WCS(header)
    dropped = wcs.dropaxis(2)
    return(array,header,dropped)

name = 'NGC4288'
path = name+'/'+name+'mom0.fits'
data,header,wcs = read_data(path)
new_array,new_wcs=crop_array(data[0],wcs)
print(new_array.shape)
visualize_image(new_array,name,new_wcs)