import numpy as np
import os
import csv
import copy

'''
gets the spectra for a galaxy with manually defined regions.

Run in directory of galaxy
'''

def extract_spectra(image):
    ia.open(image)#ON spectrum
    flux = ia.getregion('man_spectrum_ON.crtf')
    ia.close()
    temp_ON =np.sum(np.sum(flux,axis=0),axis=0)
    ia.open(image)#OFF spectra
    flux = ia.getregion('man_spectrum_OFF.crtf')
    ia.close()
    temp_OFF =np.sum(np.sum(flux,axis=0),axis=0)

    statsON = imstat(imagename=image,
                    region ='man_spectrum_ON.crtf')
    statsOFF = imstat(imagename=image,
                    region ='man_spectrum_OFF.crtf')

    temp_OFF_norm= (temp_OFF/float(statsOFF['npts']))*float(statsON['npts']) #background temp scales to same pixels as ON spectrum

    return temp_ON, temp_OFF_norm

def get_hanning_spectra():
    print('getting Hanning spectra')
    nums = ['1','2','3','4']
    for i in nums:
        temp_ON, temp_OFF_norm = extract_spectra('hanning_smoothed'+i+'.im')
        image = 'hanning_smoothed'+i+'.im'
        vel = get_vel(temp_ON,image)
        flux_ON = unit_conversion(temp_ON)
        flux_OFF= unit_conversion(temp_OFF_norm)
        #save_npy(vel,flux_ON,flux_OFF)
        output = np.stack((vel,flux_ON,flux_OFF),axis=0)
        np.save('man_hanning_spectrum'+i+'.npy',output)
    print('Hanning spectra saved')


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

def save_npy(velo,flux_inner,bg_flux_inner):
  output = np.stack((velo,flux_inner,bg_flux_inner),axis=0)
  np.save('man_spectrum.npy',output)


#get full spectrum
temp_ON, temp_OFF = extract_spectra('raw_image.im')
vel = get_vel(temp_ON,'raw_image.im')
flux_ON = unit_conversion(temp_ON)
flux_OFF = unit_conversion(temp_OFF)
save_npy(vel,flux_ON,flux_OFF)
get_hanning_spectra()
