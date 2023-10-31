import csv 
import os
#removes all mom 0 maps already generated
with open('/users/jburke/Desktop/gal_candidates_big.csv','r') as f:
    reader = csv.reader(f)
    for row in reader:#looks at each galaxy
        if ' ' in row[0]:
            row[0] = row[0].replace(' ','')
        os.system('rm -rf '+row[0]+'/no_filter_mom*')