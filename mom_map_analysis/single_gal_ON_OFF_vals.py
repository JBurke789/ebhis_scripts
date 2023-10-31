import numpy as np
import csv

'''
Calculates annulus method for single galaxy.
appends to final results csv so need to check by hand if galaxy is already in there

Need to have galaxy already open in casa viewer and run this in different terminal
'''




name = 'NGC4288'


gal_results=[]
with open('/users/jburke/ebhis_scripts/workflow_results/final_results.csv','r')as f:
    reader = csv.reader(f)
    header = next(reader)
    for row in reader:
        gal_results.append(row)


sum_ON = float(input('ON sum:'))
pix_ON = float(input('ON npix:' ))

sum_OFF= float(input('OFF sum:'))
pix_OFF= float(input('OFF npix:'))

bg_rms = 0.09# rms=90mK from ebhis calibration

OFF_norm_sum = (sum_OFF*pix_ON)/pix_OFF

clean_sum_ON = sum_ON-OFF_norm_sum
flux_jy = clean_sum_ON/1.28
norm_flux_jy = flux_jy/8.64
uncert = bg_rms*np.sqrt(pix_ON)
frac_uncert = uncert/clean_sum_ON
norm_uncert = frac_uncert*norm_flux_jy 
print('norm flux = '+ str(norm_flux_jy)+' p/m '+ str(norm_uncert))


with open('/users/jburke/Desktop/full_gal_list.csv','r')as f:
    reader = csv.reader(f)
    header = next(reader)
    for row in reader:
        if row[0]==name:
            init_row = row

new_row = init_row+[norm_flux_jy,norm_uncert]

with open('/users/jburke/ebhis_scripts/workflow_results/final_results.csv','a')as f:
    writer = csv.writer(f)
    writer.writerow(new_row)
