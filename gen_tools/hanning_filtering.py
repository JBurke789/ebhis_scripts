import csv

"""
runs through csv of galaxies and runs hanning filtering 4 times for each galaxy

run in CASA
source /vol/software/software/astro/casa/initcasa.sh


"""

def run_han(name):
    ia.open(name+'/MW_pipe.im') # open the file
    ia.hanning(name+'/hanning_smoothed1.im', drop=False)# submit outfile and set (drop pixels) to false
    ia.close()
    ia.open(name+'/hanning_smoothed1.im')
    ia.hanning(name+'/hanning_smoothed2.im', drop=False)
    ia.close()
    ia.open(name+'/hanning_smoothed2.im')
    ia.hanning(name+'/hanning_smoothed3.im', drop=False)
    ia.close()
    ia.open(name+'/hanning_smoothed3.im')
    ia.hanning(name+'/MW_hanning_smoothed4.im', drop=False)
    ia.close()
    print("Hanning run on ", name)
"""
with open('/users/jburke/ebhis_scripts/catagorisation/cat_results/MW_overlap.csv','r') as f:
    reader = csv.reader(f)
    head = next(reader)
    for row in reader:
        run_han(row[0])
"""
name = 'NGC4449'

run_han(name)
