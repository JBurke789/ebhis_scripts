import numpy as np
import os
import csv
import copy
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt


def make_regions(name,ra,dec):
  file1 = name+ '/spec_region1.crtf'
  with open(file1,'w') as file:
    lines = ['#CRTFv0 CASA Region Text Format version 0 \n','ellipse [[',ra,'deg,',dec,'deg], [2500arcsec, 2500arcsec], 0.00000000deg]']
    file.write(''.join(lines))
  file2 = name+ '/spec_region2.crtf'
  with open(file2,'w') as file:
    lines = ['#CRTFv0 CASA Region Text Format version 0 \n','annulus [[',ra,'deg,',dec,'deg], [3500arcsec, 4000arcsec]]']
    file.write(''.join(lines))

def extract_fluxes(name):
  ia.open(name+'/raw_image.im')
  flux = ia.getregion(name+'/spec_region1.crtf')
  ia.close()
  temp_in =np.sum(np.sum(flux,axis=0),axis=0) #collapse into 1D array
  ia.open(name+'/raw_image.im')
  flux = ia.getregion(name+'/spec_region2.crtf')
  ia.close()
  temp_ann =np.sum(np.sum(flux,axis=0),axis=0) #collapse into 1D array    
  #print(sumspec2)
  stats1 = imstat(imagename=name+'/raw_image.im',
                  region =name+'/spec_region1.crtf')
  stats2 = imstat(imagename=name+'/raw_image.im',
                  region =name+'/spec_region2.crtf')
  bg_temp_inner = (temp_ann/float(stats2['npts']))*float(stats1['npts'])          
  return temp_in,temp_ann,stats1,stats2,bg_temp_inner

def get_vel(name,temp_in):
  ia.open(name+'/raw_image.im')
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

def save_npy(name,velo,flux_inner,bg_flux_inner):
  output = np.stack((velo,flux_inner,bg_flux_inner),axis=0)
  np.save(name+'/spectrum.npy',output)

with open('/users/jburke/ebhis_scripts/workflow_results/final_results.csv','r') as f:
   reader = csv.reader(f)
   header = next(reader)
   for row in reader:
      name = row[0]
      ra = row[1]
      dec = row[2]
      dist = row[3]
      radvel = row[4]
      mag21 = row[5]
      w50 = row[6]

      make_regions(name,ra,dec)
      temp_in,temp_ann,stats1,stats2,bg_temp_inner=extract_fluxes(name)
      vel = get_vel(name,temp_in)
      flux_in =unit_conversion(temp_in)
      flux_ann=unit_conversion(temp_ann)
      bg_flux_inner=unit_conversion(bg_temp_inner)
      save_npy(name,vel,flux_in,bg_flux_inner)
