import numpy as np
import csv
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import astropy.io.fits as fits
from matplotlib.colors import LogNorm
from matplotlib.ticker import LogLocator
import astropy.visualization
from matplotlib.colors import LogNorm
from astropy.wcs import WCS

'''makes python plots of fits moment 0 maps'''
def crop_array(array):
    orig_shape = array.shape
    new_shape = (orig_shape[0]//3,orig_shape[1]//3)
    start_indices = ((orig_shape[0]-new_shape[0]) // 2, (orig_shape[1] - new_shape[1]) // 2)
    crop_array = array[start_indices[0]:start_indices[0]+new_shape[0],start_indices[1]:start_indices[1]+new_shape[1]]
    return crop_array

def visualize_image(array,name,wcs):
    rescaled_array = (array+abs(np.min(array))*1.00001)
    fig = plt.figure()
    ax=plt.subplot(projection=wcs)
    #ax=plt.subplot()
    if np.max(rescaled_array)<= 20:
        tick_loc = [0.2*np.max(rescaled_array),5,8,10,np.max(rescaled_array)]
        tick_lab = ["{:.1f}".format(0.2*np.max(rescaled_array)),'5','8','10',"{:.1f}".format(np.max(rescaled_array))]
        
    elif np.max(rescaled_array)<= 100 and np.max(rescaled_array)>20:
        tick_loc = [0.2*np.max(rescaled_array),5,10,20,40,80,np.max(rescaled_array)]
        tick_lab = ["{:.1f}".format(0.2*np.max(rescaled_array)),'5','10','20','40','80',"{:.1f}".format(np.max(rescaled_array))]
        
    else:
        tick_loc=[0.2*np.max(rescaled_array),10,50,100,200,300,500,np.max(rescaled_array)]
        tick_lab= ["{:.1f}".format(0.2*np.max(rescaled_array)),'10','50','100','200','300','500',"{:.1f}".format(np.max(rescaled_array))]
    #histogram = plt.hist(rescaled_array.flatten(), bins='auto')    
    plt.imshow(rescaled_array,norm=LogNorm(),vmin = 0.2*np.max(rescaled_array))

    ax.set_xlabel('Right Ascension')
    ax.set_ylabel('Declination')
    ax.set_title(name)
    print(np.max(rescaled_array))
    cbar=plt.colorbar(ticks=tick_loc)
    cbar.ax.set_yticklabels(tick_lab)
    cbar.ax.set_ylabel('K km/s')
    contours = plt.contour(rescaled_array, levels=[0.5*np.max(rescaled_array)], colors='red', linewidths=1)
    plt.show()

def read_data(filepath):
    hdul= fits.open(filepath)
    array = hdul[0].data
    header = hdul[0].header
    hdul.close()
    wcs=WCS(header)
    dropped = wcs.dropaxis(2)
    return(array,header,dropped)


gal_names = []
with open('/users/jburke/ebhis_scripts/workflow_results/final_results.csv','r') as f:
    reader = csv.reader(f)
    header = next(reader)
    for row in reader:
        gal_names.append(row[0])

for name in gal_names:
    if name =='HIZSS003':
        pass
    else:
        print(name)
        path = name+'/'+name+'mom0.fits'
        data,header,wcs = read_data(path)
        new_array=crop_array(data[0])
        visualize_image(new_array,name,wcs)