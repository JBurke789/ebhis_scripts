import csv

'''
Makes blank csv file with header
'''

with open('/users/jburke/ebhis_scripts/w50_stuff/MW_overlap_results.csv','w') as f:
    writer = csv.writer(f)
    header = ['name','rv','+/-','w50','+/-','hanning level']
    writer.writerow(header)
