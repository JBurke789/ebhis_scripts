import csv

'''
exports all the moment zero maps to a fits file
run in casa enviroment
'''

gal_names = []
with open('/users/jburke/ebhis_scripts/workflow_results/final_results.csv','r') as f:
    reader = csv.reader(f)
    header = next(reader)
    for row in reader:
        gal_names.append(row[0])

def make_fits(name):
    casa_file = name +'/no_filter_moment0'
    outfile = name + '/' +name +'mom0.fits'

    exportfits(imagename=casa_file,
               fitsimage=outfile)
    print(name + ' fits image made.')
    

for i in gal_names:
    make_fits(i)
