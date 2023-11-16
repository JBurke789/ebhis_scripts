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
name = ' '
zoom_level = 1 #change  to zoom in. Always odd to have centered
peak_val = 22.4 #include if brighter gal in field of view



def crop_array(array,wcs):
    #crops to center of image 
    orig_shape = array.shape
    new_shape = (orig_shape[0]//zoom_level,orig_shape[1]//zoom_level)
    start_indices = ((orig_shape[0]-new_shape[0]) // 2, (orig_shape[1] - new_shape[1]) // 2)
    crop_array = array[start_indices[0]:start_indices[0]+new_shape[0],start_indices[1]:start_indices[1]+new_shape[1]]
    crop_wcs = wcs[start_indices[0]:start_indices[0]+new_shape[0],start_indices[1]:start_indices[1]+new_shape[1]]
    return crop_array,crop_wcs

def visualize_image(array,info,wcs):
    rescaled_array = array
    #rescaled_array = (array+abs(np.min(array))*1.00001)
    fig = plt.figure()
    ax=plt.subplot(projection=wcs)  
    #plt.imshow(rescaled_array,vmin = 44*0.2,vmax=0.8*44)#comment out if brighter gal in field of view
    #plt.imshow(rescaled_array)
    plt.imshow(rescaled_array,vmin = 0.2*peak_val, vmax=peak_val)
    ax.set_xlabel('Right Ascension')
    ax.set_ylabel('Declination')
    #ax.set_title(name)
    for gal in info:
        name = gal[0]
        print(name)
        ra = float(gal[1])
        dec = float(gal[2])
        if name == 'KK16' or name== 'AGC112521':
            pass
        else:
            #ax.text(ra,dec,name,transform=ax.get_transform('world'))
            #ax.scatter(ra, dec, 'o',transform=ax.get_transform('world'),edgecolor='white', facecolor='none')
            ax.annotate(name, xy=(ra, dec), xycoords=ax.get_transform('world'))
            ax.scatter(ra, dec, transform=ax.get_transform('world'), s=100,
           edgecolor='black', facecolor='none')
        ax.annotate('DDO217', xy=(352.4946,40.9903), xycoords=ax.get_transform('world'))
        ax.scatter(352.4946,40.9903, transform=ax.get_transform('world'), s=100,
           edgecolor='black', facecolor='none')
    cbar=plt.colorbar()
    cbar.formatter = ScalarFormatter(useMathText=False)
    cbar.ax.set_ylabel('K km/s')
    cbar.update_ticks()
    #contours = plt.contour(rescaled_array, levels=[0.5*np.max(rescaled_array)], colors='red', linewidths=1)#comment out if brighter gal in FOV
    contours = plt.contour(rescaled_array, levels=[0.5*peak_val], colors='red', linewidths=1)
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

path = 'mom0.fits'
info = np.load('group_info.npy')
print(info)
data,header,wcs = read_data(path)
new_array,new_wcs=crop_array(data[0],wcs)
#print(new_array.shape)
visualize_image(new_array,info,new_wcs)