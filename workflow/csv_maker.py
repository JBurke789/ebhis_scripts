import csv
"""
with open('/users/jburke/ebhis_scripts/w50_stuff/overlap_spectra.csv','r') as file:
    reader = csv.reader(file)
    header = next(reader)
    with open('/users/jburke/ebhis_scripts/group_gal_results/single_group_gals.csv','w') as f:
        writer = csv.writer(f)
        writer.writerow(header)
"""
with open('/users/jburke/ebhis_scripts/w50_stuff/new_vals.csv','w') as f:
    writer = csv.writer(f)
    header = ['name','rv','+/-','w50','+/-']
    writer.writerow(header)