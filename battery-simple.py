#!/usr/bin/python
## Plotting script 
## Author: Matteo Varvello 
import os 
import sys
import numpy as np
import time
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})
rcParams.update({'figure.autolayout': True})
rcParams.update({'errorbar.capsize': 2})
from pylab import *
from os import listdir
from os.path import isfile, join, isdir
from collections import defaultdict
from datetime import datetime
import matplotlib.patches as patches

# get name of the script 
script_name = os.path.basename(__file__)

# simple helper to lighten a color 
def lighten_color(color, amount=0.5):
    import matplotlib.colors as mc
    import colorsys
    try:
        c = mc.cnames[color]
    except:
        c = color
    c = colorsys.rgb_to_hls(*mc.to_rgb(c))
    return colorsys.hls_to_rgb(c[0], 1 - amount * (1 - c[1]), c[2])

# global parameters
light_green = '#90EE90'
color       = ['blue', light_green, lighten_color('magenta'), 'black', 'purple', 'orange', 'yellow', 'pink']    # colors supported
style       = ['solid', 'dashed', 'dotted']              # styles of plots  supported
marker_list = ['v', 'h', 'D', '8', '+' ]                 # list of markers supported
width = 0.3   # width for barplot 
bar_colors   = ['red', 'blue', light_green, 'magenta', 'black', 'purple', 'orange', 'yellow', 'pink']    # colors supported
#bar_colors = ['orange', 'red', 'blue', 'darkorange', 'c', 'purple']
patterns = [ "", "x" , "+" , "x", "*" ]

# increase font 
font = {'weight' : 'medium',
        'size'   : 16}
#'family' : 'normal',
matplotlib.rc('font', **font)

# main goes here 
def main():
    # data
    detection = [0.14, 0.09]
    hashing   = [0.15, 0.07]
    ZKP       = [5.45, 1.03]

    # plotting
    count = 0
    plt.figure()
    ax = plt.gca()
    ax.bar(count, detection[0], width, yerr = detection[1], align='center', alpha=0.8, ecolor='black', capsize=5, color = color[count], hatch = patterns[1])
    count += 1 
    
    ax.bar(count, hashing[0], width, yerr = hashing[1], align='center', alpha=0.8, ecolor='black', capsize=5, color = color[count], hatch = patterns[1])        
    count += 1 

    ax.bar(count, ZKP[0], width, yerr = ZKP[1], align='center', alpha=0.8, ecolor='black', capsize=5, color = color[count], hatch = patterns[1])        
    
    # figure characteristics
    custom_lines = []
    custom_lines.append(patches.Rectangle((0,0),1,1,facecolor='white', edgecolor ='black', hatch = patterns[1]))
    labels = ['detection', 'hash', 'ZKP']
    x_pos = np.arange(count + 1)
    plt.xticks(x_pos, labels,  fontsize = 14)
    plt.legend(custom_lines, ['J3']) 
    grid(True)
    ylabel('Extra Discharge (mAh)')    
    plot_file =   'discharge-new.png'
    savefig(plot_file)
    print("Check plot: ", plot_file)
        

# call main here
if __name__=="__main__":
    main()  