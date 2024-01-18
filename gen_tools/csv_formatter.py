import csv
import astropy.units as u
import numpy as np
from astropy.coordinates import SkyCoord
'''
makes csv ready to be latex table
'''
#get flux and ra/dec vals
full_list =[]
with open('/users/jburke/Desktop/results/full_results.csv','r') as f:
    reader = csv.reader(f)
    header = next(reader)
    for row in reader:
        full_list.append(row)


def coord_convert(ra,dec):
    coord_deg = SkyCoord(ra=float(ra) * u.deg, dec=float(dec) * u.deg)
    ra_hms = coord_deg.ra.to_string(unit=u.hour, sep=':', precision=2, pad=True)
    dec_dms = coord_deg.dec.to_string(unit=u.degree, sep=':', precision=1, pad=True, alwayssign=True)
    return ra_hms, dec_dms

def rounding(num,uncert,dec_places):
    if num =='-' or uncert=='-':
        return '-'
    else:
        val = str(round(float(num), dec_places))
        pm = str(round(float(uncert),dec_places))
        string = val+ ' $\pm$ ' + pm
        return string

#convert row vals
new_full_list=[]
for row in full_list:
    #convert coords
    ra,dec = coord_convert(row[1],row[2])
    #round figs
    rv = rounding(row[9],row[10],1)
    w50 = rounding(row[11],row[12],1)

    flux = rounding(row[4],row[5],1)                       
    mass = str(round(float(row[7]),1))
    
    
    new_row=[row[0],ra,dec,row[3],row[6],rv,w50,flux,mass]


    new_full_list.append(new_row)

with open('/users/jburke/Desktop/results/latex_full_results.csv','w') as f:
    writer = csv.writer(f)
    header = ['Object','RA','Dec','D','Method','v ','w50','flux','Mass']
    writer.writerow(header)
    writer.writerows(new_full_list)


