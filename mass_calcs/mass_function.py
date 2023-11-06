import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import csv

'''
histogram of galaxy masses
'''

mass_vals =[]
with open('/users/jburke/ebhis_scripts/mass_calcs/results/mom_map_mass_results.csv','r') as f:
    reader = csv.reader(f)
    header = next(reader)
    for row in reader:
        mass_vals.append(float(row[3]))

with open('/users/jburke/ebhis_scripts/mass_calcs/results/mass_results_spec.csv','r') as f:
    reader = csv.reader(f)
    header = next(reader)
    for row in reader:
        mass_vals.append(float(row[3]))

plt.hist(mass_vals,25)
plt.xlabel('Mass [M_sol x10^6]')
plt.ylabel('counts')
plt.yscale('log')
plt.title('Mass function')
plt.show()