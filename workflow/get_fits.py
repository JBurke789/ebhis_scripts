import os
import csv

"""
Run after gal_sort.py . 

Runs through the CSV files generated of galaxy candidates. Runs command to make datacubes from EBHIS. 
Saves each datacube to its own directory.
Needs enviroment already open.

"""
def data_request(name, ra ,dec):
    print('...')
    print('galaxy  --->  '+name)
    print('...')
    #make directory for galaxy
    if ' ' in name:
        name = name.replace(' ','')

    try:
        os.mkdir(name)#makes directory for galaxy
    except FileExistsError:
        print("Directory for "+ name + " already exists.")

    #make data request
    ra_vals = str(float(ra) - 3) + ' ' + str(float(ra) +3)
    dec_vals = ' ' + str(float(dec) - 2.5) + ' ' + str(float(dec) +2.5)
    filename = ' '+name+'/'+name+'.fits'

    command = 'python /vol/ebhis2/data1/bwinkel/software/hpxtools/hpxgrid4.py -ds EBHIS -s E -l ' + ra_vals + dec_vals + filename
    os.system(command)    

autogen_file_path = '/users/jburke/ebhis_scripts/full_workflow_results/auto_analyse.csv'
mw_overlap_file_path = '/users/jburke/ebhis_scripts/full_workflow_results/MW_overlap.csv'
no_w50_file_path ='/users/jburke/ebhis_scripts/full_workflow_results/no_linewidth.csv'


print('...')
print('auto_analyse.csv galaxies')
print('...')
with open(autogen_file_path,'r') as f:
    reader = csv.reader(f)
    header = next(reader)
    #length = str(len(list(reader)))
    i=0
    for row in reader:
        i+=1
    length = i
with open(autogen_file_path,'r') as f:
    reader = csv.reader(f)
    header = next(reader)
    j=1
    for row in reader:
        print(str(j)+ ' of '+ str(length))
        j+=1
        name = row[0]
        ra= row[1]
        dec = row[2]
        data_request(name,ra,dec)
print('...')
print('MW_overlap.csv galaxies')
print('...')
with open(mw_overlap_file_path,'r') as f:
    reader = csv.reader(f)
    header = next(reader)
    #length = str(len(list(reader)))
    i=0
    for row in reader:
        i+=1
    length = i
with open(mw_overlap_file_path,'r') as f:
    reader = csv.reader(f)
    header = next(reader)
    j=1
    for row in reader:
        print(str(j)+ ' of '+ str(length))
        j+=1
        name = row[0]
        ra= row[1]
        dec = row[2]
        data_request(name,ra,dec)

print('...')
print('no_linewidth.csvgalaxies')
print('...')
with open(no_w50_file_path,'r') as f:
    reader = csv.reader(f)
    header = next(reader)
    #length = str(len(list(reader)))
    i=0
    for row in reader:
        i+=1
    length = i
with open(no_w50_file_path,'r') as f:
    reader = csv.reader(f)
    header = next(reader)
    j=1
    for row in reader:
        print(str(j)+ ' of '+ str(length))
        j+=1
        name = row[0]
        ra= row[1]
        dec = row[2]
        data_request(name,ra,dec)