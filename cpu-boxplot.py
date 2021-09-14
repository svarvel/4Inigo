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
bar_colors   = ['blue', light_green, 'magenta', 'black', 'purple', 'orange', 'yellow', 'pink']    # colors supported
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


# function for setting the colors of the box plots pairs
def setBoxColors(bp, c):
    #setp(bp['boxes'][0],     color = c)
    setp(bp['caps'][0],      color = c)
    setp(bp['caps'][1],      color = c)
    setp(bp['whiskers'][0],  color = c)
    setp(bp['whiskers'][1],  color = c)
    setp(bp['fliers'][0],    color = c)
    setp(bp['fliers'][1],    color = c)
    setp(bp['medians'][0],   color = 'black')
    bp['boxes'][0].set(facecolor = c )

    #setp(bp['boxes'][1],     color = c)
    setp(bp['caps'][2],      color = c)
    setp(bp['caps'][3],      color = c)
    setp(bp['whiskers'][2],  color = c)
    setp(bp['whiskers'][3],  color = c)
    #setp(bp['fliers'][2],   color = c)
    #setp(bp['fliers'][3],   color = c)
    setp(bp['medians'][1],   color = 'black')
    bp['boxes'][1].set(hatch = patterns[1])
    bp['boxes'][1].set(facecolor = c )

# main goes here 
def main():
    # old results 
    # # input data 
    # base_J3 = 'results/imperial-last/'
    # ids_J3 = ['1573173897','1573168968','1573182109']
    # base_S9 = 'results/'
    # #ids_S9 = ['1572904913',  '1572899317', '1572901992']
    # ids_S9 = ['1572911693','1573540798','1573544436']
    # #1573537160
    

    # input data 
    base_J3 = 'results-resubmit/'
    ids_J3 = ['1573173897','1586389516','1586389521']
    base_S9 = 'results-resubmit/'
    ids_S9 = ['1572911693','1586384948', '1586385213']    


    res_labels = ['detection','hash','ZKP']
    custom_lines = []
    custom_lines.append(patches.Rectangle((0,0),1,1,facecolor='white', edgecolor ='black', hatch = patterns[0]))
    custom_lines.append(patches.Rectangle((0,0),1,1,facecolor='white', edgecolor ='black', hatch = patterns[1]))

    # iterate on J3
    J3 = []
    for id in ids_J3: 
        # quick input check 
        res_folder = base_J3 + id        
        if not os.path.isdir(res_folder):
            print("Something is wrong. Folder %s is missing" %(res_folder))
            return 

        # work on cpu log
        log_file = res_folder + '/cpu.log'
        if not os.path.isfile(log_file):
            print("Something is wrong. CPU log file %s is missing" %(log_file))
        else:
            # load file
            with open(log_file) as f: 
                lines = f.readlines()
            
            # parse file 
            cpu_times = []
            cpu_vals = []    
            for line in lines: 
                fields = line.split('\t')
                val = float(fields[0])
                cpu_times.append(val)
                val = fields[1].split(' ')[0].replace('%',  '')
                cpu_vals.append(float(val))

            J3.append(cpu_vals)

    # iterate on S9
    S9 = []
    for id in ids_S9: 
        # quick input check 
        res_folder = base_S9 + id        
        if not os.path.isdir(res_folder):
            print("Something is wrong. Folder %s is missing" %(res_folder))
            return 

        # work on cpu log
        log_file = res_folder + '/cpu.log'
        if not os.path.isfile(log_file):
            print("Something is wrong. CPU log file %s is missing" %(log_file))
        else:
            # load file
            with open(log_file) as f: 
                lines = f.readlines()
            
            # parse file 
            cpu_times = []
            cpu_vals = []    
            for line in lines: 
                fields = line.split('\t')
                cpu_times.append(float(fields[0]))
                val = float(fields[1].split(' ')[0].replace('%',  ''))
                if id == '1572911693' and val > 40: 
                    print("skipping", val)
                    continue                
                cpu_vals.append(val)

            S9.append(cpu_vals)

    # plot 
    fig = figure()
    ax = axes()
    plt.legend(custom_lines, ['S9', 'J3']) 

    # first boxplot pair
    bp = boxplot([S9[0], J3[0]], positions = [1, 2], widths = 0.9, patch_artist=True)
    setBoxColors(bp, color[0])

    # second boxplot pair
    bp = boxplot([S9[1], J3[1]], positions = [4, 5], widths = 0.9, patch_artist=True)
    setBoxColors(bp, color[1])

    # third boxplot pair
    bp = boxplot([S9[2], J3[2]], positions = [7, 8], widths = 0.9, patch_artist=True)
    setBoxColors(bp, color[2])

    # labels 
    plt.xticks([1.5, 4.5, 7.5], res_labels,  fontsize = 14)# rotation = 30)
    ylabel('CPU Utilization (%)')

    plot_file =  'boxplot-cpu-com.png'
#    plt.legend(loc = 'upper right')
    savefig(plot_file)
    print("Check plot: ", plot_file)

    
# call main here
if __name__=="__main__":
    main()  