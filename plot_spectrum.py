import scipy as sp
import numpy as np
import matplotlib.pyplot as plt
import os
import copy


#define input galaxy details.
im_name='raw_image.im'
xbl= 45 #box around galaxy
ybl= 57
xtr= 57
ytr= 73
low_chan=60
high_chan= 85
dB = 'E' 
blc=[xbl,ybl, low_chan-20]
trc=[xtr,ytr,high_chan+20]

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

#plot spectrum
fig,ax=plt.subplots()
ax.plot(velo,sumspec)
ax.set_xlabel('velocity (km/s)')
ax.set_ylabel('Brightness temp (K)')

'''
#fit spectrum with 2 Gaussains
#define functions
gaussfunc = lambda A,x0,sigma, x: A*np.exp(-((x-x0)**2)/(2.*sigma**2) )
fitfunc = lambda p, x: gaussfunc(p[0],p[1],p[2],x) + gaussfunc(p[3],p[4],p[5],x) +p[6]
errfunc = lambda p, x, y, err: (y - fitfunc(p, x)) / err
pinit = [60.,300.,20.,60.,350.,20.,-20.] # only x0 values were changed
yerr=np.ones(len(sumspec))

out = sp.optimize.leastsq(errfunc, pinit, args=(velo,sumspec,yerr),full_output=1) # this time use velo as x-array
pfinal = out[0]
covar = out[1]
#plot fittings
ax.plot(velo,fitfunc(pfinal,velo))
'''

fig.savefig('spectrum.png')
 