import numpy as np
import os
import csv
import copy

#make regions for source
def make_regions(ra,dec):
  file1 = 'ann_spec_region1.crtf'
  with open(file1,'w') as file:
    lines = ['#CRTFv0 CASA Region Text Format version 0 \n','ellipse [[',ra,'deg,',dec,'deg], [1600arcsec, 1600arcsec], 0.00000000deg]']
    file.write(''.join(lines))
  file2 = 'ann_spec_region2.crtf'
  with open(file2,'w') as file:
    lines = ['#CRTFv0 CASA Region Text Format version 0 \n','annulus [[',ra,'deg,',dec,'deg], [1600arcsec, 3500arcsec]]']
    file.write(''.join(lines))


def extract_fluxes():
  ia.open('raw_image.im')
  flux = ia.getregion('ann_spec_region1.crtf')
  ia.close()
  temp_in =np.sum(np.sum(flux,axis=0),axis=0) #collapse into 1D array
  ia.open('raw_image.im')
  flux = ia.getregion('ann_spec_region2.crtf')
  ia.close()
  temp_ann =np.sum(np.sum(flux,axis=0),axis=0) #collapse into 1D array    
  #print(sumspec2)
  stats1 = imstat(imagename='raw_image.im',
                  region ='ann_spec_region1.crtf')
  stats2 = imstat(imagename='raw_image.im',
                  region ='ann_spec_region2.crtf')
  bg_temp_inner = (temp_ann*float(stats1['npts']))/float(stats2['npts'])
  return temp_in,temp_ann,stats1,stats2,bg_temp_inner

def get_vel(temp_in):
  ia.open('raw_image.im')
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
  np.save('spectrum.npy',output)

def save_csv(velo,flux_inner,bg_flux_inner):
  headers = ['velocity','galaxy flux','normalised bg']
  data = list(zip(velo,flux_inner,bg_flux_inner))
  with open('spectrum_NGC2403.csv','w') as f:
    csv_writer=csv.writer(f)
    csv_writer.writerow(headers)
    csv_writer.writerows(data)


name = input('Galaxy Name:')

with open('/users/jburke/Desktop/full_gal_list.csv','r') as f:
   reader = csv.reader(f)
   header = next(reader)
   for row in reader:
    if name == row[0]:
      ra = row[1]
      dec = row[2]

make_regions(ra,dec)
temp_in,temp_ann,stats1,stats2,bg_temp_inner=extract_fluxes()
vel = get_vel(temp_in)
flux_in =unit_conversion(temp_in)
flux_ann=unit_conversion(temp_ann)
bg_flux_inner=unit_conversion(bg_temp_inner)
save_npy(vel,flux_in,bg_flux_inner)
#save_csv(vel,flux_in,bg_flux_inner)
