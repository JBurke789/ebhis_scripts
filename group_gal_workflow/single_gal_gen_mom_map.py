import csv
import numpy as np
import os

gal_name = input('Galaxy name: ')
low_lim = float(input('Low velocity: '))
high_lim= float(input('High velocity: '))
vels = np.linspace(-606.648,609.427,945)
l_ind = np.argmin(np.abs(np.array(vels)-low_lim))
h_ind = np.argmin(np.abs(np.array(vels)-high_lim))
channels= str(l_ind)+'~'+str(h_ind)


immoments(imagename='raw_image.im',
          moments=[0],
          chans=channels,
          outfile=gal_name+'_moment0.im')

print('Moment 0 map created.')