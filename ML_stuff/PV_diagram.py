import matplotlib.pyplot as plt
import numpy as np

from astropy.visualization import quantity_support
from astropy import units as u
from astropy import wcs


from pvextractor import extract_pv_slice, Path
from astropy.coordinates import SkyCoord
from spectral_cube import SpectralCube


cube = SpectralCube.read('EG_empty_sky.fits')
#cube_m0 = SpectralCube.read('..\..\..\Desktop\ML_stuff\EG_m0_map.fits')
path=Path(SkyCoord([190,189.1]*u.deg , [44,43]*u.deg , frame='fk5'))

#ax = plt.subplot(111, projection=cube.wcs.celestial)
#ax.imshow(cube_m0[0].value,aspect='equal')
#path.show_on_axis(ax, spacing=1, color='r')
#ax.set_xlabel(f"Right Ascension [{cube.wcs.wcs.radesys}]")
#ax.set_ylabel(f"Declination [{cube.wcs.wcs.radesys}]")
#plt.show()

pv_diagram = extract_pv_slice(cube,path)
ww = wcs.WCS(pv_diagram.header)

ax = plt.subplot(111, projection=ww)
im = ax.imshow(pv_diagram.data,aspect='auto',vmin=-0.01,vmax=0.2)
cb = plt.colorbar(mappable=im)
cb.set_label("Brightness Temperature [K]")

ax0 = ax.coords[0]
ax0.set_format_unit(u.arcmin)
ax1 = ax.coords[1]
ax1.set_format_unit(u.km/u.s)
ax.set_ylabel("Velocity [km/s]")
ax.set_xlabel("Offset [arcmin]")
ax.set_title('EG')
plt.show()



