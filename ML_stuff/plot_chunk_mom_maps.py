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
out_files=['chunk1.im','chunk2.im','chunk3.im','chunk4.im','chunk5.im','chunk6.im','chunk7.im','chunk8.im']
vels = [[-1358.0,0],[0.0,2500],[2500,5000],[5000,7500],[7500,10000],[10000,12500],[12500,15000],[15000,18500]]
  

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

def make_string(vel):
    string= str(vel[0])+ ' - '+str(vel[1])+ ' km/s '
    return string

def visualize_image(array1,array2,array3,array4,array5,array6,array7,array8,wcs,min,max):
   
    fig = plt.figure()
    fig.suptitle('Moment 1 maps')
    
    fig.add_subplot(3,3,1)
    im1=plt.imshow(array1,vmin=vels[0][0],vmax=vels[0][1])
    plt.title(make_string(vels[0]))
    plt.xlabel('')
    plt.ylabel('')
    cbar=plt.colorbar()
    cbar.formatter = ScalarFormatter(useMathText=False)
    cbar.ax.set_ylabel(' km/s')
    cbar.update_ticks()
    

    fig.add_subplot(332)
    im2=plt.imshow(array2,vmin=vels[1][0],vmax=vels[1][1])
    plt.title(make_string(vels[1]))
    cbar=plt.colorbar()
    cbar.formatter = ScalarFormatter(useMathText=False)
    cbar.ax.set_ylabel(' km/s')
    cbar.update_ticks()

    fig.add_subplot(333)
    im2=plt.imshow(array3,vmin=vels[2][0],vmax=vels[2][1])
    plt.title(make_string(vels[2]))
    cbar=plt.colorbar()
    cbar.formatter = ScalarFormatter(useMathText=False)
    cbar.ax.set_ylabel(' km/s')
    cbar.update_ticks()

    fig.add_subplot(334)
    im2=plt.imshow(array4,vmin=vels[3][0],vmax=vels[3][1])
    plt.title(make_string(vels[3]))
    cbar=plt.colorbar()
    cbar.formatter = ScalarFormatter(useMathText=False)
    cbar.ax.set_ylabel(' km/s')
    cbar.update_ticks()

    fig.add_subplot(335)
    im2=plt.imshow(array5,vmin=vels[4][0],vmax=vels[4][1])
    plt.title(make_string(vels[4]))
    cbar=plt.colorbar()
    cbar.formatter = ScalarFormatter(useMathText=False)
    cbar.ax.set_ylabel(' km/s')
    cbar.update_ticks()

    fig.add_subplot(336)
    im2=plt.imshow(array6,vmin=vels[5][0],vmax=vels[5][1])
    plt.title(make_string(vels[5]))
    cbar=plt.colorbar()
    cbar.formatter = ScalarFormatter(useMathText=False)
    cbar.ax.set_ylabel(' km/s')
    cbar.update_ticks()

    fig.add_subplot(337)
    im2=plt.imshow(array7,vmin=vels[6][0],vmax=vels[6][1])
    plt.title(make_string(vels[6]))
    cbar=plt.colorbar()
    cbar.formatter = ScalarFormatter(useMathText=False)
    cbar.ax.set_ylabel(' km/s')
    cbar.update_ticks()

    fig.add_subplot(338)
    im2=plt.imshow(array8,vmin=vels[7][0],vmax=vels[7][1])
    plt.title(make_string(vels[7]))
    cbar=plt.colorbar()
    cbar.formatter = ScalarFormatter(useMathText=False)
    cbar.ax.set_ylabel(' km/s')
    cbar.update_ticks()

    plt.show()

def min_max(arrays):
    maxes=[]
    mins=[]
    for array in arrays:
        maxes.append(np.max(array))
        mins.append(np.min(array))
    return max(maxes),min(mins)


arrays =[]
wcss=[]
for chunk in out_files:
    path = chunk+'_m1.fits'
    data,header,wcs = read_data(path)
    array,wcs = crop_array(data[0],wcs)
    arrays.append(array)
    wcss.append(wcs)


max,min=min_max(arrays)



visualize_image(arrays[0],arrays[1],arrays[2],arrays[3],arrays[4],arrays[5],arrays[6],arrays[7],wcs[0],min,max)