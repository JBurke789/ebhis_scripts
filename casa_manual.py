#!/usr/bin/python

import os
from scipy import *
from numpy import *
from pylab import *

# browse to the directory where your data are located in
# start casa by using 'casapy in your console' (casa-installation dir needs to be in your $PATH variable)

# example data are provided in fits format, we need to convert them to the casa data format (.ms = measurement set)
#################################################################

default(importfits) # use default() to open a command and start giving input information
fitsimage='ebhis.fits' # name of the file you wish to convert
imagename='ebhis.im' # output filename
go() # start any command with 'go()'

# alternatively, try the GASS data cube:

default(importfits) # convert the raw data
fitsimage='gass.fits'
imagename='gass.im'
go()

### use the task viewer to have a look at the data
viewer()
# or viewer(infile='clean_data.im')
# use the casa cookbook for help!
# you should learn how to slide through the data cube, look at position-velocity plots, produce contour lines, print out some maps

# in the gass data cube you see Milky Way emission, in p-v you should be able to see a spiral arm
# in the ebhis data there are at least 7 galaxies visible "by naked eye", you can find them most easily by sliding through the p-v view and using something like [-0.3,1.] for the data range (which adjusts the intensity scale); hint: galaxies look like "sausages" in p-v
# you should write down for each of the galaxies there x,y,z coordinates (both in world and pixel coordinates); also you will need the velocity interval which is covered by each galaxy
# for example, one very bright galaxy is located in:
# Pixel: 87 115 540 
# Ra: 12:25:56.521 Dec +33.29.15.205  280.972 km/s
# Velocity Interval: z= 508 to 638 (v= 239 to 407 km/s) 
# makes also sense to define a subcube in x and y for later use:
# bottom left corner:  73, 103
# top right corner: 102, 130

# creating basic moment-maps
#################################################################

default(immoments)
imagename='ebhis.im'
moments=[0,1] # create moment0 and moment1 maps
box='73, 102, 103, 130' # 'lower left x/RA, lower left y/DEC, upper right x/RA, upper right y/DEC'. you should have written down these values already
chans='508~638' # velocity range (in pixels!) of the galaxy, you should have written down these values already; note the tilde is used in casa to define a range
outfile='galaxy1_moments_basic'
go()

# you can have a look at the moment maps using the viewer
# moments_basic.integrated is the moment 0 aka total intensity map
# moments_basic.weighted_coord is the moment 1 aka velocity field
# you will note, that the moment 1 looks horrible, there is a ring around the source containing totally wrong values. this is due to the low signal strength at the edge of the galaxy, see below on how to improve...


# using tresholds to create improved moment-maps
#################################################################
# by using only such pixels in the data cube which contain a certain amount of flux the influence of the noise can be decreased, to find resonable threshold values one should use either the viewer or the casa task imstat to have an estimate of the noise in the datacube
# in the viewer just go to a velocity plane which does no contain emission, and use the 'rectangle drawing' tool to define a region, double click inside - casa will pop up a message window containing some image statistics, like the standard deviation (std dev)
#Frequency=591
#Plane Npts      Sum            Mean           Rms            Std dev        #Minimum        Maximum        
#591   2475      -5.808449e+01  -2.346848e-02  5.649389e-02   5.139901e-02   -1.971492e-01  1.553935e-01   
# -> sigma is something like 51 mK
# if you like to use the imstat task just do the following:
default(imstat)
imagename = 'ebhis.im'
go
# the results are shown in the casa log messages window
# the standard deviation as computed over the FULL data cube is 0.239 K which is obviously much higher than the value computed with the casa viewer. the reason is that the milky way emission distorts the results, so we should restrict the spectral channels to not contain MW emission:
chans = '400~500'
go
# now the standard deviation is 57 mK, which is much better matching the value obtained with the viewer

# we now apply a threshold (4*sigma is resonable) when computing the image moments:
default(immoments)

