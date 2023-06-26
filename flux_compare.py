
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np

names=['HoI','NGC4214','NGC4736','DDO154','NGC5457']

ethings = np.array([39.6, 323,   95.7,151,1680])
my_vals = np.array([20.4, 332.9, 58.7, 77,2979])
my_vals = np.array([20.4, 332.9, 58.7, 77,2979])
x= np.array([1,2,3,4,5])

plt.figure()
plt.scatter(x,ethings,label='ETHINGS')
plt.scatter(x,my_vals,label='my vals')
plt.show()