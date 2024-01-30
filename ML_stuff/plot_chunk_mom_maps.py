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
chunks=['chunk0.im','chunk1.im','chunk2.im','chunk3.im']
vels = [[300,2300],[2300,4300],[4300,6300],[6300,8300]]
  

def read_data(cube,chunk,mom_map):
    filepath = cube+chunk+'_'+mom_map+'.fits'
    hdul= fits.open(filepath)
    array = hdul[0].data
    header = hdul[0].header
    hdul.close()
    wcs=WCS(header)
    wcs = wcs.dropaxis(2)
    return(array,header,wcs)

def make_string(vel):
    string= str(vel[0])+ ' - '+str(vel[1])+ ' km/s '
    return string

def min_max(arrays):
    maxes=[]
    mins=[]
    for array in arrays:
        maxes.append(np.max(array))
        mins.append(np.min(array))
    return max(maxes),min(mins)

def vis_mom0(cube,array,wcs):
    max,min = min_max(array)
    fig = plt.figure()
    fig.suptitle(cube+' - Moment 0 Maps')
    
    fig.add_subplot(141,projection=wcs)
    im1=plt.imshow(array[0],vmin=min,vmax=max)
    plt.title(make_string(vels[0]))

    fig.add_subplot(142,projection=wcs)
    im2=plt.imshow(array[1],vmin=min,vmax=max)
    plt.title(make_string(vels[1]))

    fig.add_subplot(143,projection=wcs)
    im3=plt.imshow(array[2],vmin=min,vmax=max)
    plt.title(make_string(vels[2]))
    
    fig.add_subplot(144,projection=wcs)
    im4=plt.imshow(array[3],vmin=min,vmax=max)
    plt.title(make_string(vels[3]))

    fig.subplots_adjust(right=0.8)
    cbar_ax = fig.add_axes([0.85, 0.15, 0.05, 0.7])
    cbar = plt.colorbar(im1,cax=cbar_ax)
    cbar.set_label('K km/s')
    plt.show()

def vis_mom1(cube,array,wcs):
    fig = plt.figure()
    fig.suptitle(cube+' - Moment 1 Maps')
    
    fig.add_subplot(141,projection=wcs)
    im1=plt.imshow(array[0],vmin=300,vmax=2300)
    plt.title(make_string(vels[0]))
    cbar=plt.colorbar()
    cbar.formatter = ScalarFormatter(useMathText=False)
    cbar.ax.set_ylabel('km/s')
    cbar.update_ticks()

    fig.add_subplot(142,projection=wcs)
    im2=plt.imshow(array[1],vmin=2300,vmax=4300)
    plt.title(make_string(vels[1]))
    cbar=plt.colorbar()
    cbar.formatter = ScalarFormatter(useMathText=False)
    cbar.ax.set_ylabel('km/s')
    cbar.update_ticks()

    fig.add_subplot(143,projection=wcs)
    im3=plt.imshow(array[2],vmin=4300,vmax=6300)
    plt.title(make_string(vels[2]))
    cbar=plt.colorbar()
    cbar.formatter = ScalarFormatter(useMathText=False)
    cbar.ax.set_ylabel('km/s')
    cbar.update_ticks()

    fig.add_subplot(144,projection=wcs)
    im4=plt.imshow(array[3],vmin=6300,vmax=8300)
    plt.title(make_string(vels[3]))
    cbar=plt.colorbar()
    cbar.formatter = ScalarFormatter(useMathText=False)
    cbar.ax.set_ylabel('km/s')
    cbar.update_ticks()
    plt.show()

def vis_mom2(cube,array,wcs):
    fig = plt.figure()
    fig.suptitle(cube+' - Moment 2 Maps')
    
    fig.add_subplot(141,projection=wcs)
    im1=plt.imshow(array[0],vmin=0,vmax=2000)
    plt.title(make_string(vels[0]))

    fig.add_subplot(142,projection=wcs)
    im2=plt.imshow(array[1],vmin=0,vmax=2000)
    plt.title(make_string(vels[1]))

    fig.add_subplot(143,projection=wcs)
    im3=plt.imshow(array[2],vmin=0,vmax=2000)
    plt.title(make_string(vels[2]))

    fig.add_subplot(144,projection=wcs)
    im4=plt.imshow(array[3],vmin=0,vmax=2000)
    plt.title(make_string(vels[3]))

    fig.subplots_adjust(right=0.8)
    cbar_ax = fig.add_axes([0.85, 0.15, 0.05, 0.7])
    cbar = plt.colorbar(im1,cax=cbar_ax)
    cbar.set_label('km/s')
    plt.show()

def make_mask(array,min,max):
    masked_array = np.ma.masked_outside(array, min, max)
    return masked_array

def rms(array):
    mu_sqrd =np.mean(array**2)
    rms = np.sqrt(mu_sqrd)
    return rms

def get_stats(array):
    return [np.mean(array),np.std(array),rms(array)]

#to be done for each cube
cube = 'cube0'
arrays_m0=[]#get arrays
arrays_m1=[]
arrays_m2=[]
for i in range(4):
    array,header,wcs = read_data(cube,chunks[i],'m0')
    arrays_m0.append(array[0])
    array,header,wcs = read_data(cube,chunks[i],'m1')
    arrays_m1.append(array[0])
    array,header,wcs = read_data(cube,chunks[i],'m2')
    arrays_m2.append(array[0])    
vis_mom0(cube,arrays_m0,wcs)#plot arrays
vis_mom1(cube,arrays_m1,wcs)
vis_mom2(cube,arrays_m2,wcs)


m0_mean=[]
m0_std=[]
m0_rms=[]
for chunk in range(4):
    stats=get_stats(arrays_m0[chunk])
    print(stats)
    #do for other mom maps

'''
for j in range(5):
    cube = 'cube'+str(j)
    arrays=[]
    for i in range(4):
        array,header,wcs = read_data(cube,chunks[i],'m0')
        arrays.append(array[0])
    vis_mom0(cube,arrays,wcs)

done=input('y:')
'''



"""

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

visualize_image(arrays[0],arrays[1],arrays[2],arrays[3],arrays[4],arrays[5],arrays[6],arrays[7],-200,500)"""