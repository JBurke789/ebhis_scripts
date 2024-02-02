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
chunks=['chunk0','chunk1','chunk2','chunk3']
vels = [[300,2300],[2300,4300],[4300,6300],[6300,8300]]
  
def make_string(vel):
    string= str(vel[0])+ ' - '+str(vel[1])+ ' km/s '
    return string

def read_data(chunk,mom_map):
    filepath =chunk+'_'+mom_map+'.fits'
    hdul= fits.open(filepath)
    array = hdul[0].data
    header = hdul[0].header
    hdul.close()
    wcs=WCS(header)
    wcs = wcs.dropaxis(2)
    return(array[0],header,wcs)

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
    plt.vlines([15,30,45],0,75,'r',linewidth=0.5)
    plt.hlines([15,30,45,60],0,61,'r',linewidth=0.5)
    plt.title(make_string(vels[0]))

    fig.add_subplot(142,projection=wcs)
    im2=plt.imshow(array[1],vmin=min,vmax=max)
    plt.vlines([15,30,45],0,75,'r',linewidth=0.5)
    plt.hlines([15,30,45,60],0,61,'r',linewidth=0.5)
    plt.title(make_string(vels[1]))

    fig.add_subplot(143,projection=wcs)
    im3=plt.imshow(array[2],vmin=min,vmax=max)
    plt.title(make_string(vels[2]))
    plt.vlines([15,30,45],0,75,'r',linewidth=0.5)
    plt.hlines([15,30,45,60],0,61,'r',linewidth=0.5)
    
    fig.add_subplot(144,projection=wcs)
    im4=plt.imshow(array[3],vmin=min,vmax=max)
    plt.title(make_string(vels[3]))
    plt.vlines([15,30,45],0,75,'r',linewidth=0.5)
    plt.hlines([15,30,45,60],0,61,'r',linewidth=0.5)

    fig.subplots_adjust(right=0.8)
    cbar_ax = fig.add_axes([0.85, 0.15, 0.05, 0.7])
    cbar = plt.colorbar(im1,cax=cbar_ax)
    cbar.set_label('K km/s')
    plt.show()

def make_arrays():
    #gets the arrays for each chunk for a single cube
    arrays_m0=[]#get arrays
    arrays_m1=[]
    arrays_m2=[]
    for i in range(4):
        array,header,wcs = read_data(chunks[i],'m0')
        arrays_m0.append(array)
        array,header,wcs = read_data(chunks[i],'m1')
        arrays_m1.append(array)
        array,header,wcs = read_data(chunks[i],'m2')
        arrays_m2.append(array) 
    return arrays_m0,arrays_m1,arrays_m2,wcs 

def sub_array(array,x_lims,y_lims):
    new_array = array[y_lims[0]:y_lims[1],x_lims[0]:x_lims[1]]
    return new_array

def get_rms(array):
    mu_sqrd =np.mean(array**2)
    rms = np.sqrt(mu_sqrd)
    return rms

def get_stats(array):
    #calculates the stats for each array. Run on each mom map and chunk
    return [np.mean(array),np.std(array),get_rms(array)]

def all_stats(m0,m1,m2):
    #for a single cube, gets the stats from each chunk
    mean=[[],[],[]]
    std=[[],[],[]]
    rms=[[],[],[]]
    for chunk in range(4):
        #moment0
        stats=get_stats(m0[chunk])
        mean[0].append(stats[0])
        std[0].append(stats[1])
        rms[0].append(stats[2])
        #moment1 (mask so that only vel vals in interval are shown)
        '''masked_m1 = make_mask(arrays_m1[chunk],vels[chunk][0],vels[chunk][1])
        stats = get_stats(masked_m1)
        mean[1].append(stats[0])
        std[1].append(stats[1])
        rms[1].append(stats[2])
        #moment 2(mask so only vels in range are shown)
        masked_m2 = make_mask(arrays_m2[chunk],0,2000)
        stats=get_stats(masked_m2)
        mean[2].append(stats[0])
        std[2].append(stats[1])
        rms[2].append(stats[2])'''
    return mean,std,rms



arrays_m0,arrays_m1,arrays_m2,wcs  = make_arrays()


x_coords =[[0,14],[15,29],[30,44],[45,59]]
y_coords =[[0,14],[15,29],[30,44],[45,59],[60,75]]

mean=[[],[],[],[]]
std= [[],[],[],[]]
rms= [[],[],[],[]]
for i in range(len(chunks)):
    for y in range(5):
        for x in range(4): 
            sub = sub_array(arrays_m1[i],x_coords[x],y_coords[y])
            stats = get_stats(sub)
            mean[i].append(stats[0])
            std[i].append( stats[1])
            rms[i].append( stats[2])

x=[1,2,3,4]
ys=[[],[],[]]
for bit in range(20):
    y_single=[[],[],[]]
    for i in range(4):
        y_single[0].append(mean[i][bit])
        y_single[1].append(std[i][bit])
        y_single[2].append(rms[i][bit])
    ys[0].append(y_single[0])
    ys[1].append(y_single[1])
    ys[2].append(y_single[2])


fig,(ax1,ax2,ax3) = plt.subplots(3,1,sharex=True)
for y in ys[0]:
    ax1.plot(x,y)
for y in ys[1]:
    ax2.plot(x,y)
for y in ys[2]:
    ax3.plot(x,y)

ax1.set_ylabel('Mean')
ax2.set_ylabel('Stand Dev')
ax3.set_ylabel('RMS')
ax3.set_xlabel('Chunk')
plt.xticks(x)
plt.suptitle('Moment 1')
plt.tight_layout()
plt.legend()
plt.show(block=False)

'''
fig = plt.figure()
fig.suptitle(' - Moment 0 Maps')
fig.add_subplot()
im1=plt.imshow(gal_array,origin='lower')
plt.show(block=False)
'''
vis_mom0('',arrays_m1,wcs)