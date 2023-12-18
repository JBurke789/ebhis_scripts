import os 
import csv

'''
source /vol/software/software/astro/casa/initcasa.sh
'''

def run_han(name):
    ia.open(name+'/raw_image.im') # open the file
    ia.hanning(name+'/hanning_smoothed1.im')# submit outfile and set (drop pixels) to false
    ia.close()
    ia.open(name+'/hanning_smoothed1.im')
    ia.hanning(name+'/hanning_smoothed2.im')
    ia.close()
    ia.open(name+'/hanning_smoothed2.im')
    ia.hanning(name+'/hanning_smoothed3.im')
    ia.close()
    ia.open(name+'/hanning_smoothed3.im')
    ia.hanning(name+'/hanning_smoothed4.im')
    ia.close()
    print("Hanning run on ", name)


number_list = [str(i).zfill(2) for i in range(1, 31)]

print(number_list)
groups=[]
for i in number_list:
    x = 'group'+i
    groups.append(x)

for i in groups:
    run_han(i)