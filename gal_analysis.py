import numpy as np


execfile('../ebhis_scripts/full_code.py')
gal_name = input('Galaxy Name: ')

#imports raw file to CASA compatable format
gal = Galaxy(gal_name,gal_name+'.fits')
gal.import_fits()


#select channels that contains galaxy and generate moment map of galaxy
def gen_momap():
    imview('raw_image.im')
    MW_high_chan = int(input('MW high channel: '))#used for spectra later
    low_chan = int(input('Galaxy low channel number:'))
    high_chan = int(input('Galaxy high channel number:'))
    gal.mom0_map(low_chan,high_chan)

gen_momap()
#Annulus Method


def annulus_method():
    imview('no_filter_moment0/')
    inner_val = float(input('inner circle sum: '))
    inner_rms = float(input('inner circle rms: '))
    inner_pix = float(input('n pix inner circle: '))

    outer_val = float(input('Outer circle sum: '))
    outer_rms = float(input('Outer circle rms: '))
    outer_pix = float(input('n pix outer circle: '))

    bg_flux = outer_val-inner_val
    bg_pix = outer_pix-inner_pix
    bg_per_pix = bg_flux/bg_pix
    clean_flux = inner_val - bg_per_pix*inner_pix
    flux_jy = clean_flux/1.28
    norm_flux_jy = flux_jy/8.64

    bg_rms = np.sqrt((outer_pix/(bg_pix))*(outer_rms**2 - (inner_pix/outer_pix)*inner_rms**2))
    uncert = bg_rms*np.sqrt(inner_pix)
    frac_uncert = uncert/clean_flux
    print('Flux = '+ str(flux_jy)+' p/m '+ str(uncert))
    print('norm flux = '+ str(norm_flux_jy)+' p/m '+ str(frac_uncert*norm_flux_jy))
    print('rms of background: '+ str(bg_rms))

annulus_method()







#max_val = float(input('Max value of background: '))
#rms_val = float(input('RMS value of background: '))
#gal.thresh(max_val,rms_val)
'''
gal_sum = float(input('Galaxy sum: '))
npix = float(input('Number of pixels: '))
gal.gal_vals(gal_sum,npix)

#save results to a text file
file= open(gal_name+'.txt','w')
file.write('Galaxy channels: ' +str(low_chan) + '~' + str(high_chan)+ '\n')
file.write('Threshold: ' + str(gal.thresh)+'\n')
file.write('Normalised total flux: ' + str(gal.normalised_tot_flux) + '+-'+str(gal.uncertainty*gal.normalised_tot_flux)+'\n')
file.close()

#save results to csv file
def search_csv(name):
    with open('~/ebhis_scripts/values.csv','r') as file:
        reader = csv.reader(file)
        for row in reader:
            if name in row:
                return True
    return False
Doesnt work yet            
if search_csv(gal_name):
    overwrite = input('Galaxy is already in csv. Overwrite? (y\n): ')
    if overwrite == 'y':
'''
    

