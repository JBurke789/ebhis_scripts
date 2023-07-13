import os
import csv
"""From candidate list, runs command to make datacubes from EBHIS, saves each to its own directory. Needs enviroment to be open already"""

file_path = '/users/jburke/Desktop/gal_candidates_big.csv'

def data_request(name, ra ,dec):
    #make directory for galaxy
    if ' ' in name:
        name = name.replace(' ','')

    try:
        os.mkdir(name)
    except FileExistsError:
        print("Directory for '{name}' already exists.")

    #make data request
    ra_vals = str(float(ra) - 3) + ' ' + str(float(ra) +3)
    dec_vals = ' ' + str(float(dec) - 2.5) + ' ' + str(float(dec) +2.5)
    filename = ' '+name+'/'+name+'.fits'

    command = 'python /vol/ebhis2/data1/bwinkel/software/hpxtools/hpxgrid4.py -ds EBHIS -s E -l ' + ra_vals + dec_vals + filename
    os.system(command)    

with open(file_path,'r') as f:
    reader = csv.reader(f)

    for row in reader:
        name = row[0]
        ra= row[1]
        dec = row[2]

        data_request(name,ra,dec)