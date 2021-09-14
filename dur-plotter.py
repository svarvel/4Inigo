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

# plot CDF of input array 
def cdfplot(vals):
    num = len(vals)
    y_val = np.array(range(num))/float(num)
    x_val = np.array(sorted(vals, key = float))
    curve = plot(x_val, y_val)
    return curve


def cdfplot_new(data):
    num_bins = 20
    counts, bin_edges = np.histogram (data, bins=num_bins, normed=True)
    cdf = np.cumsum (counts)
    curve = plt.plot (bin_edges[1:], cdf/cdf[-1])
    return curve



# main goes here 
def main():

    res_labels = ['detection', 'hash', 'ZKP']
    custom_lines = []

    # figures 
    fig_dur  = plt.figure()
    fig_discharge  = plt.figure()

    # results from Stan version (and that rejected submission)
    # #python plotter.py results/1572911693,results/1572904913,results/1572899317,results/1572901992  baseline,detection,hash,ZKP testing
    # S9_detection = [0.30, 0.28, 0.30, 0.31, 0.29]  
    # S9_hash = [24.113, 24.037, 24.04]
    # S9_ZKP = [176.264, 174.561, 175.256, 175.066, 177.359, 175.595]

    # # python plotter.py results/imperial-last/1573177981,results/imperial-last/1573173897,results/imperial-last/1573168968,results/imperial-last/1573182109 baseline,detection,hash,ZKP testing-J3
    # J3_detection = [0.32, 0.31, 0.37, 0.32, 0.33]  
    # J3_hash = [189.288, 190.097, 193.245, 190.926, 189.36]
    # J3_ZKP = [624.693, 627.514, 625.119, 625.182, 626.904]

    #################################################
    S9_detection = [0.30, 0.28, 0.30, 0.31, 0.29]  
    S9_hash      = [0.43, 0.42, 0.43, 0.42, 0.43]
    S9_ZKP       = [2.890, 2.889, 2.888, 2.890, 2.905]

    # python plotter.py results/imperial-last/1573177981,results/imperial-last/1573173897,results/imperial-last/1573168968,results/imperial-last/1573182109 baseline,detection,hash,ZKP testing-J3
    J3_detection = [0.32, 0.31, 0.37, 0.32, 0.33]  
    J3_hash      = [0.650, 0.622, 0.629, 0.623, 0.624]
    J3_ZKP       = [39.295, 39.356, 39.462, 39.358, 39.373, 39.412]

    # compute average and stdev [S9]
    S9_avg_dur = []
    S9_std_dur = []    
    S9_avg_dur.append(np.mean(S9_detection))
    S9_std_dur.append(np.std(S9_detection))
    S9_avg_dur.append(np.mean(S9_hash))
    S9_std_dur.append(np.std(S9_hash))
    S9_avg_dur.append(np.mean(S9_ZKP))
    S9_std_dur.append(np.std(S9_ZKP))
        
    # compute average and stdev [J3]
    J3_avg_dur = []
    J3_std_dur = []    
    J3_avg_dur.append(np.mean(J3_detection))
    J3_std_dur.append(np.std(J3_detection))
    J3_avg_dur.append(np.mean(J3_hash))
    J3_std_dur.append(np.std(J3_hash))
    J3_avg_dur.append(np.mean(J3_ZKP))
    J3_std_dur.append(np.std(J3_ZKP))
    
    # plotting
    plt.figure(fig_dur.number)
    ax = plt.gca()
    x_pos = np.arange(len(res_labels))
    ax.bar(x_pos, S9_avg_dur, width, yerr = S9_std_dur, align='center', alpha=0.8, ecolor='black', capsize=5, color = color, hatch = patterns[0])        
    #custom_lines.append(Line2D([0], [0], color = 'black', lw = 2,  marker = patterns[0]))
    custom_lines.append(patches.Rectangle((0,0),1,1,facecolor='white', edgecolor ='black', hatch = patterns[0]))
    
    ax.bar(x_pos+width, J3_avg_dur, width, yerr = J3_std_dur, align='center', alpha=0.8, ecolor='black', capsize=5, color = color, hatch = patterns[1])
    #custom_lines.append(Line2D([0], [0], color = 'black', lw = 2,  marker = patterns[1]))
    custom_lines.append(patches.Rectangle((0,0),1,1,facecolor='white',  edgecolor ='black', hatch = patterns[1]))
    
    plt.legend(custom_lines, ['S9', 'J3'])   
    ax.set_xticks(x_pos+width/2)
    ax.set_yscale('log')
    ylim([0, 100])    
    plt.yticks([0.5, 1,3,10,40,100], [0.5, 1,3,10,40,100], fontsize = 14)    
    ax.set_xticklabels(res_labels, fontsize = 14)# rotation = 30)
    grid(True)
    ylabel('Duration (sec)')
    plot_file = 'dur-comparison.png'
    savefig(plot_file)
    print("Check plot: ", plot_file)


# call main here
if __name__=="__main__":
    main()  
