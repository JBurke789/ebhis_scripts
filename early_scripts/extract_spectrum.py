import scipy as sp
import numpy as np
import os
import copy


#define input galaxy details.
im_name='raw_image.im'
xbl= 110 #box around galaxy
ybl= 140
xtr= 180
ytr= 185

low_chan=60
high_chan= 106
#dB = 'G' 
blc=[xbl,ybl, 50]
trc=[xtr,ytr,233]

#extract spectrum from datacube
ia.open(im_name)
flux = ia.getchunk(blc,trc)
ia.close()
sumspec =np.sum(np.sum(flux,axis=0),axis=0) #collapse into 1D array

#extract velocities for x axis
ia.open(im_name)
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

#save spectrum to numpy file [velocity,flux/Beam Area]
output = np.stack((velo,sumspec),axis=0)
np.save('spectrum.npy',output)