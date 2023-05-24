import os
import numpy as np

#give inputs to be used
im_name='raw_image.im'
dB = 'G'

low_chan=60
high_chan= 133
MW_high_chan = 125

xbl= 125 #box around galaxy
ybl= 130
xtr= 175
ytr= 175

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
if dB=='G':#bigger box
    xbls=[xbl-100, xbl-100, xtr+50 , xtr+50]#define coords for 4 boxes around galaxy
    ybls=[ybl-100, ytr+50 , ytr+50 , ybl-100]
    xtrs=[xbl-50 , xbl-50 , xtr+100, xtr+100]
    ytrs=[ybl-50 , ytr+100, ytr+100, ybl-50]
elif dB=='E':#smaller box
    xbls=[xbl-20, xbl-20, xtr   , xtr   ]#define coords for 4 boxes around galaxy
    ybls=[ybl-20, ytr   , ytr   , ybl-20]
    xtrs=[xbl   , xbl   , xtr+20, xtr+20]
    ytrs=[ybl   , ytr+20, ytr+20, ybl   ]  
stdevs=[]

if (low_chan- MW_high_chan)<= 20:
    std_lw= high_chan +10
    std_hgh= high_chan + 30

else:
    std_lw = MW_high_chan
    std_hgh = low_chan


for i in range(4):#calc stdev in each of the boxes
    coord = str(xbls[i]) + ',' + str(ybls[i]) + ',' + str(xtrs[i]) + ',' + str(ytrs[i])
    stats=imstat(imagename= 'hanningsmoothed.im',
                 box=coord,
                 chans= str(std_lw)+'~'+str(std_hgh))
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
#os.system('rm -r no_filter_moment0*')#remove old file

#generate moment maps using hanning filter
immoments(imagename=im_name,
          moments=[0,1,2],
          #box=box_coords,
          chans=channels,
          mask=mask_string,
          outfile='moment_map')#use smoothed data as a mask and only use pixels for moment map with more than 3 sigma of hanning data sigma = 0.05
