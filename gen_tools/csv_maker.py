import csv

'''
Makes blank csv file with header
'''

with open('/users/jburke/Desktop/results/full_results.csv','w') as f:
    writer = csv.writer(f)
    header = ['name','ra','dec','dist','flux ','+/-','mass x10^6Msol','+/-','rv','+/-','w50','+/-']
    writer.writerow(header)
