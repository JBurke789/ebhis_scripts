import csv
import numpy as np

gal_rows=[]
with open('/users/jburke/ebhis_scripts/new_spec/results.csv','r') as f:
    reader = csv.reader(f)
    header = next(reader)
    for row in reader:
        gal_rows.append(row)

gal_dist =[]
with open('/users/jburke/ebhis_scripts/catagorisation/cat_results/MW_overlap.csv','r') as f:
    reader = csv.reader(f)
    header = next(reader)
    for row in reader:
        line = [row[0],row[3]]
        gal_dist.append(line)

def mass_calc(dist,flux,uncert):
    m= 2.36e5 * (dist**2)* flux *1e-6
    u = 2.36* (dist**2)*uncert*1e-6

    return m , u


mass_results=[]
for row in gal_rows:
    name = row[0]
    #dist = float(row[3])
    flux = float(row[1])
    f_uncert= float(row[2])
    for gal in gal_dist:
        if name == gal[0]:
            dist = float(gal[1])


    mass,uncert = mass_calc(dist,flux,f_uncert)
    new_row = [name,flux,f_uncert,mass,uncert]
    mass_results.append(new_row)
    print(new_row)


with open('/users/jburke/ebhis_scripts/mass_calcs/results/mass_results_spec.csv','w') as f:
    writer = csv.writer(f)
    header = ['name','flux [Jy/BA]','+/-','mass [M_sol x10^6]','+/-']
    writer.writerow(header)
    writer.writerows(mass_results)