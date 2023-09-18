import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np
import csv


#name = input('galaxy name: ')

array = np.load('spectrum.npy')
"""
with open('/users/jburke/Desktop/full_gal_list.csv','r') as f:
   reader = csv.reader(f)
   header = next(reader)
   for row in reader:
        if row[0]== name:
            radvel = float(row[4])
            w50 = row[6]
            if w50 =='':
                w50 = 0
            else:
                w50 = float(w50)

"""
fig1,ax1 = plt.subplots()
#ax1.plot(array[0],array[1]-array[2])
ax1.plot(array[0],array[1],label='gal')
ax1.plot(array[0],array[2],label='bg')
ax1.plot(array[0],array[1]-array[2],label='gal-bg')
#ax1.plot(array[0],array[3],label='ann2')
#ax1.axvline(radvel, color='red', linestyle='--',label='Rad vel')
#if w50!= 0:
 #   ax1.axvline(radvel+w50,color='red',linestyle='--',label='w50',alpha=0.4)
  #  ax1.axvline(radvel-w50,color='red',linestyle='--',alpha=0.4)
ax1.set_xlabel('Velocity [km/s]')
ax1.set_ylabel('Flux per Beam Area [Jy/BA]')
#ax1.set_title(name)
ax1.legend()
#fig1.savefig(name+'/spectrum.png',dpi=600)
plt.show()
