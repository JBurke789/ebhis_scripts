import csv
import numpy as np
import os


low_chan= input('Low Channel: ')
high_chan=input('High Channel: ')
#function to make moment 0 map, given the frame numbers of the galaxy
def mom0_map(low_vel,high_vel):
    #assign channels of galaxy
    channels=str(low_vel)+'~'+str(high_vel)
    #create moment 0 map with no filter
    raw_im ='raw_image.im' 
    out = 'moment0.im'
    immoments(imagename=raw_im,
              moments=[0],
              chans=channels,
              outfile=out)
    
mom0_map(low_chan,high_chan)