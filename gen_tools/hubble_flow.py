import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import csv

'''
Plots rv vs distance to investigate hubble flow
'''
rv = []
dist =[]
with open('/users/jburke/Desktop/results/full_results.csv','r') as f:
    reader = csv.reader(f)
    header = next(reader)
    for row in reader:
        if row[9]=='-':
            pass
        else:
            rv.append(float(row[9]))
            dist.append(float(row[3]))




g_rv =[]
g_dist =[]
with open('/users/jburke/Desktop/results/group_latex_full_results.csv','r') as f:
    reader = csv.reader(f)
    header = next(reader)
    for row in reader:
        g_dist.append(float(row[1]))
with open('/users/jburke/ebhis_scripts/group_gal_results/rv_w50_results.csv','r') as f:
    reader = csv.reader(f)
    header = next(reader)
    for row in reader:
        g_rv.append(float(row[1]))


def hubble_line(D,h_0):
    return h_0*D

dists=np.arange(0,16,1)
fig, ax = plt.subplots()

ax.scatter(dist,rv,s=3,color='b',label='Isolated',)
ax.scatter(g_dist,g_rv,s=3,color='r',label='Groups')
ax.plot(dists,hubble_line(dists,74.6),'k--',linewidth=0.7,alpha=0.7,label='$H_0 = 74.6$')
ax.plot(dists,hubble_line(dists,67.4),'k-.',linewidth=0.7,alpha=0.7,label='$H_0 =67.4$')
plt.legend(loc=4)
ax.set_ylabel('Radial Velocity [km/s]')
ax.set_xlabel('Distance [Mpc]')
plt.show()