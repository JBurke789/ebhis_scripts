import os
import numpy as np
import copy
import scipy as sp

class Galaxy:
    def __init__(self,name,path):
        self.name=name #galaxy name
        self.path=path #path to galaxy fits file

    def import_fits(self):
        dir = 'raw_image.im'
        if os.path.isdir(dir):
            print('fits file already imported to CASA format.')
        else:
            importfits(fitsimage=self.path,
                        imagename='raw_image.im')
            print('fits file imported')
        
    def mom0_map(self,low_vel,high_vel):
        #assign channels of galaxy
        channels=str(low_vel)+'~'+str(high_vel)
        coords=[low_vel,high_vel]
        setattr(self,'vel_coords',coords)
        setattr(self,'vel_channels',channels)
        #remove existing files so can run again from scratch
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
        #rms = self.rms #rms is the uncertainty per pixel
        uncert = self.rms*np.sqrt(npix)
        frac_uncert = uncert/total
        #set attributes to object
        setattr(self,'total_flux',tot_flux)
        setattr(self,'normalised_tot_flux',norm_tot_flux)
        setattr(self,'uncertainty',frac_uncert)
        #print important values to command line
        #print('Threshold: '+ str(threshold))
        print('total flux: ' + str(tot_flux)+ ' +- ' +str(frac_uncert*tot_flux) +' Jy km/s')
        print('Normalised total flux: ' +str(norm_tot_flux)+ ' +- ' +str(frac_uncert*norm_tot_flux) +' Jy km/s')
