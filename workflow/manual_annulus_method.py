import csv 
import os
import numpy as np

class galaxy:
    def __init__(self,row):
        self.row= row
        self.name=row[0]
        self.ra = row[1]
        self.dec = row[2]

    def region_vals(self):
        map_name = self.name+'/no_filter_moment0'
        imview(map_name)
        in_sum = float(input('Inner sum: ')) 
        in_npix = float(input('Inner npix: '))
        in_rms =  float(input('Inner rms: '))
        out_sum = float(input('Outer sum: ')) 
        out_npix = float(input('Outer npix: '))
        out_rms =  float(input('Outer rms: '))
        bg_rms = np.sqrt((out_npix/(out_npix-in_npix))*(out_rms**2 - (in_npix/(out_npix))*in_rms**2))
        #calculates flux from values in annuli
        bg_flux = out_sum-in_sum
        bg_npix = out_npix-in_npix
        bg_per_pix = bg_flux/bg_npix
        clean_flux = in_sum - bg_per_pix*in_npix
        flux_jy = clean_flux/1.28
        norm_flux_jy = flux_jy/8.64
        uncert = bg_rms*np.sqrt(in_npix)
        frac_uncert = uncert/clean_flux
        norm_uncert = frac_uncert*norm_flux_jy 
        print('norm flux = '+ str(norm_flux_jy)+' p/m '+ str(norm_uncert))
        setattr(self,'norm_flux',norm_flux_jy)
        setattr(self,'norm_flux_uncert',norm_uncert)

with open('/users/jburke/ebhis_scripts/workflow_results/gals_with_m0maps.csv','r') as f:
    reader = csv.reader(f)
    for row in reader:
        obj=galaxy(row)
        obj.region_vals()
        #save results?
        save = input('Save results?: (y/n) ')
        if save == 'y':
            file1 = '/users/jburke/ebhis_scripts/workflow_results/final_results'
            with open(file1,'a') as file:
                a= obj.norm_flux
                b=obj.norm_flux_uncert
                lines = [obj.name,
                         obj.ra,
                         obj.dec,
                         str(a[0]),
                         str(b[0]),
                         '\n']
                file.write(','.join(lines))
        else:
            print(obj.name,' not saved')