import csv
import numpy as np


'''
Lists galaxies close to a given galaxy and gives coords
'''

name = input('Name: ')



with open('/users/jburke/Desktop/full_gal_list.csv','r') as file:
    reader1 = csv.reader(file)
    header1 = next(reader1)
    for row1 in reader1:
        if name == row1[0]:
            ra = row1[1]
            dec = row1[2]
            print(name)    
            print(ra,',',dec)

        

with open('/users/jburke/Desktop/full_gal_list.csv','r') as file:
    reader1 = csv.reader(file)
    header1 = next(reader1)
    for row1 in reader1:
        if name == row1[0]:
            pass   
        else:
            ra1=row1[1]
            dec1=row1[2]
            dist=np.sqrt( (float(ra1)-float(ra))**2 + (float(dec1)-float(dec))**2)*60*60
            if dist<=4000:
                print(row1[0], 'close to galaxy')
                print(ra1,',',dec1)