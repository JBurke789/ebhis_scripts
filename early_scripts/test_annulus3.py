import numpy as np
import os
import csv

class Gal:
    def __init__(self,name,ra,dec):
        self.name=name
        self.ra = ra
        self.dec = dec

    def make_region_files(self):#makes 5 region files of increasing radius
        file1 = str(self.name)+ '/region1.crtf'
        with open(file1,'w') as file:
            lines = ['#CRTFv0 CASA Region Text Format version 0 \n','ellipse [[',self.ra,'deg,',self.dec,'deg], [1600arcsec, 1600arcsec], 0.00000000deg]']
            file.write(''.join(lines))
        file2 = str(self.name)+ '/region2.crtf'
        with open(file2,'w') as file:
            lines = ['#CRTFv0 CASA Region Text Format version 0 \n','ellipse [[',self.ra,'deg,',self.dec,'deg], [2000arcsec, 2000arcsec], 0.00000000deg]']
            file.write(''.join(lines))
        file3 = str(self.name)+ '/region3.crtf'
        with open(file3,'w') as file:
            lines = ['#CRTFv0 CASA Region Text Format version 0 \n','ellipse [[',self.ra,'deg,',self.dec,'deg], [2500arcsec, 2500arcsec], 0.00000000deg]']
            file.write(''.join(lines))
        file4 = str(self.name)+ '/region4.crtf'
        with open(file4,'w') as file:
            lines = ['#CRTFv0 CASA Region Text Format version 0 \n','ellipse [[',self.ra,'deg,',self.dec,'deg], [3000arcsec, 3000arcsec], 0.00000000deg]']
            file.write(''.join(lines))
        file5 = str(self.name)+ '/region5.crtf'
        with open(file5,'w') as file:
            lines = ['#CRTFv0 CASA Region Text Format version 0 \n','ellipse [[',self.ra,'deg,',self.dec,'deg], [3500arcsec, 3500arcsec], 0.00000000deg]']
            file.write(''.join(lines))
        #print('region files created for ', self.name)


    def extract_annuli_vals(self):
        self.make_region_files()
        #run imstat on each circle and get values
        stats1 = imstat(imagename=str(self.name)+'/no_filter_moment0',
                region = str(self.name)+'/region1.crtf')
        sum1 = stats1['sum']
        rms1 = stats1['rms']
        npix1 = stats1['npts']
        stats2 = imstat(imagename=str(self.name)+'/no_filter_moment0',
                region = str(self.name)+'/region2.crtf')
        sum2 = stats2['sum']
        rms2 = stats2['rms']
        npix2 = stats2['npts']
        stats3 = imstat(imagename=str(self.name)+'/no_filter_moment0',
                region = str(self.name)+'/region3.crtf')
        sum3 = stats3['sum']
        rms3 = stats3['rms']
        npix3 = stats3['npts']
        stats4 = imstat(imagename=str(self.name)+'/no_filter_moment0',
                region = str(self.name)+'/region4.crtf')
        sum4 = stats4['sum']
        rms4 = stats4['rms']
        npix4 = stats4['npts']
        
        stats5 = imstat(imagename=str(self.name)+'/no_filter_moment0',
                region = str(self.name)+'/region5.crtf')
        sum5 = stats5['sum']
        rms5 = stats5['rms']
        npix5 = stats5['npts']
        print('...')
        #calculate noise per pixel in each annuli
        sum_ann1 = (sum2-sum1)/(npix2-npix1)
        sum_ann2 = (sum3-sum2)/(npix3-npix2)
        sum_ann3 = (sum4-sum3)/(npix4-npix3)
        sum_ann4 = (sum5-sum4)/(npix5-npix4)
        #print('background ann1:',sum_ann1)
        #print('background ann2:',sum_ann2)
        #print('background ann3:',sum_ann3)
        #print('background ann3:',sum_ann4)
        #calculate rms of annuli
        rms_ann1 = np.sqrt((npix2/(npix2-npix1))*(rms2**2 - (npix1/(npix2))*rms1**2))
        rms_ann2 = np.sqrt((npix3/(npix3-npix2))*(rms3**2 - (npix2/(npix3))*rms2**2))
        rms_ann3 = np.sqrt((npix4/(npix4-npix3))*(rms4**2 - (npix3/(npix4))*rms3**2))
        rms_ann4 = np.sqrt((npix5/(npix5-npix4))*(rms5**2 - (npix4/(npix5))*rms4**2))
        #print('rms ann1:',rms_ann1)
        #print('rms ann2:',rms_ann2)
        #print('rms ann3:',rms_ann3)
        #print('rms ann4:',rms_ann4)
        #check if annuli have same vals
        ann_diff1 = abs(sum_ann1-sum_ann2)/sum_ann2
        ann_diff2 = abs(sum_ann2-sum_ann3)/sum_ann3
        ann_diff3 = abs(sum_ann3-sum_ann4)/sum_ann4
        if ann_diff1<= 0.1:
            print('First annuli have similar values => proceed ')
            self.annulus_calc(sum1,npix1,sum2,npix2,rms_ann1)
        elif ann_diff1>= 0.1 and ann_diff2<= 0.1:
            print('Second annuli have similar values => proceed ')
            self.annulus_calc(sum2,npix2,sum3,npix3,rms_ann2)
        elif ann_diff2>= 0.1 and ann_diff3<= 0.1:
            print('Second annuli have similar values => proceed ')
            self.annulus_calc(sum3,npix3,sum4,npix4,rms_ann3)
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
        norm_uncert = frac_uncert*norm_flux_jy
        print('Flux = '+ str(flux_jy)+' p/m '+ str(uncert))
        print('norm flux = '+ str(norm_flux_jy)+' p/m '+ str(norm_uncert))
        print('rms of background: '+ str(bg_rms))
        self.write_output(norm_flux_jy,norm_uncert)

    def write_output(self,norm_flux_jy,norm_uncert):
        file1 = '/users/jburke/ebhis_scripts/data_lists_testing_sample/auto_analyse_values.csv'
        with open(file1,'a') as file:
            a= norm_flux_jy
            b=norm_uncert
            lines = [self.name,
                     self.ra,
                     self.dec,
                     str(a[0]),
                     str(b[0]),
                     '\n']
            file.write(','.join(lines))
with open('/users/jburke/ebhis_scripts/data_lists_testing_sample/auto_analyse_values.csv','w') as empty_csv:
    pass
with open('/users/jburke/ebhis_scripts/data_lists_testing_sample/auto_analyse.csv','r') as f:
    reader = csv.reader(f)
    for row in reader:
        print('...')
        print(row[0])
        obj = Gal(row[0],row[1],row[2])
        obj.extract_annuli_vals()



