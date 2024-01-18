import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np
import csv

def make_arrays(groupID):
    index = ['0','1','2','3','4']
    names=[]
    for i in index:
        filename= '../Desktop/group_spectra/group'+groupID+'_spectrum_h'+i+'.npy'
        names.append(filename)
    arrays=[]
    for name in names:
        data = np.load(name)
        arrays.append(data)

    return arrays[0],arrays[1],arrays[2],arrays[3],arrays[4] 

def plot_all_spectra(h0,h1,h2,h3,h4):
    fig,ax = plt.subplots()
    ax.plot(h0[0],h0[1]-h0[2],label='H=0')
    ax.plot(h1[0],h1[1]-h1[2],label='H=1')
    ax.plot(h2[0],h2[1]-h2[2],label='H=2')
    ax.plot(h3[0],h3[1]-h3[2],label='H=3')
    ax.plot(h4[0],h4[1]-h4[2],label='H=4')
    ax.hlines(0,xmin=np.min(h0[0]),xmax=np.max(h0[0]))
    ax.legend()
    ax.set_xlabel('vel')
    ax.set_ylabel('flux')
    plt.show(block=False)

def plot_single_spec(array):
    fig,ax=plt.subplots()
    ax.plot(array[0],array[1]-array[2])
    ax.hlines(0,xmin=np.min(array[0]),xmax=np.max(array[0]))
    ax.set_xlabel('Velocity [km/s]')
    ax.set_ylabel('Flux per Beam Area [Jy/BA]')
    plt.show(block=False)

    low_x = float(input('low vel val: '))
    high_x = float(input('high vel val: '))
    mask = (array[0]>=low_x) & (array[0]<=high_x)
    peak_vels = array[0][mask]
    peak_flux = array[1][mask]-array[2][mask]
    plt.close()
    peak_index = np.argmax(peak_flux)
    max_val = peak_flux[peak_index]
    hm = max_val/2.0
    
    l_index = 0
    while peak_flux[l_index] < hm:
        l_index+=1
    r_index = len(peak_vels)-1
    while peak_flux[r_index]<hm:
        r_index-=1
    fwhm=abs(peak_vels[r_index]-peak_vels[l_index])
    step_size = abs(peak_vels[peak_index]-peak_vels[peak_index-1])
    rad_vel = (peak_vels[r_index]+peak_vels[l_index])/2.0
    print('FWHM: ',fwhm,' +/- ', step_size,' km/s')
    print('RV: ',rad_vel, ' +/- ', step_size*2,' km/s')
    return rad_vel,fwhm,step_size
    

def final_spec(array,rv,w50):
    fig1,ax1 = plt.subplots()
    ax1.plot(array[0],array[1]-array[2],'k',linewidth=0.7,drawstyle='steps-mid')
    ax1.hlines(0,np.min(array[0]),np.max(array[0]),linestyle='--',linewidth=0.6,alpha=0.6)
    ax1.set_xlabel('Velocity [km/s]')
    ax1.set_ylabel('Flux per Beam Area [Jy/BA]')
    ax1.vlines(rv,np.min(array[1]-array[2]),np.max(array[1]-array[2]),'r',linewidth=0.7,alpha=0.5,label='v_r')
    closest_index1 = np.argmin(np.abs(array[0] - rv-0.5*w50))
    closest_index2 = np.argmin(np.abs(array[0] - rv+0.5*w50))
    ax1.plot(array[0][closest_index1],array[1][closest_index1]-array[2][closest_index1],'.',color='r',label='w50',linewidth=0.001,alpha=0.5)
    ax1.plot(array[0][closest_index2],array[1][closest_index2]-array[2][closest_index2],'.',color='r',label='w50',linewidth=0.001,alpha=0.5)
    plt.show(block=False)

def save_results(id,rv,w50,step_size):
    with open('/users/jburke/ebhis_scripts/group_gal_results/rv_w50_results.csv','a') as f:
        writer = csv.writer(f)
        new_line = [id, str(rv), str(step_size*2),str(w50),str(step_size)]
        writer.writerow(new_line)


id = input('Group ID: ')

h0,h1,h2,h3,h4= make_arrays(id)

plot_all_spectra(h0,h1,h2,h3,h4)
level=input('hanning level: ')
list_arrays = [h0,h1,h2,h3,h4]



rv,fwhm,step_size = plot_single_spec(list_arrays[int(level)])
final_spec(list_arrays[int(level)],rv,fwhm)
save = input('Save: y/n ')
if save == 'y':
    save_results(id,rv,fwhm,step_size)
else:
    pass

plt.close()



