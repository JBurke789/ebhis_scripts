import csv

'''
exports mom map to a fits file for group
run in casa enviroment in group directory

'''




#casa_file = 'moment0.im'
casa_file = 'no_filter_moment0'
outfile = 'mom0.fits'

exportfits(imagename=casa_file,
               fitsimage=outfile)
print('fits image saved')
    