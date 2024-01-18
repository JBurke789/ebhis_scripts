import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import astropy.io.fits as fits
from matplotlib.colors import LogNorm
import astropy.visualization
from astropy.wcs import WCS
from matplotlib.ticker import ScalarFormatter
from mpl_toolkits.axes_grid1 import make_axes_locatable

"""
makes mom map from fits file for single galaxy.
run in full list directory
"""


def read_data(filepath):
    hdul= fits.open(filepath)
    array = hdul[0].data
    header = hdul[0].header
    hdul.close()
    wcs=WCS(header)
    dropped = wcs.dropaxis(2)
    return(array,header,dropped)

def crop_array(array,wcs):
    #crops to center of image 
    orig_shape = array.shape
    new_shape = (orig_shape[0]//1,orig_shape[1]//1)
    start_indices = ((orig_shape[0]-new_shape[0]) // 2, (orig_shape[1] - new_shape[1]) // 2)
    crop_array = array[start_indices[0]:start_indices[0]+new_shape[0],start_indices[1]:start_indices[1]+new_shape[1]]
    crop_wcs = wcs[start_indices[0]:start_indices[0]+new_shape[0],start_indices[1]:start_indices[1]+new_shape[1]]
    return crop_array,crop_wcs

def visualize_image(array1,array2,wcs1,wcs2):
   
    fig = plt.figure()
    fig.suptitle('Moment 2 maps')
    
    fig.add_subplot(1,2,1,projection=wcs1)
    im1=plt.imshow(array1,vmin=0,vmax=110)
    plt.xlabel('RA')
    plt.ylabel('Dec')
    plt.title('MW')

    fig.add_subplot(1,2,2,projection=wcs2)
    im2=plt.imshow(array2,vmin=0,vmax=110)
    plt.xlabel('RA')
    plt.ylabel('Dec')
    plt.title('EG')

    fig.subplots_adjust(right=0.8)
    cbar_ax = fig.add_axes([0.85, 0.15, 0.05, 0.7])
    cbar = plt.colorbar(im1,cax=cbar_ax)
    cbar.set_label(' km/s')
    plt.show()



path1 = '..\..\..\Desktop\ML_stuff\MW_m2_map.fits'
data1,header1,wcs1 = read_data(path1)
MW_array,MW_wcs = crop_array(data1[0],wcs1)
path2 = '..\..\..\Desktop\ML_stuff\EG_m2_map.fits'
data2,header2,wcs2 = read_data(path2)
EG_array,EG_wcs = crop_array(data2[0],wcs2)


visualize_image(MW_array,EG_array,MW_wcs,EG_wcs)