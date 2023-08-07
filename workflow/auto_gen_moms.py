import csv
import numpy as np
import os


class galaxy:
    def __init__(self,name,rad_vel,width):
        self.name=name #galaxy name
        self.rad_vel = float(rad_vel)
        self.width = float(width)

    def mom0_map(self):#for galaxies with known w50
        #find limits and channels
        low_lim  =self.rad_vel-self.width-10
        high_lim =self.rad_vel+self.width+10
        vels = np.linspace(-606.648,609.427,945)
        l_ind = np.argmin(np.abs(np.array(vels)-low_lim))
        h_ind = np.argmin(np.abs(np.array(vels)-high_lim))
        channels= str(l_ind)+'~'+str(h_ind)
        #remove existing files so can run again from scratch
        os.system('rm -rf '+self.name+'/moment_map*')
        os.system('rm -rf '+self.name+'/no_filter_mom*')
        #create moment 0 map with no filter
        raw_im = self.name+'/raw_image.im' 
        out = self.name+'/no_filter_moment0'
        immoments(imagename=raw_im,
                  moments=[0],
                  chans=channels,
                  outfile=out)
        

    def big_mom0_map(self):#for galaxies with no w50 and positive radial vel
        channels = '510~944' #channels for all velocities above MW
        #remove existing files so can run again from scratch
        os.system('rm -rf '+self.name+'/moment_map*')
        os.system('rm -rf '+self.name+'/no_filter_mom*')
        #create moment 0 map with no filter
        raw_im = self.name+'/raw_image.im' 
        out = self.name+'/no_filter_moment0'
        immoments(imagename=raw_im,
                  moments=[0],
                  chans=channels,
                  outfile=out)


#makes empty csv file for galaxies with maps
with open('/users/jburke/Desktop/test_gal_list.csv','r') as f:
    reader = csv.reader(f)
    header = next(reader)
    with open('/users/jburke/ebhis_scripts/workflow_results/gals_with_m0maps.csv','w') as empty_csv:
        csv_writer = csv.writer(empty_csv)
        csv_writer.writerow(header)
#goes through csv of galaxies ready to make m0 maps

with open('/users/jburke/ebhis_scripts/workflow_results/auto_analyse.csv','r') as f:
    reader = csv.reader(f)
    for row in reader:
        obj = galaxy(row[0],row[4],row[6])
        obj.mom0_map()
        #adds to csv list of galaxies with mom0 maps
        with open('/users/jburke/ebhis_scripts/workflow_results/gals_with_m0maps.csv','a')as file:
            write= csv.writer(file)
            write.writerow(row)

with open('/users/jburke/ebhis_scripts/workflow_results/no_linewidth.csv','r') as f:
    reader = csv.reader(f)
    header = next(reader)
    for row in reader:
        if row[4]>=50:
            obj = galaxy(row[0],row[4],row[6])
            obj.big_mom0_map()
            with open('/users/jburke/ebhis_scripts/workflow_results/gals_with_m0maps.csv','a')as file:
                write= csv.writer(file)
                write.writerow(row)

