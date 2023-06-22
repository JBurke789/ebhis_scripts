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

gal= Galaxy('NGC5457','NGC5457.fits')
#gal.import_fits()
gal.gal_coords(550,780)
gal.mom0_map()
gal.gal_vals(4.038,1.369,37155.14,1036,1.36317)
'''
Threshold: 4.0558565217391305
total flux: 25744.74425271739 +- 1.0649765625 Jy km/s
Normalised total flux: 2979.7157699904387 +- 0.12326117621527778 Jy km/s
'''