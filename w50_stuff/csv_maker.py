import csv

with open('/users/jburke/ebhis_scripts/w50_stuff/overlap_spectra.csv','r') as file:
    reader = csv.reader(file)
    header = next(reader)
    with open('/users/jburke/ebhis_scripts/w50_stuff/ready_to_analyse.csv','w') as f:
        writer = csv.writer(f)
        writer.writerow(header)
