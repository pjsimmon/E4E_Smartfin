#Purisa Jasmine Simmons
#July 6, 2018
#An algorithm for generating a Power Spectral Density Plot from 
#accelerometer data.

#Overview of Algorithm:
#1.
#Returns the Power Spectral Density Plot

#Data Units:
#acceleration is measured in g, 500a = 1g = -9.81m/s^2?
#time measured in seconds

import numpy as np
from scipy import signal
import matplotlib.pyplot as plt

#from plotly import tools
#import plotly.offline
#import plotly.graph_objs as go

import math
import re

#Need to do peak-picking before algorithm runs:
#1. Read through file, save all times and accelerations:
print('Running WaveStats Algorithm:')

#Reading data from filename_r
filename_r = "Motion_14644.CSV"
read_file = open(filename_r, "r")

#File that gets written to:
write_file = open("WaveStatsOut.txt", "w")

#Initialize lists
t1 = 0 
t2 = 0
time_list = []  #list of ***elapsed*** times
acc_list = []   #list of estimated accelerations

print 'Extracting data from file...'
with open(filename_r, 'r') as f: 
  for line in f:
    str_array = line.split(',')  #separates each line into an array on commas

    #-------Calculating Time Offset--------#
    if str_array[0] == "UTC":
      t1 = 0
      t2 = 0
      time_list.append(0)  #initialize time_list with 0

    else:
      t2 = str_array[0]

      if (t2 != 0 and t1 != 0 and str_array[2] != "N/A"):
        time_regex = r"(\.\d+)"
        t2_val = float(re.search(time_regex, t2).group(1))
        t1_val = float(re.search(time_regex, t1).group(1))

        #print t2_val
        #print t1_val

        t_out = t2_val - t1_val #measured in secs

        #t_out is the time offset between two subsequent samples
        if (t_out < 0): 
          t_out = t_out + 1
     
        last = len(time_list) - 1
        last_time = time_list[last] 
        new_time = t_out + last_time
        time_list.append(new_time)

      if (str_array[2] != "N/A" and str_array[3] != "N/A" and \
        str_array[4] != "N/A" and str_array[2] != "IMU A1"):

        g_const = 512     #g_const is scaling constant: 500 (500raw units = 1g)
        gravity = 9.80665 #gravity is the constant 9.80665m^2/s 

        ax = int(str_array[2])  #x-axis (horizontal direction 1)
        ax = (ax/g_const)*gravity
        ay = int(str_array[3])  #y-axis, affected by gravity (vertical)
        ay = (ay/g_const)*gravity
        az = int(str_array[4])  #z-axis (horizontal direction 2)
        az = (az/g_const)*gravity


        #Calculate the magnitude of acceleration from all three axes:
        a_mag = math.sqrt(ax**2 + ay**2 + az**2)

        #Double integrate aA to get approximate distance b/w wave trough and crest
        aA = a_mag - gravity     #aA is the approximated vertical acceleration

        acc_list.append(aA)


    #Reset t1 and t2 after t_out is calculated
    t1 = t2
    t2 = 0

#----------Here, after both lists created----------

time_array = np.array(time_list)
acc_array = np.array(acc_list)

#plt.plot(time_array, acc_array)
#plt.show()

#Need to remove the scaling factor of 500 to get more correct units for 
#Energy in m^2/Hz.

print 'Finished computing the time_offset array.'
print 'Finished computing the acc array.'

print 'Algorithm Successful.'
x = acc_array

##-----Version 1, scaling units wrong (10^3)------

#f, Pxx_den = signal.periodogram(x)
#plt.semilogy(f, Pxx_den)
#plt.xlabel('Frequency [Hz]')
#plt.ylabel('Energy [m^2Hz]')
#plt.show()

##---------Version 2, wrong axes titles, scaling off by 15------best

dt = 0.01
#plt.plot(time_array,acc_array)
plt.psd(x=acc_array)
plt.title(filename_r)
plt.xlabel('Frequency [Hz]')
plt.ylabel('Energy [m^2/Hz]')
plt.show()

##------Version 3, not working?-----

#trace1 = go.Scatter(x=time_array, y=acc_array)
#trace2 = go.Scatter(x=f, y=Pxx_den)

#fig = tools.make_subplots(rows=2, cols=1)
#fig.append_trace(trace1, 2, 1)
#fig.append_trace(trace2, 1, 1)
#fig['layout'].update(height=600, width=600, title='Stacked subplots')
#plotly.offline.plot(fig, filename='stacked-subplots')


