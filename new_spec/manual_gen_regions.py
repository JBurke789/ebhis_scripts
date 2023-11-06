import csv

with open('/users/jburke/ebhis_scripts/catagorisation/cat results/MW_overlap.csv','r') as f:
    reader = csv.reader(f)
    header = next(reader)
    for row in reader:
        name = row[0]
        rv = row[4]
        w50 = row[6]
        print('RV: ' , rv)
        print('W50: ' , w50)
        imview(name+'/raw_image.im')
        next = input('done')