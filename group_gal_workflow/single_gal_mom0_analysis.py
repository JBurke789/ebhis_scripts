import csv 
import os
import numpy as np

gal_results=[]
with open('/users/jburke/ebhis_scripts/group_gal_results/single_group_gals.csv','r') as f:
    reader = csv.reader(f)
    header = next(reader)
    for row in reader:
        gal_results.append(row)
galaxy = input('Galaxy name: ')
imview(galaxy+'_moment0.im')


in_sum = float(input('Inner sum: '))
in_npix = float(input('Inner npix: '))
out_sum = float(input('Outer sum: ')) 
out_npix = float(input('Outer npix: '))
bg_rms = 0.09# rms=90mK from ebhis calibration
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
    with open('/users/jburke/Desktop/full_gal_list.csv','r') as f:#get initial row vals from full list
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            if row[0]==galaxy:
                init_row = row
    #run through gals already analysed and replace values
    gals_analysed=[]
    for i in gal_results:#replaces values if galaxy already analysed
        gals_analysed.append(i[0])
        if i[0]==galaxy:
            i[7]=str(norm_flux_jy)
            i[8]=str(norm_uncert)
    #append gal vals if not already analysed
    if galaxy not in gals_analysed:
        new_add = [str(norm_flux_jy),str(norm_uncert)]
        new_row = init_row+new_add
        gal_results.append(new_row)
    
    with open('/users/jburke/ebhis_scripts/group_gal_results/single_group_gals.csv','w') as f:
        csv_writer = csv.writer(f)
        header=['name','ra','dec','distance','radial_velocity','h1_21_cm_mag','h1_21_cm_50pc_width','flux [Jy km/s BA^-1]','uncert']
        csv_writer.writerow(header)
        csv_writer.writerows(gal_results)


