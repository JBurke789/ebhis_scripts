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

    def thresh(self,max,rms):
        self.rms = rms
        threshold= max + 3.*(rms/(float(self.vel_coords[1])-float(self.vel_coords[0])))
        setattr(self,'thresh',threshold)
        print('Threshold: '+ str(threshold))

    def gal_vals(self,sum,npix):
        #calculate values
        threshold= self.thresh
        total = sum - threshold*npix#K km/s
        tot_flux = total /1.28
        norm_tot_flux = tot_flux/8.64 #8.64pix/b.a
        #uncertainty
        rms = self.rms #rms is the uncertainty per pixel
        uncert = rms*npix
        frac_uncert = uncert/total
        #set attributes to object
        setattr(self,'total_flux',tot_flux)
        setattr(self,'normalised_tot_flux',norm_tot_flux)
        setattr(self,'uncertainty',frac_uncert)
        #print important values to command line
        #print('Threshold: '+ str(threshold))
        print('total flux: ' + str(tot_flux)+ ' +- ' +str(frac_uncert*tot_flux) +' Jy km/s')
        print('Normalised total flux: ' +str(norm_tot_flux)+ ' +- ' +str(frac_uncert*norm_tot_flux) +' Jy km/s')

gal= Galaxy('NGC628','NGC628.fits')
#gal.import_fits()
gal.gal_coords(60,90)
gal.mom0_map()
gal.thresh(5.649662,2.639534)
gal.gal_vals(9357.889,600)

'''
Threshold: 5.9136154
total flux: 4538.843562499999 +- 50.511808271308226 Jy km/s
Normalised total flux: 525.3291160300925 +- 5.846274105475488 Jy km/s
'''