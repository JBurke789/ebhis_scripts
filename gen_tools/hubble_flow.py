import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import csv

'''
Plots rv vs distance to investigate hubble flow
'''
rv_vals =[]
rv_uncert = []
names =[]
with open('/users/jburke/ebhis_scripts/w50_stuff/fixed_vals.csv','r') as f:
    reader = csv.reader(f)
    header = next(reader)
    for row in reader:
        if row[1]=='-':
            pass
        else:
            names.append(row[0])
            rv_vals.append(float(row[1]))
            rv_uncert.append(float(row[2]))


dist=[]
for i in names:
    with open('/users/jburke/ebhis_scripts/workflow_results/final_results.csv','r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            if i == row[0]:
                dist.append(float(row[3]))


fig, ax = plt.subplots()

ax.scatter(dist,rv_vals,s=0.5)
ax.errorbar(dist,rv_vals,yerr=rv_uncert,fmt='o')
ax.set_ylabel('Radial Velocity [km/s]')
ax.set_xlabel('Distance [Mpc]')
plt.show()