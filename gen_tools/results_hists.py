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


'''
Plot results
'''
def bin_size(array):
    width , bin_edges = knuth_bin_width(array,return_bins=True)
    return bin_edges
fig, ((ax1,ax2),(ax3,ax4))=plt.subplots(2,2)





ax1.hist(np.log10(mass),bins=bin_size(np.log10(mass)))
ax1.set_xlabel('log Mass [M_sol x10^6]')
ax1.set_ylabel('counts')

ax2.hist(w50,bins=bin_size(w50))
ax2.set_xlabel('w50 [km/s]')
ax2.set_ylabel('counts')


ax3.hist(rv,bins=bin_size(rv))
ax3.set_xlabel('radial velocity[km/s]')
ax3.set_ylabel('counts')

bin_edges=bin_size(np.log10(mean_flux))
new_bins =[]
for i in bin_edges:
    val = 10**i
    new_bins.append(val)
#ax4.hist(mean_flux,bins=int((np.log(mean_flux).max() - np.log(mean_flux).min()) / bin_width))
ax4.hist(mean_flux, bins=new_bins)
ax4.set_xlabel('Mean Flux Density')
ax4.set_ylabel('counts')
ax4.set_xscale('log')
ax4.set_yscale('log')




plt.show()