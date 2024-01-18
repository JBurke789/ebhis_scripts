import csv

'''
Makes blank csv file with header
'''

with open('/users/jburke/ebhis_scripts/group_gal_results/mass_results.csv','w') as f:
    writer = csv.writer(f)
    header = ['group','m_dist','flux','uncert','mass']
    writer.writerow(header)


