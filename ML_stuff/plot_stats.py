import numpy as np
import matplotlib.pyplot as plt

# cube 1
m0_1 =[[24.0,5,-0.8,-1,4.6,6.2,2.0,-9.8],
       [10.1,11.4,8.3,12.62,14.2,14.3,16.7,24.7],
       [26.1,12.5,8.4,12.66,14.9,15.6,16.8,26.5]]

m1_1=[[-59,1189,38.16,6361,8777,11159,13792,16682],
      [52,522,594,553,484,458,462,591],
      [78,1299,3862,6385,8789,11168,138000,16692]]

m2_1=[[569.9,790,884,843,803,709,788,964],
      [277,456,488,467,420,318,384,567],
      [633,912.6,1010,965,906,777,872,1119]]

# cube 2
m0_2 =[[109,12,0.5,-2.5,-1.1,0.7,1.3,3.2],
       [186,44,13.1,42.6,56.6,68.5,76.3,117.7],
       [216,46,13.1,42.7,56.6,68.5,76.3,117.8]]

m1_2 =[[-134,750,3768,6373,8826,11255,13782,16699],
       [206,560,624,458,434,410,402,527],
       [246,936,3820,6390,8837,11262,13788,16707]]

m2_2 =[[351,819,905,730,708,722,730,919],
       [205,455,547,381,357,320,314,315],
       [406,937,1058,823,792,789,795,972]]

#plot
def plot(map,title):
    x =[1,2,3,4,5,6,7,8]
    fig, (ax1,ax2,ax3) = plt.subplots(3,1,sharex=True)
    ax1.plot(x,map[0])
    ax1.set_ylabel('Mean')
    ax2.plot(x,map[1])
    ax2.set_ylabel('stan dev')
    ax3.plot(x,map[2])
    ax3.set_ylabel('RMS')
    plt.suptitle(title)
    plt.tight_layout()
    plt.show()

#plot(m0_1,'cube 1, mom 0')
#plot(m1_1,'cube 1, mom 1')
plot(m2_1,'cube 1, mom 2')

#plot(m0_2,'cube 2, mom 0')
#plot(m1_2,'cube 2, mom 1')
#plot(m2_2,'cube 2, mom 2')