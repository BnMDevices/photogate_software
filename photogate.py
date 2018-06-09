'''
Created on Dec 26, 2016

@author: dabarne
'''
import math
from time import sleep, time
import spidev

spi=spidev.SpiDev()
spi.open(0,0)
light_channel=1
sleep_time=0.05

def light(ch):
    raw=spi.xfer([1,(8+ch)<<4,0])
    data=((raw[1]&3)<<8)+raw[2]
    return data

def speed(Time, length):
    v=length/Time
    return v

def get_baseline(T,light_channel,sleep_time):
    #T is the time frame you would want the baseline
    #light channel is the ADC's channel that you are using
    A=[]
    x=0.0
    N=T/0.1
    for i in range(0,int(N)):
        y=float(light(light_channel))
        A.append(y)
        x=x+y
        sleep(sleep_time)
    avg=x/float(N)
    var=0.0
    for k in range(0,len(A)):
        y=(A[k]-avg)**2
        var=var+y
    std=math.sqrt(var)
    #returns a list of avg +/- std
    return [avg,std]

T=int(raw_input("How long would you like the baseline for? "))
avg_std=get_baseline(T,light_channel,sleep_time)
avg=avg_std[0]
std=avg_std[1]
print("Baseline established")
#print("Baseline established: "+str(avg)+"+/-"+str(std))

while True:
    data=float(light(light_channel))
    t=time()
    if data<avg-3*std:
        time_start=t
        sleep(sleep_time)
        while data<avg-3*std:
            data=float(light(light_channel))
            time_end=time()
            #print(str(data))
        del_t=time_end-time_start
        print("Time Duration: "+str(del_t))
    else:
        sleep(sleep_time)