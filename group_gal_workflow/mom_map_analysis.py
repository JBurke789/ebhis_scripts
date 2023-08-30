import csv 
import os
import numpy as np

gal_results=[]
with open('/users/jburke/ebhis_scripts/group_gal_results/group_results.csv','r') as f:
    reader = csv.reader(f)
    header = next(reader)
    for row in reader:
        gal_results.append(row)

print(gal_results)

imview('moment0.im')
group = input('group ID: ')

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
    #run through gals already analysed and replace values
    groups_analysed=[]
    for i in gal_results:
        groups_analysed.append(i[0])
        if i[0]==group:
            i[1]=str(norm_flux_jy)
            i[2]=str(norm_uncert)
    #append gal vals if not already analysed
    if group not in groups_analysed:
        new_row = [group,str(norm_flux_jy),str(norm_uncert)]
        gal_results.append(new_row)

    sorted_gal_results= sorted(gal_results,key = lambda x: float(x[0]))
    with open('/users/jburke/ebhis_scripts/group_gal_results/group_results.csv','w') as f:
        csv_writer = csv.writer(f)
        header=['Group','flux [Jy km/s /BA]','uncert']
        csv_writer.writerow(header)
        csv_writer.writerows(sorted_gal_results)


