import csv 
import os

with open('/users/jburke/Desktop/gal_candidates_big.csv','r') as f:
    reader = csv.reader(f)
    for row in reader:#looks at each galaxy
        if ' ' in row[0]:
            row[0] = row[0].replace(' ','')
        os.system('rm -rf '+row[0]+'/no_filter_mom*')