import csv
import astropy.units as u
import numpy as np
from astropy.coordinates import SkyCoord
'''
makes csv ready to be latex table
'''
#get flux and mass vals
fm_list =[]
with open('/users/jburke/ebhis_scripts/group_gal_results/mass_results.csv','r') as f:
    reader = csv.reader(f)
    header = next(reader)
    for row in reader:
        fm_list.append(row)
#rv and w50 vals
rv_list =[]
with open('/users/jburke/ebhis_scripts/group_gal_results/rv_w50_results.csv','r') as f:
    reader = csv.reader(f)
    header = next(reader)
    for row in reader:
        rv_list.append(row)


def rounding(num,uncert,dec_places):
    if num =='-' or uncert=='-':
        return '-'
    else:
        val = str(round(float(num), dec_places))
        pm = str(round(float(uncert),dec_places))
        string = val+ ' $\pm$ ' + pm
        return string


rows =[]
for i in range(len(fm_list)):
    rv = rounding(rv_list[i][1],rv_list[i][2],1)
    w50 = rounding(rv_list[i][3],rv_list[i][4],1)
    flux = rounding(fm_list[i][2],fm_list[i][3],1)

    new_row =[fm_list[i][0],round(float(fm_list[i][1]),1),rv,w50,flux,fm_list[i][4]]
    rows.append(new_row)

print(rows)

with open('/users/jburke/Desktop/results/group_latex_full_results.csv','w') as f:
    writer = csv.writer(f)
    header = ['Group','m_D','v ','w50','flux','Mass']
    writer.writerow(header)
    writer.writerows(rows)