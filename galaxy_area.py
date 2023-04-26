import numpy as np
import os

#define input galaxy details.
im_name='moment_map.integrated'
xbl= 130 #box around galaxy
ybl= 130
xtr= 170 
ytr= 170

#find standard deviation of background
xbls=[xbl-50, xbl-50,    xtr,    xtr]#define coords for 4 boxes around galaxy
ybls=[ybl-50,    ytr,    ytr, ybl-50]
xtrs=[   xbl,    xbl, xtr+50, xtr+50]
ytrs=[   ybl, ytr+50, ytr+50,    ybl]
stdevs=[]
for i in range(4):#calc stdev in each of the boxes
    coord = str(xbls[i]) + ',' + str(ybls[i]) + ',' + str(xtrs[i]) + ',' + str(ytrs[i])
    stats=imstat(imagename= im_name,
                 box=coord)
    stdevs.append(stats['sigma'][0])
mn_stdev = np.mean(np.array(stdevs))#calc mean stdev