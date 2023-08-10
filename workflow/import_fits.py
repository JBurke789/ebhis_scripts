import csv
import os

#function to import the datacube of a single galaxy to a CASA format
def import_fit(name):
    datacube_path = name+'/'+name+'.fits'
    rawim_path = name+'/raw_image.im'
    importfits(fitsimage=datacube_path,
           imagename=rawim_path)
    
#runs through lists of galaxies with datacubes and imports datacube if it has not already been done
with open('/users/jburke/ebhis_scripts/full_workflow_results/auto_analyse.csv','r') as f:
    reader = csv.reader(f)
    header = next(reader)
    for row in reader:#looks at each galaxy
        name= row[0]
        if ' ' in name:
            name = name.replace(' ','')
        dir = name+'/raw_image.im'
        if os.path.isdir(dir):
            print(name+' fits file already imported')
        else:
            import_fit(name)
            print(name,' fits file imported')

with open('/users/jburke/ebhis_scripts/full_workflow_results/MW_overlap.csv','r') as f:
    reader = csv.reader(f)
    header = next(reader)
    for row in reader:#looks at each galaxy
        name= row[0]
        if ' ' in name:
            name = name.replace(' ','')
        dir = name+'/raw_image.im'
        if os.path.isdir(dir):
            print(name+' fits file already imported')
        else:
            import_fit(name)
            print(name,' fits file imported')

with open('/users/jburke/ebhis_scripts/full_workflow_results/no_linewidth.csv','r') as f:
    reader = csv.reader(f)
    header = next(reader)
    for row in reader:#looks at each galaxy
        name= row[0]
        if ' ' in name:
            name = name.replace(' ','')
        dir = name+'/raw_image.im'
        if os.path.isdir(dir):
            print(name+' fits file already imported')
        else:
            import_fit(name)
            print(name,' fits file imported')