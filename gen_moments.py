import os
import numpy as np

#give inputs to be used
im_name='NGC3198_EBHIS.im'

xbl= 130 #box around galaxy
ybl= 130
xtr= 170 
ytr= 170

low_chan= 70
high_chan= 205
box_coords = str(xbl) + ',' + str(ybl) + ',' + str(xtr) + ',' + str(ytr)
channels=str(low_chan)+'~'+str(high_chan)

#remove existing files so can run again from scratch
os.system('rm -rf hanningsmoothed*')
os.system('rm -rf column_density_map*')
os.system('rm -rf moment_map*')


#Hanning filtering
ia.open(im_name)
ia.hanning('hanningsmooth1.im',drop=False)
ia.close()
ia.open('hanningsmooth1.im')
ia.hanning('hanningsmooth2.im',drop=False)
ia.close()
ia.open('hanningsmooth2.im')
ia.hanning('hanningsmooth3.im',drop=False)
ia.close()
ia.open('hanningsmooth3.im')
ia.hanning('hanningsmoothed.im',drop=False)
ia.close()
os.system('rm -r *hanningsmooth1.im')#remove intermediary steps
os.system('rm -r *hanningsmooth2.im')
os.system('rm -r *hanningsmooth3.im')

#get stddev for hanning filter in region with no galaxy (make three cubes and get mean of stddevs)
xbls=[xbl-50, xbl-50,    xtr,    xtr]#define coords for 4 boxes around galaxy
ybls=[ybl-50,    ytr,    ytr, ybl-50]
xtrs=[   xbl,    xbl, xtr+50, xtr+50]
ytrs=[   ybl, ytr+50, ytr+50,    ybl]
stdevs=[]
for i in range(4):#calc stdev in each of the boxes
    coord = str(xbls[i]) + ',' + str(ybls[i]) + ',' + str(xtrs[i]) + ',' + str(ytrs[i])
    stats=imstat(imagename= 'hanningsmoothed.im',
                 box=coord,
                 chans= str(low_chan-50)+'~'+str(low_chan))
    stdevs.append(stats['sigma'][0])
mn_stdev = np.mean(np.array(stdevs))#calc mean stdev
mask_string = "'hanningsmoothed.im'" + ">" + str(mn_stdev*3)

#create moment 0 map with no filter to use for for contour map.
#preserves total flux=> needed for column density map
immoments(imagename=im_name,
          moments=[0],
          #box=box_coords,
          chans=channels,
          outfile='no_filter_moment0')
immath(imagename= 'no_filter_moment0',
       expr='1.823e18*IM0',
       outfile='column_density_map')
ia.open('column_density_map')#fix units
ia.setbrightnessunit('1/cm**2')
ia.done()
os.system('rm -r no_filter_moment0*')#remove old file

#generate moment maps using hanning filter
immoments(imagename=im_name,
          moments=[0,1,2],
          #box=box_coords,
          chans=channels,
          outfile='moment_map',
          mask=mask_string)#use smoothed data as a mask and only use pixels for moment map with more than 3 sigma of hanning data sigma = 0.05
