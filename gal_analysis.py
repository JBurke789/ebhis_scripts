execfile('../ebhis_scripts/full_code.py')

gal_name = input('galaxy Name: ')

gal = Galaxy(gal_name,gal_name+'.fits')
gal.import_fits()
imview('raw_image.im')

low_chan = int(input('Low channel number:'))
high_chan = int(input('High channel number:'))
gal.mom0_map(low_chan,high_chan)
imview('no_filter_moment0/')
