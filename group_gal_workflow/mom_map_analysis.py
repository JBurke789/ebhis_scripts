import csv 
import os
import numpy as np


imview('moment0.im')
group = input('group ID: ')

in_sum = float(input('Inner sum: '))
in_npix = float(input('Inner npix: '))
out_sum = float(input('Outer sum: ')) 
out_npix = float(input('Outer npix: '))
            #out_rms =  float(input('Outer rms: '))
            #bg_rms = np.sqrt((out_npix/(out_npix-in_npix))*(out_rms**2 - (in_npix/(out_npix))*in_rms**2))
bg_rms = 0.09# rms=90mK from ebhis calibration
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

save = input('Save results? y/n: ')
if save == 'y':
    with open('/users/jburke/ebhis_scripts/group_gal_results/group_results.csv','a') as f:
        lines =[group,
                str(norm_flux_jy),
                str(norm_uncert),
                '\n']
        f.write(','.join(lines))   