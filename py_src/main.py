#!/c/Python36/python
"""
Lidar Test
Date: 12/10/2019
"""

import os 
import numpy as np
import matplotlib.pyplot as plt

def read_data(fname):
    angle = []
    distance = []
    quality = []

    with open(fname, mode='r') as file:
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

def detect_bed_centers(gradient, nbeds):
    bed_width = len(gradient)/nbeds
    
    bed_centers = []
    for i in range(nbeds):
        gdx1 = int(np.round((bed_width * i) - (bed_width/2)))
        gdx2 = int(np.round((bed_width * i) + (bed_width/2)))
        gdx3 = int(np.round((bed_width * (i+1)) + (bed_width/2)))
        
        if gdx1<0:
            gdx1 = 0
        if gdx3>(len(gradient)-1):
            gdx3 = len(gradient)-1
        
        fleft = np.argmin(gradient[gdx1:gdx2]) + gdx1 #left furrow
        fright = np.argmax(gradient[gdx2:gdx3]) + gdx2 #right furrow
        bed_centers.append(np.round((fleft + fright)/2))
        
    return bed_centers
    
def plot_data(pt_num, distance, angle, gradient, bed_centers, dtype, plt_layout):
    fig = plt.figure(figsize=(12,10))
    pl = plt_layout
    
    color = 'blue'
    ax1 = fig.add_axes([pl[0],pl[1],pl[2],pl[2]], ylabel=dtype, title='Test Plot')
    ax1.plot(pt_num, distance, color=color)
    ax1.scatter(bed_centers[0], distance[int(bed_centers[0])], s=150, c='magenta')
    ax1.scatter(bed_centers[1], distance[int(bed_centers[1])], s=150, c='magenta')
    ax1.scatter(bed_centers[2], distance[int(bed_centers[2])], s=150, c='magenta')
    
    color = 'red'
    ax2 = ax1.twinx()
    ax2.set_ylabel('Gradient')
    ax2.plot(pt_num[:-1], gradient, color=color)
    
# =============================================================================
#     color = 'green'
#     ax3 = ax1.twinx()
#     ax3.set_ylabel('Gradient Deriv')
#     ax3.plot(pt_num[:-2], np.diff(gradient), color=color)
# =============================================================================
    
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

#detect bed centers
bed_centers = detect_bed_centers(gradient, 3)

plt_layout = [0.1, 0.1, 0.8,0.8]
plot_data(pt_num, distance, angle, gradient, bed_centers, 'distance', plt_layout)

