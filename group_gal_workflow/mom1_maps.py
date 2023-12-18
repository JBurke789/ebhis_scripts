import numpy as np
import csv
import os
"""
Run in casa and in directory of group
source /vol/software/software/astro/casa/initcasa.sh
"""



gal_names =[]
name='init'
while name!= '':
    name = input('Galaxy name: ')
    gal_names.append(name)

gal_info=[]
with open('/users/jburke/Desktop/full_gal_list.csv','r')as f:
    reader = csv.reader(f)
    header = next(reader)
    for row in reader:
        gal_info.append(row)

lv =[]
hv=[]
for gal in gal_names:
    for full_gal in gal_info:
        if gal == full_gal[0]:
            print(gal+' ok')
            w50 = float(full_gal[6])
            rv = float(full_gal[4])
            low_v = rv-0.5*w50
            high_v = rv + 0.5*w50
            lv.append(low_v)
            hv.append(high_v)
print(lv)
print(hv)
low_lim = min(lv)
high_lim= max(hv)
vels = np.linspace(-606.648,609.427,945)
l_ind = np.argmin(np.abs(np.array(vels)-low_lim))
h_ind = np.argmin(np.abs(np.array(vels)-high_lim))
channels= str(l_ind)+'~'+str(h_ind)

path_raw = 'raw_image.im'


ia.open(path_raw)
ia.hanning('hanningsmooth1.im',drop=False)
ia.close()
ia.open('hanningsmooth1.im')
ia.hanning('hanningsmooth2.im',drop=False)
ia.close()
ia.open('hanningsmooth2.im')
ia.hanning('hanningsmooth3.im',drop=False)
ia.close()
ia.open('hanningsmooth3.im')
ia.hanning('hanningsmoothed.im',drop=False)
ia.close()

path_hanning = 'hanningsmoothed.im'

print('hanning generated')

immoments(imagename=path_raw,
          moments=[1],
          chans=channels,
          mask="'hanningsmoothed.im'>0.27",
          outfile='masked_mom1_map')

print('mom1 map generated')

os.system('rm -r *hanningsmooth1.im')#remove 
os.system('rm -r *hanningsmooth2.im')
os.system('rm -r *hanningsmooth3.im')
os.system('rm -r *hanningsmoothed.im')