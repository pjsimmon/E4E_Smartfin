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
#acceleration is measured in g, 500a = 1g = -9.81m/s^2
#velocity measured in m/s
#distance measured in m
#time measured in seconds

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
time_list = []  #list of time offsets; t_out = current_time - prev_time 
acc_list = []   #list of estimated accelerations

with open(filename_r, 'r') as f: 
  for line in f:
    #print line     #helps with debugging
    str_array = line.split(',')  #separates each line into an array on commas

    #-------Calculating Time Offset--------#
    if str_array[0] == "UTC":
      t1 = 0
      t2 = 0
      time_list.append(0)  #initialize time_list with 0

    else:
      t2 = str_array[0]

      if (t2 != 0 and t1 != 0 and str_array[2] != "N/A"):
        time_regex = r"(\.\d+)" #regex to get the part of time that we care about
        t2_val = float(re.search(time_regex, t2).group(1))
        t1_val = float(re.search(time_regex, t1).group(1))

        #print t2_val
        #print t1_val

        t_out = t2_val - t1_val #measured in secs

        #t_out is the time offset between two subsequent samples
        if (t_out < 0): 
          t_out = t_out + 1
        #print t_out
      
        time_list.append(t_out)
        print("Time offset is: %f") % t_out

      if (str_array[2] != "N/A" and str_array[3] != "N/A" and \
        str_array[4] != "N/A" and str_array[2] != "IMU A1"):


        #Scale raw to get correct units in m/s^2
        g_const = 512            #g is the constant for gravity: 500 (measured in g?)
        gravity = -9.80665

        ax = float(str_array[2])  #x-axis (horizontal direction 1)
        ax = (ax/g_const)*gravity
        ay = float(str_array[3])  #y-axis, affected by gravity (vertical)
        ay = (ay/g_const)*gravity
        az = float(str_array[4])  #z-axis (horizontal direction 2)
        az = (az/g_const)*gravity

        print("ax: %f") % ax 
        print("ay: %f") % ay
        print("az: %f") % az 


        #Calculate the magnitude of acceleration from all three axes:
        a_mag = math.sqrt(ax**2 + ay**2 + az**2)

        print("Acceleration a_mag is: %f") % a_mag

        #Double integrate aA to get approximate distance b/w wave trough and crest
        aA = a_mag + gravity #aA is the approximated vertical acceleration

        print("Acceleration aA is: %f") % aA

        acc_list.append(aA)


    #Reset t1 and t2 after t_out is calculated
    t1 = t2
    t2 = 0

#----------Here, after both lists created----------
#Now, calculate wave heights between peaks and valleys.

if len(time_list) != len(acc_list):
  print("Error: Lengths of time_list and acc_list don't match!")
  #print len(time_list)
  #print len(acc_list)

else:
  #Initializations:
  a0 = 0
  v0 = 0
  d0 = 0

  i = 2            #start initialization at 2
  minNotFound = 1  #boolean
  numWaves = 0
  waveHeight = 0
  waveFreq = 0
  total_WH = 0
  total_WF = 0

  max_wi = 0  #index of local max wavepoint
  min_wi = 0  #index of local min wavepoint

  wave_pi = 0 #time of wave period
  total_wave_pi = 0

  #-------Setting the threshold------------
  threshold = 0.05  #not sure yet what to initalize threshold to

  end = len(acc_list)

  while(i < (end - 3)):
    a_prev2 = float(acc_list[i-2])
    a_prev1 = float(acc_list[i-1])
    a_this = float(acc_list[i])
    a_next1 = float(acc_list[i+1])
    a_next2 = float(acc_list[i+2])

    #Check if a_this is a max point
    if (a_prev1 > a_prev2 + threshold and a_this > a_prev1 + threshold \
      and a_next1 > a_this + threshold and a_next2 > a_this + threshold):

      max_wi = i
 
      #Do calculations until a new min is found 
      while (minNotFound and i < (end - 3)):
        t = time_list[i]
        #t = t_out
        a_new = acc_list[i] 
        v_new = (a_new*t) + v0
        d_new = (0.5*a_new*(t**2)) + v_new*t + d0 
    
        wave_pi = time_list[i+1] + wave_pi    
 
        #print "Looking for a min" 
        #print a_prev2
        #print a_prev1
        #print a_this
        #print a_next1
        #print a_next2

        #Check for next min point
        if (a_prev1 <  a_prev2 - threshold and a_this < a_prev1 - threshold \
          and a_this < a_next1 - threshold and a_next1 < a_next2 - threshold):

          print("Found a new min")

          minNotFound = 0  #min point has been found at acc_list[i]
          min_wi = i

          t = time_list[i]
          #t = t_out
          a_new = acc_list[i] 
          v_new = (a_new*t_out) + v0
          d_new = (0.5*a_new*(t**2)) + v_new*t + d0 
          wave_pi = time_list[i] + wave_pi    

          #Don't count heights greater than 20m (unreasonable)
          # or periods greater than 30s
          if (abs(d_new) < 20 and 2*wave_pi < 30):
            numWaves = numWaves + 1
            waveHeight = abs(d_new)
            total_WH = total_WH + waveHeight

            if (wave_pi != 0):
              wave_pi = 2*wave_pi
              waveFreq = 1/(wave_pi) 
              total_wave_pi = total_wave_pi + 2*wave_pi
              print "The wave height is %f, wave frequency is %f, period: %f." \
                % (waveHeight, waveFreq, wave_pi)
              total_WF = total_WF + waveFreq

        #Set all parameters for next sample (same wave)
        a0 = a_new
        v0 = v_new
        d0 = d_new

        i = i + 1 #Increment i for while(minNotFound) loop
        a_prev2 = float(acc_list[i-2])
        a_prev1 = float(acc_list[i-1])
        a_this = float(acc_list[i])
        a_next1 = float(acc_list[i+1])
        a_next2 = float(acc_list[i+2])

    #Reset after every max point - calculating new wave height and frequency:
    a0 = 0
    v0 = 0
    d0 = 0

    minNotFound = 1
    waveHeight = 0
    waveFreq = 0

    max_wi = 0  #index of local max wavepoint
    min_wi = 0  #index of local min wavepoint
    wave_pi = 0 #time of wave period

    i = i + 1   #Increment i for while(i < end) loop

  #At the end of the .CSV data file, return results:
  if numWaves == 0:
    print("Error! numWaves = 0")
  else:
    avg_WH_m = total_WH/numWaves
    avg_WP = total_wave_pi/numWaves
    avg_WF = total_WF/numWaves
    #print ("avg_WP: %f")%avg_WP
    #print ("avg_WF: %f")%avg_WF
    #print ("1/avg_WP = avg_WF?: %f ?= %f")%(1/avg_WP, avg_WF)

    #if (avg_WP == 0):
    #  avg_WF = avg_WF
    #else:
    #  avg_WF = 1/avg_WP

    total_time_secs = sum(time_list)
    total_time_mins= total_time_secs/60 

    print "\n" 
    print "Algorithm Successful."
    print "Using a threshold of %f:" % threshold 
    print "The total number of waves measured this session was: %d." % numWaves
    print "The total time for this session was: %f secs (or %f mins)." \
      %(total_time_secs, total_time_mins)
    print "Calculated Average Wave Height as: %f m." % avg_WH_m 
    print "Calculated Average Wave Period as: %f s." % avg_WP 
    print "Calculated Average Wave Frequency as: %f Hz." % (1/avg_WP) 
    #print "Calculated Average Wave Frequency as: %f Hz." % avg_WF

