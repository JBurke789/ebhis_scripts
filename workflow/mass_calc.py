import csv
import numpy

gal_rows=[]
with open('/users/jburke/ebhis_scripts/workflow_results/final_results.csv','r') as f:
    reader = csv.reader(f)
    header = next(reader)
    for row in reader:
        gal_rows.append(row)


def mass_calc(dist,flux,uncert):
    m= 2.36e5 * (dist**2)* flux *1e-6
    u = 2.36* (dist**2)*uncert*1e-6

    return m , u


mass_results=[]
for row in gal_rows:
    name = row[0]
    dist = float(row[3])
    flux = float(row[7])
    f_uncert= float(row[8])

    mass,uncert = mass_calc(dist,flux,f_uncert)
    new_row = [name,flux,f_uncert,mass,uncert]
    mass_results.append(new_row)
    print(new_row)


with open('/users/jburke/ebhis_scripts/workflow_results/mass_results.csv','w') as f:
    writer = csv.writer(f)
    header = ['name','flux [Jy/BA]','+/-','mass [M_sol x10^6]','+/-']
    writer.writerow(header)
    writer.writerows(mass_results)