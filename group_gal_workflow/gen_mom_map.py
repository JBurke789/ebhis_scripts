import csv
import numpy as np
import os
"""
imports fits to CASA format. Calculates the velocity range to make moment maps in and makes it if it can.
Needs to be run in CASA

source /vol/software/software/astro/casa/initcasa.sh
"""

importfits(fitsimage='data_cube.fits',
           imagename='raw_image.im' )


gal_info = np.load('group_info.npy')

min_vels=[]
max_vels=[]
for i in gal_info:
    rad_vel= float(i[4])
    if i[6]=='':
        w50=0
    else:
        w50=float(i[6])
    min_vels.append(rad_vel-w50/2.0)
    max_vels.append(rad_vel+w50/2.0)

low_lim  =min(min_vels)-10
high_lim =max(max_vels)+10
vels = np.linspace(-606.648,609.427,945)
l_ind = np.argmin(np.abs(np.array(vels)-low_lim))
h_ind = np.argmin(np.abs(np.array(vels)-high_lim))
channels= str(l_ind)+'~'+str(h_ind)


if high_lim<=609.425 and low_lim>=50:
    print(str(low_lim)+'km/s -> '+str(high_lim)+'km/s')
    immoments(imagename='raw_image.im',
              moments=[0],
              chans=channels,
              outfile='moment0.im')
    print('Moment 0 map created.')
elif low_lim>=-606.648 and high_lim<=-50:
    print(str(low_lim)+'km/s -> '+str(high_lim)+'km/s')
    immoments(imagename='raw_image.im',
              moments=[0],
              chans=channels,
              outfile='moment0.im')
    print('Moment 0 map created.')
else:
    print(str(low_lim)+'km/s -> '+str(high_lim)+'km/s')
    imview('raw_image.im')
    valid = input('Can moment map be generated? (y/n): ')
    if valid =='y':
        low_chan= input('Low Channel: ')
        high_chan=input('High Channel: ')
        channels=str(low_chan)+'~'+str(high_chan)
        immoments(imagename='raw_image.im',
                  moments=[0],
                  chans=channels,
                  outfile='moment0.im')

