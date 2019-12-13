#!/c/Python36/python
"""
Lidar Test
Date: 12/10/2019
"""

import os 
import numpy as np
import matplotlib.pyplot as plt

def read_data(filename):
    angle = []
    distance = []
    quality = []

    with open(filename, mode='r') as file:
        for _ in range(3):
            next(file)
        for line in file:
            ldata = line.split()
            angle.append(float(ldata[0]))
            distance.append(float(ldata[1]))
            quality.append(float(ldata[2]))
    
    #convert lists to numpy arrays
    angle = np.array(angle)
    distance = np.array(distance)
    quality = np.array(quality)
    
    return angle, distance, quality

def plot_data(pt_num, distance, gradient, dtype, plt_layout):
    fig = plt.figure(figsize=(12,10))
    pl = plt_layout
    
    color = 'blue'
    ax1 = fig.add_axes([pl[0],pl[1],pl[2],pl[2]], ylabel=dtype, title='Test Plot')
    ax1.plot(pt_num, distance, color=color)
    
    color = 'red'
    ax2 = ax1.twinx()
    ax2.set_ylabel('Gradient')
    ax2.plot(pt_num[:-1], gradient, color=color)
    
    #plt.savefig(figtitle, bbox_inches='tight')
            
'''############################################################################
# MAIN
############################################################################'''
#directories
home_dir = os.path.dirname(os.path.realpath(__file__))[:-6]
data_dir = home_dir + 'data/'

#data filenames
filename = data_dir + '3_pillow_test'

#read in data
angle, distance, quality = read_data(filename)
pt_num = np.array(range(len(angle))) #get point number for plotting purposes

#perform QC
ndx = np.where(quality >= 100.) #can change QC threshold later
angle = angle[ndx]
distance = distance[ndx]
pt_num = pt_num[ndx]
gradient = np.diff(distance) #get gradient, will currently mess up when QC excludes points, can perform an average to fill in blanks

plt_layout = [0.1, 0.1, 0.8,0.8]
plot_data(pt_num, distance, gradient,'distance', plt_layout)

