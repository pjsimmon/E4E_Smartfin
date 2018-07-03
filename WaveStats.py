#Purisa Jasmine Simmons
#July 2, 2018
#Estimating wave statistics from IMU data.
#Version 1: Focuses on data collected from accelerometer.
#Using this paper as a guide: http://essay.utwente.nl/59198/1/scriptie_J_Kuperus.pdf

#Overview of Algorithm:
#1. Create two arrays: time_list has time offsets and acc_list has accelerations.
#2. Find local maximums and local minimums, using a threshold.
#3. Estimate wave height via double integration of acceleration between
#   a peak and the subsequent valley.
#4. Return the average wave height for that surf session. 
#5. Return the average wave frequency.  


#Data Units:
#acceleration is measured in g, 500a = 1g = -9.81m/s^2?
#velocity measured in m/s?
#distance measured in m?
#time measured in seconds

import math
import re

print('Running WaveStats Algorithm:')

#Reading data from filename_r
filename_r = "Motion_14637.txt"
read_file = open(filename_r, "r")

#File that gets written to:
write_file = open("WaveStatsOut.txt", "w")


#Need to do peak-picking before algorithm runs:
#1. Read through file, save all times:

#Reset to beginning of read file
read_file.seek(0)

#Initializations:
a0 = 0
v0 = 0
d0 = 0

counter = 0     #counts the line number
time_list = []  #list of times; t_out = current_time - prev_time 
acc_list = []   #list of estimated accelerations

with open(filename_r, 'r') as f: 
  for line in f:
    print line     #helps with debugging
    str_array = line.split(',')  #separates each line into an array on commas

    #-------Calculating Time Offset--------#
    if str_array[0] == "UTC":
      t1 = "0"
      t2 = "0"
      time_list.append(0)  #initialize time_list with 0

    else:
      t2 = str_array[0]

      if (t2 != "0" and t1 != "0"):
        time_regex = r"(\.\d+)"
        t2_val = float(re.search(time_regex, t2).group(1))
        t1_val = float(re.search(time_regex, t1).group(1))

        #print t2_val
        #print t1_val

        t_out = t2_val - t1_val #measured in secs

        #t_out is the time offset between two subsequent samples
        if (t_out < 0): 
          t_out = t_out + 1
        print t_out
      
        time_list.append(t_out)

        if (str_array[2] != "N/A" and str_array[3] != "N/A" and \
          str_array[4] != "N/A" and str_array[2] != "IMU A1"):

          ax = int(str_array[2])  #x-axis (horizontal direction 1)
          ay = int(str_array[3])  #y-axis, affected by gravity (vertical)
          az = int(str_array[4])  #z-axis (horizontal direction 2)

          g = 500            #g is the constant for gravity: 500 (measured in g?)

          #Calculate the magnitude of acceleration from all three axes:
          a_mag = math.sqrt(ax**2 + ay**2 + az**2)

          #Double integrate aA to get approximate distance b/w wave trough and crest
          aA = a_mag - g     #aA is the approximated vertical acceleration

          acc_list.append(aA)


          a_new = aA
          v_new = (a_new*t_out) + v0
          d_new = (0.5*a_new*(t_out**2)) + v_new*t_out + d0 
      
          print d_new


          #Reset all parameters for next sample, it will get added to d_new
          a0 = a_new
          v0 = v_new
          d0 = d_new

    #Reset t1 and t2 after t_out is calculated
    t1 = t2
    t2 = 0


print('Algorithm Successful.')
print "Calculated wave height: %f." % (d_new)

