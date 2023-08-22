import numpy as np
import os
import csv
import copy
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt


with open('/users/jburke/Desktop/full_gal_list.csv','r') as f:
    reader = csv.reader(f)
    header = next(reader)
    for row in reader:
        if row[0] == 'NGC6946':
            ra = row[1]
            dec = row[2]
            dist = row[3]
            radvel = row[4]
            mag21 = row[5]
            w50 = row[6]


file1 = str('NGC6946')+ '/region1.crtf'
with open(file1,'w') as file:
    lines = ['#CRTFv0 CASA Region Text Format version 0 \n','ellipse [[',ra,'deg,',dec,'deg], [2500arcsec, 2500arcsec], 0.00000000deg]']
    file.write(''.join(lines))
file2 = str('NGC6946')+ '/region2.crtf'
with open(file2,'w') as file:
    lines = ['#CRTFv0 CASA Region Text Format version 0 \n','ellipse [[',ra,'deg,',dec,'deg], [3500arcsec, 3500arcsec], 0.00000000deg]']
    file.write(''.join(lines))

ia.open('NGC6946/raw_image.im')
flux = ia.getregion(file1)
ia.close()
sumspec1 =np.sum(np.sum(flux,axis=0),axis=0) #collapse into 1D array
ia.open('NGC6946/raw_image.im')
flux = ia.getregion(file2)
ia.close()
sumspec2 =np.sum(np.sum(flux,axis=0),axis=0) #collapse into 1D array
#print(sumspec2)
stats1 = imstat(imagename='NGC6946/raw_image.im',
                region ='NGC6946/region1.crtf')
print(stats1['npts'])
stats2 = imstat(imagename='NGC6946/raw_image.im',
                region ='NGC6946/region2.crtf')
print(stats2['npts'])

bg_spec= sumspec2-sumspec1
norm_bg = bg_spec*(float(stats1['npts'])/(float(stats2['npts']-float(stats1['npts']))))



ia.open('NGC6946/raw_image.im')
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
np.save('NGC6946/spectrum.npy',output)

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