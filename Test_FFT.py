import matplotlib.pyplot as plt
import numpy as np

Fs = 150.0;  # sampling rate     (number of samples per second)
Ts = 1.0/Fs; # sampling interval (time between successive samples) 
t = np.arange(0,1,Ts) # time vector

ff = 1.0;   # frequency of the signal
y = np.sin(2*np.pi*ff*t)

n = len(y) # length of the signal
k = np.arange(n)
T = n/Fs
frq = k/T # two sides frequency range
frq = frq[range(n/2)] # one side frequency range

Y = np.fft.fft(y)/n # fft computing and normalization
Y = Y[range(n/2)]


fig, ax = plt.subplots(3, 1)
ax[0].plot(t,y)
ax[0].set_xlabel('Time')
ax[0].set_ylabel('Amplitude')
ax[1].plot(frq,abs(Y),'r') # plotting the spectrum
ax[1].set_xlabel('Freq (Hz)')
ax[1].set_ylabel('|Y(freq)|')
ax[1].set_xlim(0,1)


plt.show()
