#Jasmine Simmons
#June 2018

#Estimating GPU location from IMU data

#IMU Motion Data Format:
#UTC, Time, IMU A1, IMU A2, IMU A3, IMU G1, IMU G2, IMU G3, 
# IMU M1, IMU M2, IMU M3, Latitude, Longitude

#Sample data:
#2018-06-25T14:37:02.5420+00:00,3191756172,-204,218,125,-1012,77,17,321,137,85,
#N/A,N/A

import re

print('Running DeadReckoning Algorithm:')


#abcd is the file to be read
filename_r = "Motion_14637.txt"

read_file = open(filename_r, "r")

#deadout_r.txt is the file that gets written to
write_file = open("deadout_r.txt", "w")


#Open a file name and read each line to strip \n newline chars

with open(filename_r, 'r') as f:
  for line in f:
    print line                #helps with debugging
    str_array = line.split(',')  #separates each line into an array on commas

    #print str_array
    #print str_array[0]
    #print str_array[1]

    if str_array[0] == "UTC":
      t1 = "0"
      t2 = "0"

    else: 
      t2 = str_array[0]
 
      print t1
      print t2

      #subtract t2 - t1 to get time difference
      if (t2 != "0" and t1 != "0"):
        time_regex = r"(\.\d+)"
        t2_val = float(re.search(time_regex, t2).group(1))
        t1_val = float(re.search(time_regex, t1).group(1)) 

        #print t2_val
        #print t1_val

        t_out = t2_val - t1_val
      
        if (t_out < 0):
          t_out = t_out + 1

        #print t_out

    #Reset t1 and t2 at end of loop
    t1 = t2
    t2 = 0


print('Algorithm Successful.')




