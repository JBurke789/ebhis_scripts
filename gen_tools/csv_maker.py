import csv

'''
Makes blank csv file with header
'''

with open('/users/jburke/ebhis_scripts/new_spec/results.csv','w') as f:
    writer = csv.writer(f)
    header = ['name','Flux [Jy km/s BA^-1]','+/-','low vel [km/s]','high vel [km/s]','hanning level']
    writer.writerow(header)