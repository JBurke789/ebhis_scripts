import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import csv

mass_vals =[]
with open('/users/jburke/ebhis_scripts/workflow_results/mass_results.csv','r') as f:
    reader = csv.reader(f)
    header = next(reader)
    for row in reader:
        mass_vals.append(float(row[3]))

with open('/users/jburke/ebhis_scripts/new_spec/mass_results_spec.csv','r') as f:
    reader = csv.reader(f)
    header = next(reader)
    for row in reader:
        mass_vals.append(float(row[3]))

plt.hist(mass_vals,20)
plt.xlabel('Mass [M_sol x10^6]')
plt.ylabel('counts')
plt.title('Mass function')
plt.show()