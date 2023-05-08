import numpy as np
import os
import matplotlib.pyplot as plt

#define input galaxy details.
im_name='column_density_map'
xbl= 45 #box around galaxy
ybl= 28
xtr= 58
ytr= 40
dB = 'E' 

#find standard deviation of background
if dB=='G':
    xbls=[xbl-100, xbl-100, xtr+50 , xtr+50]#define coords for 4 boxes around galaxy
    ybls=[ybl-100, ytr+50 , ytr+50 , ybl-100]
    xtrs=[xbl-50 , xbl-50 , xtr+100, xtr+100]
    ytrs=[ybl-50 , ytr+100, ytr+100, ybl-50]
elif dB=='E':
    xbls=[xbl-20, xbl-20, xtr   , xtr   ]#define coords for 4 boxes around galaxy
    ybls=[ybl-20, ytr   , ytr   , ybl-20]
    xtrs=[xbl   , xbl   , xtr+20, xtr+20]
    ytrs=[ybl   , ytr+20, ytr+20, ybl   ]  
stdevs=[]
for i in range(4):#calc stdev in each of the boxes
    coord = str(xbls[i]) + ',' + str(ybls[i]) + ',' + str(xtrs[i]) + ',' + str(ytrs[i])
    stats=imstat(imagename= im_name,
                 box=coord)
    stdevs.append(stats['sigma'][0])
mn_stdev = np.mean(np.array(stdevs))#calc mean stdev 

#extract values from moment zero map
blc= [xbl,ybl,0]
trc= [xtr,ytr,0]
ia.open(im_name)
flux = ia.getchunk(blc,trc)
ia.close()

mask=np.where(flux > mn_stdev*3,1,0)#create mask of pixels above 3 sigma
pix = np.sum(mask)#count number of pixels above 3 sigma
print('Number of pixels above threshold = '+ str(pix))

#set pixel to anglular resolution for local volume or further out.
if dB == 'E':
    pix_area=0.05427333333333333**2
elif dB == 'G':
    pix_area=0.01666666666666667**2

area= pix*pix_area#calculate area of galaxy above 3 sigma
print('area of galaxy above 3 sigma: '+ str(area)+' degrees squared')

#calculate beam size as fraction of galaxy size
beam=(9.4/120)**2 *np.pi
covered= beam/area
print('Beam covers '+str(covered)+' of the galaxy')
