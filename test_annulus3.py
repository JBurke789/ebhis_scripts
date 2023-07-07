import numpy as np
import os

file_path = 'region.crtf'
def make_region_file(ra,dec):
    with open(file_path,'w') as file:
        lines = ['#CRTFv0 CASA Region Text Format version 0 \n','ellipse [[12:15:29.78083, +036.19.28.9158], [1400.0827arcsec, 1372.9140arcsec], 0.00000000deg] coord=J2000, corr=[I], linewidth=1, linestyle=-, symsize=1, symthick=1, color=magenta, font="DejaVu Sans", fontsize=11, fontstyle=normal, usetex=false']
        file.write(''.join(lines))
        print('region file created')
        
ra = '183.9121'
dec= ' 36.3275'
make_region_file(ra,dec)
"""stats = imstat(imagename='no_filter_moment0',
               region = 'region.crtf')

sum = stats['sum']
rms = stats['rms']

print('sum:', sum)
print('rms:',rms)
"""