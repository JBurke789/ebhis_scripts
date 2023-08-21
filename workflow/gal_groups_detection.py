import os
import csv

#create empty csv files to save results from sorting in and set header, same as input file
'''with open('/users/jburke/Desktop/full_gal_list.csv','r') as f:
    reader = csv.reader(f)
    header = next(reader)
    with open('/users/jburke/ebhis_scripts/workflow_results/gal_groups.csv','w') as empty_csv:
        csv_writer = csv.writer(empty_csv)
        csv_writer.writerow(header)
'''
ra = float(input('RA: '))
dec = float(input('dec: '))
with open('/users/jburke/Desktop/full_gal_list.csv','r') as file:
    reader = csv.reader(file)
    header = next(reader)
    for gal in reader:
        ra_dist = abs(ra - float(gal[1]))
        dec_dist= abs(dec - float(gal[2]))
        if ra_dist<= 1. and dec_dist<=1.:
            print(str(gal[0])+' is close')
