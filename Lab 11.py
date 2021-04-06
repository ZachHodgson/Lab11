# RASPBERRY PI TEMPLATE
import matplotlib.pyplot as plt
import numpy as np
import serial
from time import *

ser = serial.Serial('COM5', 9600)
ser.flush()
#0.176 degrees per step for 28byj-48 motor
qi = input("Initial position= ")
qi = float(qi)
qf = input("Final position= ")
qf = float(qf)
tf = input("Time trajectory up to 20 seconds= ")
tf = float(tf)
res = input("Stepper Resolution= ")
res = float(res)
a0 = qi
a1 = 0
a2 = 3*(qf-qi)/(tf**2)
a3 = -2*(qf - qi)/(tf**3)
Ts = 0.01
Ns = tf/Ts
Ns=int(Ns)
q = np.zeros(Ns)
dq = np.zeros(Ns)
ddq = np.zeros(Ns)
time_sec = np.zeros(Ns)
dat = np.zeros(Ns)
t = 0

for k in range(0,Ns):
    q[k] = a0 + a1*t + a2*t**2 + a3*t**3
    dq[k] = 2*a2*t + 3*a3*t**2
    ddq[k] = 2*a2 + 6*a3*t
    time_sec[k] = k*Ts
    t = t + Ts


for j in range(0,Ns):
    pulse = dq[j]/res #theta/sec divided by theta/pulse = pulse/sec = frequency
    if(pulse == 0):
        pulse = 0
    else:
        pulse = 1/pulse #pulse period = sec/pulse : how long between shift register
    dat[j] = pulse/0.0001


for l in range(0,Ns):
    ser.write(str(dat).encode('utf-8'))
    ser.write(str('\n').encode('utf-8'))
    ser.flush()
    sleep(.05)
    ser.flush()

plt.plot(time_sec,q,'r')
plt.plot(time_sec,dq,'b')
plt.plot(time_sec,ddq,'k')
plt.ylabel('q(t)')
plt.xlabel('t')
plt.show()