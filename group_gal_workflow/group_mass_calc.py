import numpy as np
import csv

id =input('group ID: ')

#mean dist of group
gal_dist =[]#get all dists
with open('/users/jburke/Desktop/full_gal_list.csv','r') as f:
    reader = csv.reader(f)
    header = next(reader)
    for row in reader:
        line = [row[0],row[3]]
        gal_dist.append(line)

gals =[]#get gals in groups
gal='init'
while gal != '':
    gal =input('gal name: ')
    gals.append(gal)

dists=[]#get dists for gals in group
for i in gals:
    for row in gal_dist:
        if i == row[0]:
            dists.append(float(row[1]))
m_dist = np.mean(np.array(dists))#calc mean

#get flux for group
fluxes =[]
with open('group_gal_results/group_results.csv','r') as f:
    reader = csv.reader(f)
    header = next(reader)
    for row in reader:
        new_row = [row[0],row[1],row[2]]
        fluxes.append(new_row)
for i in fluxes:
    if id == i[0]:
        flux = [float(i[1]),float(i[2])]


#mass calc
def mass_calc(dist,flux,uncert):
    m= 2.36e5 * (dist**2)* flux *1e-6
    u = 2.36* (dist**2)*uncert*1e-6
    return m , u

mass, uncert = mass_calc(m_dist,flux[0],flux[1])

#save results
results =[id,m_dist,flux[0],flux[1],mass]

with open('/users/jburke/ebhis_scripts/group_gal_results/mass_results.csv','a') as f:
    writer = csv.writer(f)
    writer.writerow(results)
