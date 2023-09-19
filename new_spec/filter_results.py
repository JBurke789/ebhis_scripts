import csv
import numpy as np
import os


csvpath = '/users/jburke/ebhis_scripts/new_spec/filtered_results.csv'
if not os.path.exists(csvpath):
    with open('/users/jburke/ebhis_scripts/new_spec/detailed_results.csv','r') as f:
        reader = csv.reader(f)
        header = next(reader)
        extra = ['note']
        header = header + extra
        with open(csvpath,'w') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(header)
else:
    pass


with open('/users/jburke/ebhis_scripts/new_spec/detailed_results.csv','r') as f:
    reader = csv.reader(f)
    header = next(reader)
    for row in reader:
        if row[7]=='n/a':
            pass
        else:
            with open(csvpath,'a') as file:
                csv_writer = csv.writer(file)
                csv_writer.writerow(row)