import numpy as np
'''
makes mom 0,1,2 for each chunk in  cubes and exports to fits at the end.

run in casa enviroment 
source /vol/software/software/astro/casa/initcasa.sh
 
'''
out_file_bits=['chunk0.im','chunk1.im','chunk2.im','chunk3.im']
chans=['161~354','355~548','549~742','743~840']
vels = [[300.,2300.],[2300.,4300.],[4300.,6300.],[6300.,8300.]]
        


def make_moms(name,chan,outfile):
    immoments(imagename=name,
              moments=[0,1,2],
              chans=chan,
              outfile=outfile)

def export_maps(cube_id,chunk):
    casa_files = [cube_id + chunk+'.integrated',cube_id +chunk+ '.weighted_coord',cube_id +chunk+ '.weighted_dispersion_coord']
    output_files=[cube_id + chunk+'_m0.fits',cube_id + chunk+'_m1.fits',cube_id + chunk+'_m2.fits']
    for i in range(len(casa_files)):
        exportfits(imagename=casa_files[i],
                   fitsimage=output_files[i])


for i in range(5):
    cube = 'cube'+str(i)+'.im'
    for j in range(len(chans)):
        outfile='cube'+str(i)+out_file_bits[j]
        make_moms(cube,chans[j],outfile)
        export_maps('cube'+str(i),out_file_bits[j])



