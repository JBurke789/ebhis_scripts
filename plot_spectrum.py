import scipy as sp
import numpy as np
import matplotlib.pyplot as plt
import os
import copy


#define input galaxy details.
im_name='raw_image.im'
xbl= 115 #box around galaxy
ybl= 130
xtr= 150
ytr= 175
low_chan=83
high_chan= 106
dB = 'G' 
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



#set pixel to anglular resolution for local volume or further out.
if dB == 'E':
    pix_area=0.05427333333333333**2
elif dB == 'G':
    pix_area=0.01666666666666667**2

sens=1.55 #Sensitivity K/Jy
box_pix = (ytr-ybl)*(xtr-xbl)
beam=(9.4/120)**2 *np.pi#beam area degrees
flux_BA = (sumspec*beam)/(sens*box_pix*pix_area)#converts Kelvin per box area in pixels to Jy per beam area

#plot spectrum
fig,ax=plt.subplots()
ax.plot(velo,sumspec)
ax.set_xlabel('velocity (km/s)')
ax.set_ylabel('Brightness temp (K)')

#save spectrum to numpy file [velocity,flux/Beam Area]
output = np.stack((velo,flux_BA),axis=0)
np.save('spectrum.npy',output)
fig.savefig('spectrum.png',overwrite=True)
 