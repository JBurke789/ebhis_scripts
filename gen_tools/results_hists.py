import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import csv
from astropy.stats import knuth_bin_width




'''
get values to plot from results file
'''
rv = []
w50= []
mass=[]
flux= []
with open('/users/jburke/Desktop/results/full_results.csv','r') as f:
    reader = csv.reader(f)
    header = next(reader)
    for row in reader:
        mass.append(float(row[7]))
        if row[9]=='-':
            pass
        else:
            rv.append(float(row[9]))
            w50.append(float(row[11]))
            flux.append(float(row[4]))
mean_flux=[]
for i in range(len(flux)):
    val = flux[i]/w50[i]
    mean_flux.append(val)
print('median mean flux = ',np.median(np.array(mean_flux)))

'''
Plot results
'''
def bin_size(array):
    width , bin_edges = knuth_bin_width(array,return_bins=True)
    return bin_edges
fig, (ax1,ax2,ax3)=plt.subplots(3,1)





ax1.hist(np.log10(mass),color='k',bins=bin_size(np.log10(mass)),histtype='step')
ax1.set_xlabel('log (M$_{\mathrm{HI}}$) [M$_\odot$ x10$^6$]')
ax1.set_ylabel('counts')

ax2.hist(w50,bins=bin_size(w50),color='k',histtype='step')
ax2.set_xlabel('w50 [km s$^{-1}$]')
ax2.set_ylabel('counts')


ax3.hist(rv,bins=bin_size(rv),histtype='step',color='k')
ax3.set_xlabel('radial velocity[km s$^{-1}$]')
ax3.set_ylabel('Counts')



bin_edges=bin_size(np.log10(mean_flux))
new_bins =[]
for i in bin_edges:
    val = 10**i
    new_bins.append(val)

#line_x = np.linspace(0.1,100,1000)
line_x=np.arange(0.1,100,0.01)
line_y =50*line_x**(-2.5)
print(line_x,line_y)

fig4, (ax4)=plt.subplots(1,1)
#ax4.hist(mean_flux,bins=int((np.log(mean_flux).max() - np.log(mean_flux).min()) / bin_width))
ax4.hist(mean_flux, bins=new_bins,histtype='step',color='k')
ax4.plot(line_x,line_y)
ax4.set_xlabel('Mean Flux Density [Jy BA$^{-1}$]')
ax4.set_ylabel('Counts')
ax4.set_xscale('log')
ax4.set_yscale('log')




plt.show()