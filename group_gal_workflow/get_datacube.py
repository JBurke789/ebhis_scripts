import csv
import numpy as np
import os

"""
Run in directory of group. Needs EBHIS environment to be open

source /vol/ebhis2/data1/bwinkel/software/.activate_conda_hook.sh
conda activate ebhis
"""
galaxy_names = []

name='initial'
while name!='':
    name = input('galaxy name:')
    if name!='':
        galaxy_names.append(name)

ra_vals =[]
dec_vals=[]
min_vel =[]
max_vel =[]
rows = []
for i in galaxy_names:
    with open('/users/jburke/Desktop/full_gal_list.csv','r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            if i == row[0]:
                #append galaxy values to lists
                rows.append(row)
                ra_vals.append(float(row[1]))
                dec_vals.append(float(row[2]))
                #generate region file for each galaxy in  group
                file1 =  row[0]+'region.crtf'
                with open(file1,'w') as file:
                    lines = ['#CRTFv0 CASA Region Text Format version 0 \n',
                             'ellipse [[',row[1],'deg,',row[2],'deg], [800arcsec, 800arcsec], 0.00000000deg],label="',row[0],'"']
                    file.write(''.join(lines))

  
  

np.save('group_info.npy',rows)

#make data request in EBHIS
ra_val = str(min(ra_vals)-5) + ' ' + str(max(ra_vals)+5)
dec_val = ' ' + str(min(dec_vals)-5) + ' ' + str(max(dec_vals)+5)
filename = ' data_cube.fits'

command = 'python /vol/ebhis2/data1/bwinkel/software/hpxtools/hpxgrid4.py -ds EBHIS -s E -l ' + ra_val + dec_val + filename
os.system(command)    
                