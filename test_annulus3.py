import numpy as np
import os

class Gal:
    def __init__(self,name,ra,dec):
        self.name=name
        self.ra = ra
        self.dec = dec

    def make_region_files(self):
        with open('region1.crtf','w') as file:
            lines = ['#CRTFv0 CASA Region Text Format version 0 \n','ellipse [[',self.ra,'deg,',self.dec,'deg], [1600arcsec, 1600arcsec], 0.00000000deg]']
            file.write(''.join(lines))
        with open('region2.crtf','w') as file:
            lines = ['#CRTFv0 CASA Region Text Format version 0 \n','ellipse [[',self.ra,'deg,',self.dec,'deg], [2000arcsec, 2000arcsec], 0.00000000deg]']
            file.write(''.join(lines))
        with open('region3.crtf','w') as file:
            lines = ['#CRTFv0 CASA Region Text Format version 0 \n','ellipse [[',self.ra,'deg,',self.dec,'deg], [2500arcsec, 2500arcsec], 0.00000000deg]']
            file.write(''.join(lines))
            print('region files created for ', self.name)

    def extract_annuli_vals(self):
        self.make_region_files()
        #run imstat on each circle and get values
        stats1 = imstat(imagename='no_filter_moment0',
                region = 'region1.crtf')
        sum1 = stats1['sum']
        rms1 = stats1['rms']
        npix1 = stats1['npts']
        print('reg1:',sum1,rms1,npix1)
        stats2 = imstat(imagename='no_filter_moment0',
                region = 'region2.crtf')
        sum2 = stats2['sum']
        rms2 = stats2['rms']
        npix2 = stats2['npts']
        print('reg2:',sum2,rms2,npix2)
        stats3 = imstat(imagename='no_filter_moment0',
                region = 'region3.crtf')
        sum3 = stats3['sum']
        rms3 = stats3['rms']
        npix3 = stats3['npts']
        print('reg3:',sum3,rms3,npix3)
        print('...')
        #calculate noise per pixel in each annuli
        sum_ann1 = (sum2-sum1)/(npix2-npix1)
        sum_ann2 = (sum3-sum2)/(npix3-npix2)
        print('background ann1:',sum_ann1)
        print('background ann2:',sum_ann2)
        #calculate rms of annuli
        rms_ann1 = np.sqrt((npix2/(npix2-npix1))*(rms2**2 - (npix1/(npix2))*rms1**2))
        rms_ann2 = np.sqrt((npix3/(npix3-npix2))*(rms3**2 - (npix2/(npix3))*rms2**2))
        print('rms ann1:',rms_ann1)
        print('rms ann2:',rms_ann2)
        #check if annuli have same vals
        ann_diff = abs(sum_ann1-sum_ann2)/sum_ann2
        if ann_diff<= 0.05:
            print('Annuli have similar values => proceed ')
            self.annulus_calc(sum1,npix1,sum2,npix2,rms_ann1)
        else:
            print('Large variation between annuli=> DO BY HAND')

    def annulus_calc(self,inner_sum,inner_npix,outer_sum,outer_npix,rms):
        bg_flux = outer_sum-inner_sum
        bg_npix = outer_npix-inner_npix
        bg_per_pix = bg_flux/bg_npix
        clean_flux = inner_sum - bg_per_pix*inner_npix
        flux_jy = clean_flux/1.28
        norm_flux_jy = flux_jy/8.64

        bg_rms = rms
        uncert = bg_rms*np.sqrt(inner_npix)
        frac_uncert = uncert/clean_flux
        print('Flux = '+ str(flux_jy)+' p/m '+ str(uncert))
        print('norm flux = '+ str(norm_flux_jy)+' p/m '+ str(frac_uncert*norm_flux_jy))
        print('rms of background: '+ str(bg_rms))








x= Gal('NGC7640','350.5275','40.8456')
x.extract_annuli_vals()

