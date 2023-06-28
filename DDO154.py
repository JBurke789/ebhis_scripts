execfile('../ebhis_scripts/full_code.py')

gal= Galaxy('DDO154','DDO154.fits')
gal.import_fits()
gal.gal_coords(700,850)
gal.mom0_map()
gal.thresh(5.251814,1.791467)
gal.gal_vals(2690.121,494)
'''
Threshold: 5.287643340000001
total flux: 60.9571797187499 +- 31.107299987811825 Jy km/s
Normalised total flux: 7.055229134114571 +- 3.6003819430337756 Jy km/s
'''