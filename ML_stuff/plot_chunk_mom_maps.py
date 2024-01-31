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
    #masks values in an array that are outside of min and max value
    masked_array = np.ma.masked_outside(array, min, max)
    return masked_array

def get_rms(array):
    mu_sqrd =np.mean(array**2)
    rms = np.sqrt(mu_sqrd)
    return rms

def get_stats(array):
    #calculates the stats for each array. Run on each mom map and chunk
    return [np.mean(array),np.std(array),get_rms(array)]

def make_arrays(cube_name):
    #gets the arrays for each chunk for a single cube
    arrays_m0=[]#get arrays
    arrays_m1=[]
    arrays_m2=[]
    for i in range(4):
        array,header,wcs = read_data(cube_name,chunks[i],'m0')
        arrays_m0.append(array[0])
        array,header,wcs = read_data(cube_name,chunks[i],'m1')
        arrays_m1.append(array[0])
        array,header,wcs = read_data(cube_name,chunks[i],'m2')
        arrays_m2.append(array[0]) 
    return arrays_m0,arrays_m1,arrays_m2,wcs 

def make_plots(cube,m0,m1,m2,wcs):
    #plots all the chunks for each mom map for a single cube
    vis_mom0(cube,m0,wcs)#plot arrays
    vis_mom1(cube,m1,wcs)
    vis_mom2(cube,m2,wcs)

def all_stats(m0,m1,m2):
    #for a single cube, gets the stats from each chunk
    mean=[[],[],[]]
    std=[[],[],[]]
    rms=[[],[],[]]
    for chunk in range(4):
        #moment0
        stats=get_stats(arrays_m0[chunk])
        mean[0].append(stats[0])
        std[0].append(stats[1])
        rms[0].append(stats[2])
        #moment1 (mask so that only vel vals in interval are shown)
        masked_m1 = make_mask(arrays_m1[chunk],vels[chunk][0],vels[chunk][1])
        stats = get_stats(masked_m1)
        mean[1].append(stats[0])
        std[1].append(stats[1])
        rms[1].append(stats[2])
        #moment 2(mask so only vels in range are shown)
        masked_m2 = make_mask(arrays_m2[chunk],0,2000)
        stats=get_stats(masked_m2)
        mean[2].append(stats[0])
        std[2].append(stats[1])
        rms[2].append(stats[2])
    return mean,std,rms

def stats_plot(map,title):
    #plots the stats for each mom map for each chunk. compares cubes
    x = [1,2,3,4]
    fig,(ax1,ax2,ax3) = plt.subplots(3,1,sharex=True)
    for cube in range(5):
        ax1.plot(x,means[map][cube],label=str(cube+1))
        ax2.plot(x, stds[map][cube],label=str(cube+1))
        ax3.plot(x, rmss[map][cube],label=str(cube+1))
    ax1.set_ylabel('Mean')
    ax2.set_ylabel('Stand Dev')
    ax3.set_ylabel('RMS')
    ax3.set_xlabel('Chunk')
    plt.xticks(x)
    plt.suptitle(title)
    plt.tight_layout()
    plt.legend()
    plt.show()

#to be done for each cube
means =[[],[],[]]
stds=[[],[],[]]
rmss=[[],[],[]]

for i in range(5):
    cube='cube'+str(i)

    print('--------',cube,'--------')
    arrays_m0,arrays_m1,arrays_m2,wcs = make_arrays(cube)
    make_plots(cube,arrays_m0,arrays_m1,arrays_m2,wcs)
    mean,std,rms=all_stats(arrays_m0,arrays_m1,arrays_m2)
    for map in range(3):
        means[map].append(mean[map])
        stds[map].append(std[map])
        rmss[map].append(rms[map])
        

stats_plot(0,'Moment 0')
stats_plot(1,'Moment 1')
stats_plot(2,'Moment 2')
