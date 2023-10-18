import csv
import numpy

gal_rows=[]
with open('/users/jburke/ebhis_scripts/workflow_results/final_results.csv','r') as f:
    reader = csv.reader(f)
    header = next(reader)
    for row in reader:
        gal_rows.append(row)


def mass_calc(dist,flux,uncert):
    m= 2.36e5 * (dist**2)* flux
    u = 2.36* (dist**2)*uncert

    return m , u


mass_results=[]

