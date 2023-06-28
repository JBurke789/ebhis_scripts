execfile('../ebhis_scripts/full_code.py')

gal_name = input('Galaxy Name: ')

#imports raw file to CASA compatable format
gal = Galaxy(gal_name,gal_name+'.fits')
gal.import_fits()

#select channels that contains galaxy and generate moment map of galaxy
imview('raw_image.im')
MW_high_chan = int(input('MW high channel: '))#used for spectra later
low_chan = int(input('Galaxy low channel number:'))
high_chan = int(input('Galaxy high channel number:'))
gal.mom0_map(low_chan,high_chan)

#calculate threshhold value
imview('no_filter_moment0/')
max_val = float(input('Max value of background: '))
rms_val = float(input('RMS value of background: '))
gal.thresh(max_val,rms_val)

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
'''Doesnt work yet            
if search_csv(gal_name):
    overwrite = input('Galaxy is already in csv. Overwrite? (y\n): ')
    if overwrite == 'y':
'''
    

