import matplotlib
matplotlib.use('tkagg')
import matplotlib.pyplot as plt
import numpy as np
import scipy as sp
import os
import copy
'''
extract galaxy spectrum
'''
#define input galaxy details.
im_name='raw_image.im'
xbl= 110 #box around galaxy
ybl= 110    
xtr= 180
ytr= 180
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

'''
background spectrum
'''
xbl= 50 #box around galaxy
ybl= 200
xtr= 120
ytr= 270
blc=[xbl,ybl, 50]
trc=[xtr,ytr,233]

#extract spectrum from datacube
ia.open(im_name)
flux = ia.getchunk(blc,trc)
ia.close()
bg_sumspec =np.sum(np.sum(flux,axis=0),axis=0) #collapse into 1D array

#save spectrum to numpy file [velocity,flux/Beam Area]
output = np.stack((velo,sumspec,bg_sumspec),axis=0)
np.save('multi_spectrum.npy',output)