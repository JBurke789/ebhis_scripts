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
    return(array,header)

def make_string(vel):
    string= str(vel[0])+ ' - '+str(vel[1])+ ' km/s '
    return string

def visualize_image(array1,array2,array3,array4,array5,array6,array7,array8,min,max):
   
    fig = plt.figure()
    fig.suptitle('Moment 2 maps')
    
    fig.add_subplot(3,3,1)
    #im1=plt.imshow(array1,vmin=min,vmax=max*0.1)
    #im1=plt.imshow(array1,vmin=vels[0][0],vmax=vels[0][1])
    im1=plt.imshow(array1,vmin=0,vmax=1360)
    plt.title(make_string(vels[0]))
    plt.xlabel('')
    plt.ylabel('')
    cbar=plt.colorbar()
    cbar.formatter = ScalarFormatter(useMathText=False)
    cbar.ax.set_ylabel(' km/s')
    cbar.update_ticks()
    

    fig.add_subplot(332)
    #im2=plt.imshow(array2,vmin=min,vmax=max)
    #im2=plt.imshow(array2,vmin=vels[1][0],vmax=vels[1][1])
    im2=plt.imshow(array2,vmin=0,vmax=2500)
    plt.title(make_string(vels[1]))
    cbar=plt.colorbar()
    cbar.formatter = ScalarFormatter(useMathText=False)
    cbar.ax.set_ylabel(' km/s')
    cbar.update_ticks()

    fig.add_subplot(333)
    #im3=plt.imshow(array3,vmin=min,vmax=max)
    #im3=plt.imshow(array3,vmin=vels[2][0],vmax=vels[2][1])
    im3=plt.imshow(array3,vmin=0,vmax=3500)
    plt.title(make_string(vels[2]))
    cbar=plt.colorbar()
    cbar.formatter = ScalarFormatter(useMathText=False)
    cbar.ax.set_ylabel(' km/s')
    cbar.update_ticks()

    fig.add_subplot(334)
    #im4=plt.imshow(array4,vmin=min,vmax=max)
    #im4=plt.imshow(array4,vmin=vels[3][0],vmax=vels[3][1])
    im4=plt.imshow(array4,vmin=0,vmax=2500)
    plt.title(make_string(vels[3]))
    cbar=plt.colorbar()
    cbar.formatter = ScalarFormatter(useMathText=False)
    cbar.ax.set_ylabel(' km/s')
    cbar.update_ticks()

    fig.add_subplot(335)
    #im5=plt.imshow(array5,vmin=min,vmax=max)
    #im5=plt.imshow(array5,vmin=vels[4][0],vmax=vels[4][1])
    im5=plt.imshow(array5,vmin=0,vmax=2500)
    plt.title(make_string(vels[4]))
    cbar=plt.colorbar()
    cbar.formatter = ScalarFormatter(useMathText=False)
    cbar.ax.set_ylabel(' km/s')
    cbar.update_ticks()

    fig.add_subplot(336)
    #im6=plt.imshow(array6,vmin=min,vmax=max)
    #im6=plt.imshow(array6,vmin=vels[5][0],vmax=vels[5][1])
    im6=plt.imshow(array6,vmin=0,vmax=2500)
    plt.title(make_string(vels[5]))
    cbar=plt.colorbar()
    cbar.formatter = ScalarFormatter(useMathText=False)
    cbar.ax.set_ylabel(' km/s')
    cbar.update_ticks()

    fig.add_subplot(337)
    #im7=plt.imshow(array7,vmin=min,vmax=max)
    #im7=plt.imshow(array7,vmin=vels[6][0],vmax=vels[6][1])
    im7=plt.imshow(array7,vmin=0,vmax=2500)
    plt.title(make_string(vels[6]))
    cbar=plt.colorbar()
    cbar.formatter = ScalarFormatter(useMathText=False)
    cbar.ax.set_ylabel(' km/s')
    cbar.update_ticks()

    fig.add_subplot(338)
    #im8=plt.imshow(array8,vmin=min,vmax=max)
    #im8=plt.imshow(array8,vmin=vels[7][0],vmax=vels[7][1])
    im8=plt.imshow(array8,vmin=0,vmax=3500)
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

def make_mask(array, min,max):
    masked_array = np.ma.masked_outside(array, min, max)
    return masked_array

def rms(array):
    mu_sqrd =np.mean(array**2)
    rms = np.sqrt(mu_sqrd)
    return rms

def get_stats(array):
    print('Mean:    ',np.mean(array))
    print('Sigma:   ',np.std(array))
    print('RMS:     ',rms(array))

arrays =[]

for chunk in out_files:
    path = chunk+'_m2.fits'
    data,header = read_data(path)
    arrays.append(data[0])

for i in range(len(out_files)):
    print('---- Chunk '+str(i+1)+' -----')
    #masked = arrays[i]
    #masked = make_mask(arrays[i],vels[i][0],vels[i][1])
    masked = make_mask(arrays[i],0,2500)
    get_stats(masked    )

max,min=min_max(arrays)

visualize_image(arrays[0],arrays[1],arrays[2],arrays[3],arrays[4],arrays[5],arrays[6],arrays[7],-200,500)