imagename='ebhis.im'
moments=[0,1]
box='73, 102, 103, 130'
chans='508~638'
outfile='galaxy1_moments_treshold'
includepix=[0.2, 10000] # set your threshold to approx. 4 sigma, upper limit is not really required, just use a large number here
go()
# moment 1 now looks much better, though the velocity field is now restricted to the inner part of the galaxy


# one can still further improve the technique...; 
# creating a mask to improve our moment-maps, the mask is a copy of the data cube containing only those pixels which we want to use (in principle the thresholding technique also contains a mask)
# here we will first smooth the data cube in velocity in order to suppress noise, which will give us better results for the mask
#################################################################

# smoothing is done using a hanning filter
# casa does not provide a "task" (high level routine) but only a so-called "tool" (low level routine) to do that, tools are easy to use:
ia.open('ebhis.im') # open the file
ia.hanning('ebhis_hanning_smoothed1.im', drop=false)# submit outfile and set (drop pixels) to false
ia.close()
# have a look at the casa website to find an extensive documentation about tools: http://casa.nrao.edu/docs/casaref/CasaRef.html

# the hanning filter toolkit computes "an average" of 3 adjacent pixels (to be more exact, the data are filtered with a hanning function of width 3)

# we repeat the smoothing to obtain an even smoother datacube
ia.open('ebhis_hanning_smoothed1.im')
ia.hanning('ebhis_hanning_smoothed2.im', drop=false)
ia.close()

ia.open('ebhis_hanning_smoothed2.im')
ia.hanning('ebhis_hanning_smoothed3.im', drop=false)
ia.close()

ia.open('ebhis_hanning_smoothed3.im')
ia.hanning('ebhis_hanning_smoothed4.im', drop=false)
ia.close()

# have a look into the hanning filtered data cube to get an idea of what it dows

# note for pro-users: each application of the hanning filter would enlarge the velocity resolution by a factor of 2 IF we would set drop=true, as after filtering every second spectral channel contains redundant information and can be dropped. here, we have to keep these channels because our mask would not match the data cube anymore if pixels were dropped. the drawback is that repeated applications of the hanning filter do NOT double the velocity resolution as on could have naively assumed

# use this mask to create a better moment-map
#################################################################

### you need to find the rms noise level in images/hanning_smoothed_data4.im using imstat or viewer ...

default(imstat)
imagename = 'ebhis_hanning_smoothed4.im'
chans = '400~500'
go
# Standard deviation is something like 0.03

default(immoments)
imagename='ebhis.im'
moments=[0,1,2]
box='73, 102, 103, 130'
chans='508~638'
mask="'ebhis_hanning_smoothed4.im'>0.1" # use the hanning-smoothed data as a mask and only use pixels for the moment-map which have more than 3 sigma in the hanning-smoothed data
outfile='galaxy1_moments_masked'
go()
# actually the method is good enough to also compute the second moment ;-)
# compare the moment1_threshold with moment1_masked, do you notice the difference?
# in the moment2 map you can see, that the dispersion estimate is highest in the central part of the galaxy, this might indicate that the gas temperature is higher or that there is more turbulence or many individual gas clumps moving relatively to each other - be careful with the interpretation!

# from the moment0 we can compute a column density map; for moment-0 it is always best to use the basic moments version (without any masking/thresholding) in order to retain the TRUE flux
default(immath)
imagename='galaxy1_moments_basic.integrated'
expr='1.823e18*IM0'
outfile='galaxy1_moments_basic.integrated_NHI'
go

# in the viewer you note that the intensity units are wrong, we need to fix this:
ia.open('galaxy1_moments_basic.integrated_NHI')
ia.setbrightnessunit('1/cm**2')
ia.done() # we cannot use ia.close() here as it would not apply the change to the file

# use the viewer to create a nice image, e.g. velocity field overlaid with column density contours (it is good style to use contour lines as multiples of the std dev in the map, e.g., starting at 3 sigma in steps of 1 sigma; in order to estimate sigma for the moment map use again the rectangle drawing tool and let the viewer compute the std dev for an area outside the emission of the galaxy - this of course is only possible if your subcubes containing the galaxy are not too small)

