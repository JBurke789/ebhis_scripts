import numpy as np
import csv
import os
import copy
"""
Run in casa and in directory of group
source /vol/software/software/astro/casa/initcasa.sh
"""
group='group'+input('group ID: ')
print(group)

def extract_spectra(image):
    ia.open(image)
    ON_flux = ia.getregion('spectrum_ON.crtf')
    OFF_flux = ia.getregion('spectrum_OFF.crtf')
    ia.close()
    ON_temp = np.sum(np.sum(ON_flux,axis=0),axis=0)
    OFF_temp = np.sum(np.sum(OFF_flux,axis=0),axis=0)
    statsON = imstat(imagename='raw_image.im',
                    region ='spectrum_ON.crtf')
    statsOFF = imstat(imagename='raw_image.im',
                    region ='spectrum_OFF.crtf')
    
    OFF_temp_norm = (OFF_temp/float(statsOFF['npts']))*float(statsON['npts'])
    return ON_temp, OFF_temp_norm


def get_vel(temp_in,image):
  ia.open(image)
  csys=ia.coordsys()
  x=np.array(np.arange(0,len(temp_in),1.)) #need floating point array
  freqs = copy.deepcopy(x)
  velo=copy.deepcopy(x)
  blctemp=[0,0,0]
  for a in range(0,len(x)):
    blctemp[2]=x[a]
    w=ia.toworld(blctemp,'n')
    freq=w['numeric'][2] # gives frequencies
    v=csys.frequencytovelocity(value=freq,doppler='radio',velunit='km/s')
    velo[a]=float(v)
  return velo

def unit_conversion(temp):
  flux_jy = temp/1.28
  flux_BA = flux_jy/8.64
  return flux_BA

def save_npy( vel,flux_ON,flux_OFF,filename):
   output = np.stack((vel,flux_ON,flux_OFF),axis=0)
   np.save(filename,output)

image = ['raw_image.im','hanning_smoothed1.im','hanning_smoothed3.im','hanning_smoothed3.im','hanning_smoothed4.im']
num=0
for i in image:
   ON_temp, OFF_temp_norm=extract_spectra(i)
   vel=get_vel(ON_temp,i)
   flux_ON = unit_conversion(ON_temp)
   flux_OFF = unit_conversion(OFF_temp_norm)
   file = group+'_spectrum_h'+str(num)+'.npy'
   save_npy(vel,flux_ON,flux_OFF,file)
   print('hanning level ' + str(num) + 'saved.')
   num += 1