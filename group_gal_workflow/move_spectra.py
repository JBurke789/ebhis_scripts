import numpy as np
import os

groups=[]

id ='init'
while id != '':
    id = input('gal ID: ')
    groups.append(id)

def group_name(id):
    path = 'group'+id
    return path

paths =[]
files =[]
for i in groups:
    paths.append( [group_name(i)+'/'+group_name(i)+'_spectrum_h0.npy',group_name(i)+'_spectrum_h0.npy'])
    paths.append( [group_name(i)+'/'+group_name(i)+'_spectrum_h1.npy',group_name(i)+'_spectrum_h1.npy'])
    paths.append( [group_name(i)+'/'+group_name(i)+'_spectrum_h2.npy',group_name(i)+'_spectrum_h2.npy'])
    paths.append( [group_name(i)+'/'+group_name(i)+'_spectrum_h3.npy',group_name(i)+'_spectrum_h3.npy'])
    paths.append( [group_name(i)+'/'+group_name(i)+'_spectrum_h4.npy',group_name(i)+'_spectrum_h4.npy'])


for i in paths:
    command= 'cp ' + i[0] + ' /users/jburke/Desktop/group_spectra/'+i[1]
    print(command)
    os.system(command)