# utilize unsharp masking
#################################################################
# sometimes one is interested small scale structures embedded in more diffuse extended emission, the idea is to subtract a spatially smoothed datacube from the original data

# first create xy-smoothed data
#################################################################

default(imsmooth) # use xy-smoothing
imagename='gass.im'
major='60arcmin' # set major and minor axis to approx. 4 x beamwidth, the GASS data were obtained using the Parkes telescope (FWHM ~ 15')
minor='60arcmin'
outfile='gass_xy_smoothed.im'
go()

# now subtract smoothed data from original data
#################################################################
default(immath)
imagename=['gass.im', 'gass_xy_smoothed.im'] # create an unsharped mask
expr='IM0-IM1'
outfile='gass_unsharp_masking.im'
go()
# you will note, that the outcome traces mainly the disk emission and features some filamentary structures



# finally, we will extract spectra from the datacube to perform gaussian profile fitting
#################################################################

blc=[78,104,400] # bottom left corner
trc=[99,128,800] # top right corner
ia.open('ebhis.im')
flux=ia.getchunk(blc,trc)
ia.close()
print flux
sumspec=sum(sum(flux,axis=0),axis=0) # need to sum over all x and y pixels in the chosen region; in theory, this could also be done with the getchunk function, but it doesnt work in the current casa version
# use matplotlib to plot any numpy array
plot (sumspec) # eventually, you will need the "show()" command, if no window pops up

# note: one can of course also extract only one spectrum per galaxy, but then in our example we would not see the nice double horn profile typical for disk galaxies

# you can also average the data
#avg=average(average(flux,axis=0),axis=0)
# print avg


# define our (line) fitting function - a Gaussian
# p[0]= amplitude
# p[1]= mean
# p[2]= stddev
# p[3]= offset

fitfunc = lambda p, x: p[0]*exp(-((x-p[1])**2)/(2.*p[2]**2) ) +p[3]

# error function = chi square function
# err = vector of weightings
errfunc = lambda p, x, y, err: (y - fitfunc(p, x)) / err

pinit = [100.,170.,20.,-20.]
yerr=ones(len(sumspec))
x=array(range(len(sumspec)))
out = optimize.leastsq(errfunc, pinit, args=(x,sumspec,yerr),full_output=1)

pfinal = out[0]
covar = out[1]
print pfinal
print covar

plot(fitfunc(pfinal,x))
plot(fitfunc(pinit,x))

# one can easily change the fitting function, e.g. use 2 Gaussians


#blc=[78,104,400] # remember blc was this

import copy

ia.open('ebhis.im')
csys=ia.coordsys()
x=array(arange(0,len(sumspec),1.)) # need floating point array
velo=copy.deepcopy(x)
blctemp=copy.deepcopy(blc)
for a in range(0,len(x)):
  blctemp[2]=x[a]+blc[2]
  w=ia.toworld(blctemp,'n')
  freq=w['numeric'][2] # gives frequencies
  v=csys.frequencytovelocity(value=freq,doppler='radio',velunit='km/s')
  velo[a]=float(v)
  #print blctemp[2],freq ,v

print velo

# close plotter before going on...
plot (velo,sumspec)

gaussfunc = lambda A,x0,sigma, x: A*exp(-((x-x0)**2)/(2.*sigma**2) )
fitfunc = lambda p, x: gaussfunc(p[0],p[1],p[2],x) + gaussfunc(p[3],p[4],p[5],x) +p[6]
errfunc = lambda p, x, y, err: (y - fitfunc(p, x)) / err
pinit = [60.,300.,20.,60.,350.,20.,-20.] # only x0 values were changed
yerr=ones(len(sumspec))

out = optimize.leastsq(errfunc, pinit, args=(velo,sumspec,yerr),full_output=1) # this time use velo as x-array
pfinal = out[0]
covar = out[1]
print pfinal
print covar

plot(velo,fitfunc(pfinal,velo))





