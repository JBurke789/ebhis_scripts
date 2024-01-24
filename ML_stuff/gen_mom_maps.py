import numpy as np
'''
run casa enviroment 
source /vol/software/software/astro/casa/initcasa.sh
'''

raw_im = 'empty.fits'
out_files=['chunk1.im','chunk2.im','chunk3.im','chunk4.im','chunk5.im','chunk6.im','chunk7.im','chunk8.im']
chans=['000~132','133~374','375~617','618~860','861~1102','1103~1345','1346~1587','1588~1918']
vels = [[-1358.0,0],[0.0,2500],[2500,5000],[5000,7500],[7500,10000],[1250,1500],[1500,18500]]
        
def make_moms(chan,outfile):
    immoments(imagename=raw_im,
              moments=[0,1,2],
              chans=chan,
              outfile=outfile)

def unit_conversion(temp):
    flux_jy = temp/1.28
    flux_BA = flux_jy/8.64
    return flux_BA

for i in range(len(out_files)):
    make_moms(chans[i],out_files[i])
    file = out_files[i]+'.weighted_coord'
    stats=imstat(file)
    #sd = unit_conversion(stats['sigma'])
    #print(stats)
    #print('sd=',stats['sigma'])


def export_maps(name):
    casa_files = [name + '.integrated',name + '.weighted_coord',name + '.weighted_dispersion_coord']
    output_files=[name + '_m0.fits',name + '_m1.fits',name + '_m2.fits']
    for i in range(len(casa_files)):
        exportfits(imagename=casa_files[i],
                   fitsimage=output_files[i])


for file in out_files:
    export_maps(file)

    

