import csv

with open('/users/jburke/ebhis_scripts/w50_stuff/overlap_spectra.csv','r') as file:
    reader = csv.reader(file)
    header = next(reader)
    with open('/users/jburke/ebhis_scripts/w50_stuff/rv_w50_vals.csv','w') as f:
        writer = csv.writer(f)
        adds = ['RV [km/s]','uncert','w50 [km/s]','uncert']
        new_header = header+adds
        writer.writerow(new_header)
