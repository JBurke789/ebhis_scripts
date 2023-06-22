import os
import numpy as np
import copy
import scipy as sp

class Galaxy:
    def __init__(self,name,path):
        self.name=name #galaxy name
        self.path=path #path to galaxy fits file

    def import_fits(self):
        importfits(fitsimage=self.path,
                   imagename='raw_image.im')
        
    def gal_coords(self,low_vel,high_vel):
        channels=str(low_vel)+'~'+str(high_vel)
        coords=[low_vel,high_vel]
        setattr(self,'vel_coords',coords)
        setattr(self,'vel_channels',channels)

    def mom0_map(self):
        #remove existing files so can run again from scratch
        os.system('rm -rf hanningsmoothed*')
        os.system('rm -rf column_density_map*')
        os.system('rm -rf moment_map*')
        os.system('rm -rf no_filter_mom*')
        #create moment 0 map with no filter 
        immoments(imagename='raw_image.im',
                  moments=[0],
                  #box=box_coords,
                  chans=self.vel_channels,
                  outfile='no_filter_moment0')
        
    def gal_vals(self,max,rms,sum,npix,stan_dev):
        #calculate values
        threshold= max + 3.*(rms/(float(self.vel_coords[1])-float(self.vel_coords[0])))
        total = sum - threshold*npix#K km/s
        tot_flux = total /1.28
        norm_tot_flux = tot_flux/8.64 #8.64pix/b.a
        var=stan_dev/total #variance as a fraction of peak
        uncert= norm_tot_flux*var
        #set attributes to object
        setattr(self,'thresh',threshold)
        setattr(self,'total_flux',tot_flux)
        setattr(self,'normalised_tot_flux',norm_tot_flux)
        setattr(self,'uncertainty',uncert)
        #print important values to command line
        print('Threshold: '+ str(threshold))
        print('total flux: ' + str(tot_flux)+ ' +- ' +str(var*tot_flux) +' Jy km/s')
        print('Normalised total flux: ' +str(norm_tot_flux)+ ' +- ' +str(uncert) +' Jy km/s')

NGC4214= Galaxy('NGC4214','NGC4214.fits')
#NGC4214.import_fits()
NGC4214.gal_coords(620,790)
NGC4214.mom0_map()
NGC4214.gal_vals(4.740241,1.362451,6183.398,525,0.9933735)
"""
Threshold: 4.764284252941176
total flux: 2876.6787243795957 +- 0.776073046875 Jy km/s
Normalised total flux: 332.94892643282355 +- 0.0898232693142361 Jy km/s
"""