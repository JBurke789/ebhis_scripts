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
    
#looks for csv file to store gals that can't be analysed, makes one if not there
csvpath = '/users/jburke/ebhis_scripts/workflow_results/cant_make_m0map.csv'
if not os.path.exists(csvpath):
    with open('/users/jburke/Desktop/test_gal_list.csv','r') as f:
        reader = csv.reader(f)
        header = next(reader)
        with open('/users/jburke/ebhis_scripts/workflow_results/cant_make_m0map.csv','w') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(header)
else:
    pass

#makes a list of all galaxy names that have been analysed
galaxies_analysed =[]
with open('/users/jburke/ebhis_scripts/workflow_results/cant_make_m0map.csv','r') as csv_file:
    reader = csv.reader(csv_file)
    header = next(reader)
    for row in reader:
        name = row[0]
        galaxies_analysed.append(name)
with open('/users/jburke/ebhis_scripts/workflow_results/MW_overlap.csv','r') as csv_file:
    reader = csv.reader(csv_file)
    header = next(reader)
    for row in reader:
        name = row[0]
        galaxies_analysed.append(name)
with open('/users/jburke/ebhis_scripts/workflow_results/gals_with_m0maps.csv','r') as csv_file:
    reader = csv.reader(csv_file)
    header = next(reader)
    for row in reader:
        name = row[0]
        galaxies_analysed.append(name)


with open('/users/jburke/ebhis_scripts/workflow_results/no_linewidth.csv','r') as f:
    reader = csv.reader(f)
    header = next(reader)
    for row in reader:
        if row[0] in galaxies_analysed:#skip if already analysed
            print(str(row[0])+' already analysed')
        else:
            print('Radial vel-- ' + str(row[4]))
            raw_im_path = row[0]+'/raw_image.im'
            imview(raw_im_path)
            visible = input('Is galaxy visible?: (y/n)')
            if visible =='n':          #add to cant make mom0 list
                with open('/users/jburke/ebhis_scripts/workflow_results/cant_make_m0map.csv','a') as file:
                    write= csv.writer(file)
                    write.writerow(row)  
            elif visible =='y':
                MW_overlap = input('Is there MW overlap?: (y/n)')
                if MW_overlap == 'y':
                    #send to MW overlap csv
                    with open('/users/jburke/ebhis_scripts/workflow_results/MW_overlap.csv','a')as file:
                        write= csv.writer(file)
                        write.writerow(row)
                elif MW_overlap=='n':#generates m0 map
                    low_chan = int(input('Galaxy low channel number:'))
                    high_chan = int(input('Galaxy high channel number:'))
                    mom0_map(row[0],low_chan,high_chan)
                    #adds to csv list of galaxies with mom0 maps
                    with open('/users/jburke/ebhis_scripts/workflow_results/gals_with_m0maps.csv','a')as file:
                        write= csv.writer(file)
                        write.writerow(row)
