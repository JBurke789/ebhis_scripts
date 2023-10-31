import numpy as np
import os
import csv

'''
Automatically generates concentric regions around galaxy.

Calculates galaxy vals and and adds to final results or adds to manual analysis csv

Run in CASA enviroment 
source /vol/software/software/astro/casa/initcasa.sh

'''
class Gal:
    def __init__(self,row):
        self.row= row
        self.name=row[0]
        self.ra = row[1]
        self.dec = row[2]
        self.dist = row[3]
        self.radvel = row[4]
        self.mag21 = row[5]
        self.w50 = row[6]

    def make_region_files(self):
        #makes 5 region files of increasing radius
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

    def annulus_calc(self,inner_sum,inner_npix,outer_sum,outer_npix):
        #calculates flux from values in annuli
        bg_flux = outer_sum-inner_sum
        bg_npix = outer_npix-inner_npix
        bg_per_pix = bg_flux/bg_npix
        clean_flux = inner_sum - bg_per_pix*inner_npix
        flux_jy = clean_flux/1.28
        norm_flux_jy = flux_jy/8.64
        bg_rms = 0.09 #rms = 90mK, from EBHIS calibration
        uncert = bg_rms*np.sqrt(inner_npix)
        frac_uncert = uncert/clean_flux
        norm_uncert = frac_uncert*norm_flux_jy
        lowest_val = norm_flux_jy-norm_uncert
        if lowest_val>=0:
            self.write_output(norm_flux_jy,norm_uncert)
            print('Flux = '+ str(flux_jy)+' p/m '+ str(uncert))
            print('norm flux = '+ str(norm_flux_jy)+' p/m '+ str(norm_uncert))
            print('rms of background: '+ str(bg_rms))
        else:
            print('negative norm flux => DO BY HAND')
            with open('/users/jburke/ebhis_scripts/mom_map_analysis/results/need_manual_analysis.csv','a') as file:
                lines = [self.name,
                        self.ra,
                        self.dec,
                        self.dist,
                        self.radvel,
                        self.mag21,
                        self.w50,
                        '\n']
                file.write(','.join(lines))


    def extract_annuli_vals(self):
        self.make_region_files()
        #run imstat on each circle and get values
        stats1 = imstat(imagename=str(self.name)+'/no_filter_moment0',
                region = str(self.name)+'/region1.crtf')
        sum1 = stats1['sum']
        #rms1 = stats1['rms']
        npix1 = stats1['npts']
        stats2 = imstat(imagename=str(self.name)+'/no_filter_moment0',
                region = str(self.name)+'/region2.crtf')
        sum2 = stats2['sum']
        #rms2 = stats2['rms']
        npix2 = stats2['npts']
        stats3 = imstat(imagename=str(self.name)+'/no_filter_moment0',
                region = str(self.name)+'/region3.crtf')
        sum3 = stats3['sum']
        #rms3 = stats3['rms']
        npix3 = stats3['npts']
        stats4 = imstat(imagename=str(self.name)+'/no_filter_moment0',
                region = str(self.name)+'/region4.crtf')
        sum4 = stats4['sum']
        #rms4 = stats4['rms']
        npix4 = stats4['npts']
        stats5 = imstat(imagename=str(self.name)+'/no_filter_moment0',
                region = str(self.name)+'/region5.crtf')
        sum5 = stats5['sum']
        #rms5 = stats5['rms']
        npix5 = stats5['npts']
        #calculate noise per pixel in each annuli
        sum_ann1 = (sum2-sum1)/(npix2-npix1)
        sum_ann2 = (sum3-sum2)/(npix3-npix2)
        sum_ann3 = (sum4-sum3)/(npix4-npix3)
        sum_ann4 = (sum5-sum4)/(npix5-npix4)
        #calculate rms of annuli
        """
        rms_ann1 = np.sqrt((npix2/(npix2-npix1))*(rms2**2 - (npix1/(npix2))*rms1**2))
        rms_ann2 = np.sqrt((npix3/(npix3-npix2))*(rms3**2 - (npix2/(npix3))*rms2**2))
        rms_ann3 = np.sqrt((npix4/(npix4-npix3))*(rms4**2 - (npix3/(npix4))*rms3**2))
        rms_ann4 = np.sqrt((npix5/(npix5-npix4))*(rms5**2 - (npix4/(npix5))*rms4**2))
        """
        
        #check if annuli have same vals
        ann_diff1 = abs(sum_ann1-sum_ann2)/sum_ann2
        ann_diff2 = abs(sum_ann2-sum_ann3)/sum_ann3
        ann_diff3 = abs(sum_ann3-sum_ann4)/sum_ann4
        #detection threshold (bg+3*rms)
        rms = 0.09
        detect_thresh1 = (sum_ann1 + 3*rms)*npix1
        detect_thresh2 = (sum_ann2 + 3*rms)*npix1
        detect_thresh3 = (sum_ann3 + 3*rms)*npix1
        detect_thresh4 = (sum_ann4 + 3*rms)*npix1
        if detect_thresh2<=sum1 :
            if ann_diff1<= 0.1:
                print('First annuli have similar values (<10%)=> proceed ')
                self.annulus_calc(sum1,npix1,sum2,npix2)
            elif ann_diff1>= 0.1 and ann_diff2<= 0.1:
                print('Second annuli have similar values (<10%)=> proceed ')
                self.annulus_calc(sum2,npix2,sum3,npix3)
            elif ann_diff2>= 0.1 and ann_diff3<= 0.1:
                print('Second annuli have similar values (<10%)=> proceed ')
                self.annulus_calc(sum3,npix3,sum4,npix4)
            else:
                print('Large variation between annuli(>10%)=> DO BY HAND')
                with open('/users/jburke/ebhis_scripts/mom_map_analysis/results/need_manual_analysis.csv','a') as file:
                    write= csv.writer(file)
                    write.writerow(self.row)
        else:
            print('galaxy is not detected=> DO BY HAND')
            with open('/users/jburke/ebhis_scripts/mom_map_analysis/results/need_manual_analysis.csv','a') as file:
                write= csv.writer(file)
                write.writerow(self.row)

    def write_output(self,norm_flux_jy,norm_uncert):
        file1 = '/users/jburke/ebhis_scripts/mom_map_analysis/results/final_results.csv'
        with open(file1,'a') as file:
            a= norm_flux_jy
            b=norm_uncert
            lines = [self.name,
                     self.ra,
                     self.dec,
                     self.dist,
                     self.radvel,
                     self.mag21,
                     self.w50,
                     str(a[0]),
                     str(b[0]),
                     '\n']
            file.write(','.join(lines))


#make empty csv to save galaxies to be done by hand
with open('/users/jburke/Desktop/test_gal_list.csv','r') as f:
    reader = csv.reader(f)
    header = next(reader)
    with open('/users/jburke/ebhis_scripts/mom_map_analysis/results/need_manual_analysis.csv','w') as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow(header)
#empty csv to save final results in
    header_new = header + ['flux [Jy km/s BA^-1]','uncert']
    with open('/users/jburke/ebhis_scripts/mom_map_analysis/results/final_results.csv','w') as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow(header_new)

#go through csv of galaxies woth mom0 maps and run analysis on them and save results to correct csv file
with open('/users/jburke/ebhis_scripts/mom_map_analysis/results/gals_with_m0maps.csv','r') as f:
    reader = csv.reader(f)
    header = next(reader)
    for row in reader:
        print('...')
        print(row[0])
        obj = Gal(row)
        obj.extract_annuli_vals()

