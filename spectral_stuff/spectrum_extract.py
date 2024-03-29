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
    lines = ['#CRTFv0 CASA Region Text Format version 0 \n','ellipse [[',ra,'deg,',dec,'deg], [2000arcsec, 2000arcsec], 0.00000000deg]']
    file.write(''.join(lines))
  file2 = name+ '/spec_region2.crtf'
  with open(file2,'w') as file:
    lines = ['#CRTFv0 CASA Region Text Format version 0 \n','annulus [[',ra,'deg,',dec,'deg], [3500arcsec, 4500arcsec]]']
    file.write(''.join(lines))
  file3 = name+ '/spec_region3.crtf'
  with open(file3,'w') as file:
    lines = ['#CRTFv0 CASA Region Text Format version 0 \n','annulus [[',ra,'deg,',dec,'deg], [6500arcsec, 7500arcsec]]']
    file.write(''.join(lines))

def extract_fluxes(name):
  ia.open(name+'/raw_image.im')
  flux = ia.getregion(name+'/spec_region1.crtf')
  ia.close()
  temp_in =np.sum(np.sum(flux,axis=0),axis=0) #collapse into 1D array
  ia.open(name+'/raw_image.im')
  flux = ia.getregion(name+'/spec_region2.crtf')
  ia.close()
  temp_ann1 =np.sum(np.sum(flux,axis=0),axis=0) #collapse into 1D array
  ia.open(name+'/raw_image.im')
  flux = ia.getregion(name+'/spec_region3.crtf')
  ia.close()
  temp_ann2 =np.sum(np.sum(flux,axis=0),axis=0)     
  #print(sumspec2)
  stats1 = imstat(imagename=name+'/raw_image.im',
                  region =name+'/spec_region1.crtf')
  stats2 = imstat(imagename=name+'/raw_image.im',
                  region =name+'/spec_region2.crtf')
  stats3 = imstat(imagename=name+'/raw_image.im',
                  region =name+'/spec_region3.crtf')
  ann1_temp_norm = (temp_ann1/float(stats2['npts']))*float(stats1['npts'])
  ann2_temp_norm = (temp_ann2/float(stats3['npts']))*float(stats1['npts'])          
  return temp_in,temp_ann1,temp_ann2,stats1,stats2,stats3,ann1_temp_norm,ann2_temp_norm

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

def save_npy(name,velo,flux_inner,ann1_flux_norm,ann2_flux_norm):
  output = np.stack((velo,flux_inner,ann1_flux_norm,ann2_flux_norm),axis=0)
  np.save(name+'/spectrum.npy',output)




with open('/users/jburke/ebhis_scripts/workflow_results/MW_overlap.csv','r') as f:
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
      temp_in,temp_ann1,temp_ann2,stats1,stats2,stats3,ann1_temp_norm,ann2_temp_norm=extract_fluxes(name)
      vel = get_vel(name,temp_in)
      flux_in =unit_conversion(temp_in)
      flux_ann1=unit_conversion(temp_ann1)
      flux_ann2=unit_conversion(temp_ann2)
      ann1_flux_norm=unit_conversion(ann1_temp_norm)
      ann2_flux_norm=unit_conversion(ann2_temp_norm)
      save_npy(name,vel,flux_in,ann1_flux_norm,ann2_flux_norm)
      print(name,'spectrum saved')

      










"""
with open('/users/jburke/Desktop/full_gal_list.csv','r') as f:
    reader = csv.reader(f)
    header = next(reader)
    for row in reader:
        if row[0] == galaxy:
            ra = row[1]
            dec = row[2]
            dist = row[3]
            radvel = row[4]
            mag21 = row[5]
            w50 = row[6]




ia.open(galaxy+'/raw_image.im')
flux = ia.getregion(file1)
ia.close()
sumspec1 =np.sum(np.sum(flux,axis=0),axis=0) #collapse into 1D array
ia.open(galaxy+'/raw_image.im')
flux = ia.getregion(file2)
ia.close()
sumspec2 =np.sum(np.sum(flux,axis=0),axis=0) #collapse into 1D array
#print(sumspec2)
stats1 = imstat(imagename=galaxy+'/raw_image.im',
                region =galaxy+'/spec_region1.crtf')
print(stats1['npts'])
stats2 = imstat(imagename=galaxy+'/raw_image.im',
                region =galaxy+'/spec_region2.crtf')
print(stats2['npts'])

bg_spec= sumspec2-sumspec1
norm_bg = bg_spec*(float(stats1['npts'])/(float(stats2['npts']-float(stats1['npts']))))



ia.open(galaxy+'/raw_image.im')
csys=ia.coordsys()
x=np.array(np.arange(0,len(sumspec1),1.)) # need floating point array
freqs = copy.deepcopy(x)
velo=copy.deepcopy(x)
blctemp=[0,0,0]
for a in range(0,len(x)):
  blctemp[2]=x[a]
  w=ia.toworld(blctemp,'n')
  freq=w['numeric'][2] # gives frequencies
  v=csys.frequencytovelocity(value=freq,doppler='radio',velunit='km/s')
  velo[a]=float(v)
#print(velo)

output = np.stack((velo,sumspec1,norm_bg),axis=0)
np.save(galaxy+'/spectrum.npy',output)
"""
"""
fig1,ax1 = plt.subplots()
ax1.plot(velo,sumspec)
ax1.set_xlabel('Velocity [km/s]')
ax1.set_ylabel('Temp [k]')
fig1.savefig('NGC6946/spec.png')
"""
'''

#extract velocities for x axis
ia.open('NGC6946/raw_image.im')
csys=ia.coordsys()
x=np.array(np.arange(0,len(sumspec),1.)) # need floating point array
freqs = copy.deepcopy(x)
velo=copy.deepcopy(x)
blctemp=copy.deepcopy(blc)
for a in range(0,len(x)):
  blctemp[2]=x[a]+blc[2]
  w=ia.toworld(blctemp,'n')
  freq=w['numeric'][2] # gives frequencies
  v=csys.frequencytovelocity(value=freq,doppler='radio',velunit='km/s')
  velo[a]=float(v)
'''