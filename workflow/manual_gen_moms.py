import csv
import numpy as np
import os
#function to make moment 0 map, given the frame numbers of the galaxy
def mom0_map(name,low_vel,high_vel):
    #assign channels of galaxy
    channels=str(low_vel)+'~'+str(high_vel)
    #remove existing files so can run again from scratch
    os.system('rm -rf '+name+'/no_filter_mom*')
    #create moment 0 map with no filter
    raw_im = name+'/raw_image.im' 
    out = name+'/no_filter_moment0'
    immoments(imagename=raw_im,
              moments=[0],
              chans=channels,
              outfile=out)
#creates empty csv to store galaxies that cant make moment 0 map
with open('/users/jburke/ebhis_scripts/workflow_results/cant_make_m0map.csv','w') as f:
    pass

with open('/users/jburke/ebhis_scripts/workflow_results/no_linewidth.csv','r') as f:
    reader = csv.reader(f)
    for row in reader:#looks at each galaxy
        raw_im_path = row[0]+'/raw_image.im'
        imview(raw_im_path)
        cont = input('Can a Mom 0 map be generated?: (y/n)')
        if cont == 'n':
            #add to cant make mom0 list
            with open('/users/jburke/ebhis_scripts/workflow_results/cant_make_m0map.csv','a') as file:
                write= csv.writer(file)
                write.writerow(row)
        else :
            low_chan = int(input('Galaxy low channel number:'))
            high_chan = int(input('Galaxy high channel number:'))
            mom0_map(row[0],low_chan,high_chan)
            #adds to csv list of galaxies with mom0 maps
            with open('/users/jburke/ebhis_scripts/workflow_results/gals_with_m0maps.csv','a')as file:
                write= csv.writer(file)
                write.writerow(row)