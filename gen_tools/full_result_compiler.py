import csv
import numpy as np
import os


#get flux and ra/dec vals
full_list =[]

with open('/users/jburke/ebhis_scripts/mom_map_analysis/results/final_results.csv','r') as f:
    reader = csv.reader(f)
    header = next(reader)
    for row in reader:
        new_row = [row[0],row[1],row[2],row[3],row[7],row[8],'m']
        full_list.append(new_row)

gal_deets = []
with open('/users/jburke/Desktop/full_gal_list.csv','r') as f:
    reader = csv.reader(f)
    header = next(reader)
    for row in reader:
        new_row = [row[0],row[1],row[2],row[3]]
        gal_deets.append(new_row)

with open('/users/jburke/ebhis_scripts/new_spec/results.csv','r') as f:
    reader = csv.reader(f)
    header = next(reader)
    for row in reader:
        name = row[0]
        flux = row[1]
        flux_uncert = row[2]
        for gal in gal_deets:
            if gal[0]==name:
                ra = gal[1]
                dec= gal[2]
                dist=gal[3]
        new_row = [name,ra,dec,dist,flux,flux_uncert,'s']
        full_list.append(new_row)


#get mass vals
mass_vals =[]
with open('/users/jburke/ebhis_scripts/mass_calcs/results/mom_map_mass_results.csv','r') as f:
    reader = csv.reader(f)
    header = next(reader)
    for row in reader:
        vals= [row[0],row[3],row[4]]
        mass_vals.append(vals)
with open('/users/jburke/ebhis_scripts/mass_calcs/results/mass_results_spec.csv','r') as f:
    reader = csv.reader(f)
    header = next(reader)
    for row in reader:
        vals= [row[0],row[3],row[4]]
        mass_vals.append(vals)
    
for mass_val in mass_vals:
    name = mass_val[0]
    add_bit = [mass_val[1],mass_val[2]]
    for gal in full_list:
        if gal[0]==name:
            gal.extend(add_bit)

print(full_list[0])

#w50 and rv vals
rv_vals=[]
with open('/users/jburke/ebhis_scripts/w50_stuff/MW_overlap_results.csv','r') as f:
    reader = csv.reader(f)
    header = next(reader)
    for row in reader:
        vals= [row[0],row[1],row[2],row[3],row[4]]
        rv_vals.append(vals)
with open('/users/jburke/ebhis_scripts/w50_stuff/fixed_vals.csv','r') as f:
    reader = csv.reader(f)
    header = next(reader)
    for row in reader:
        vals= [row[0],row[1],row[2],row[3],row[4]]
        rv_vals.append(vals)

for rv_val in rv_vals:
    name = rv_val[0]
    add_bit = [rv_val[1],rv_val[2],rv_val[3],rv_val[4]]
    for gal in full_list:
        if gal[0] == name:
            gal.extend(add_bit)

for i in full_list:
    if len(i)==9:
        add_bit=['-','-','-','-']
        i.extend(add_bit)

#check for mom map
for gal in full_list:
    name = gal[0]
    filepath1 = '/users/jburke/Desktop/results/man_mom0_maps/'+name+'.png'
    filepath2 = '/users/jburke/Desktop/results/mom0_maps/'+name+'.png'
    if os.path.exists(filepath1) or os.path.exists(filepath2):
        add_bit =['y']
    else:
        add_bit=['-']
    gal.extend(add_bit)

print(full_list[0])

for gal in full_list:
    name = gal[0]
    filepath1 = '/users/jburke/Desktop/results/MW_overlap_spectra/'+name+'.png'
    filepath2 = '/users/jburke/Desktop/results/new_spectra/'+name+'.png'
    if os.path.exists(filepath1) or os.path.exists(filepath2):
        add_bit =['y']
    else:
        add_bit=['-']
    gal.extend(add_bit)

print(full_list[0])

with open('/users/jburke/Desktop/results/full_results.csv','w') as f:
    writer = csv.writer(f)
    header = ['name','ra','dec','dist','flux ','+/-','method','mass x10^6Msol','+/-','rv','+/-','w50','+/-','mom map','spec']
    writer.writerow(header)
    writer.writerows(full_list)
