#Purisa Jasmine Simmons
#July 2, 2018
#Estimating wave statistics from IMU data.
#Version 1: Focuses on data collected from accelerometer.
#Using this paper as a guide: http://essay.utwente.nl/59198/1/scriptie_J_Kuperus.pdf


import math


print('Running WaveStats Algorithm:')

#Reading data from filename_r
filename_r = "Motion_14637.txt"
read_file = open(filename_r, "r")

#File that gets written to:
write_file = open("WaveStatsOut.txt", "w")


with open(filename_r, 'r') as f: 
  for line in f:
    print line     #helps with debugging
    str_array = line.split(',')  #separates each line into an array on commas

    if (str_array[2] != "N/A" and str_array[3] != "N/A" and str_array[4] != "N/A" and str_array[2] != "IMU A1"):
      ax = int(str_array[2])  #x-axis (horizontal direction 1)
      ay = int(str_array[3])  #y-axis, affected by gravity (vertical)
      az = int(str_array[4])  #z-axis (horizontal direction 2)

      g = 500            #g is the constant for gravity: 500
      #t_offset = ??      #t_offset is the time offset between the readings

      #Calculate the magnitude of acceleration from all three axes:
      a_mag = math.sqrt(ax**2 + ay**2 + az**2)

      #Double integrate aA to get approximate distance b/w wave trough and crest
      aA = a_mag - g     #aA is the approximated vertical acceleration
      #d_t = (0.5)*aA*(t_offset**2) #the double integral of aA
  
      




print('Algorithm Successful.')


