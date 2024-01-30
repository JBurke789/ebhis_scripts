import os
import numpy as np
"""
source /vol/ebhis2/data1/bwinkel/software/.activate_conda_hook.sh
conda activate ebhis
"""


coords = [[135.,52.5],
          [315.,32.5],
          [180.,37.5],
          [2.5,2.5],
          [90.,27.5]]

def get_coord_lims(coord):
    ra1  = coord[0]-2
    ra2  = coord[0]+2
    dec1 = coord[1]-2
    dec2 = coord[1]+2
    string = str(ra1)+ ' ' +str(ra2)+ ' ' +str(dec1)+ ' ' +str(dec2)
    return string


def get_cube(coords,index):
    name = 'cube'+str(index)+'.fits'
    command='python /vol/ebhis2/data1/bwinkel/software/hpxtools/hpxgrid4.py -s E -l ' + coords+ ' -db E --eglob "/vol/ebhis2/data1/bwinkel/multibeam/ebhis_hpx_e9/*/*/*{:s}*_healpix.fits" '+name
    os.system(command)   

test_coords =[135.,52.5]

for i in range(len(coords)):
    string = get_coord_lims(coords[i])
    get_cube(string,i)