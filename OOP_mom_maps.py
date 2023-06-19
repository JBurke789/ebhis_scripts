import os
import numpy as np

class galaxy:
    def __init__(self,name,path):
        self.name=name #galaxy name
        self.path=path #path to galaxy fits file

    def import_fits(self):
        importfits(fitsimage=self.path,
                   imagename='raw_image.im')
        
    def gal_coords(self,blc,trc,low_vel,high_vel):
        setattr(self,'box_coords',[blc,trc])
        setattr(self,'vel_coords',[low_vel,high_vel])

    def mom0_map(self)
        #remove existing files so can run again from scratch
        os.system('rm -rf hanningsmoothed*')
        os.system('rm -rf column_density_map*')
        os.system('rm -rf moment_map*')
        os.system('rm -rf no_filter_mom*')
        #create moment 0 map with no filter 
        immoments(imagename=im_name,
                  moments=[0],
                  #box=box_coords,
                  chans=channels,
                  outfile='no_filter_moment0')