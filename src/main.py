#!/usr/bin/env python3
import time
import serial
from pdb import set_trace as st

ser = serial.Serial(
        port='/dev/ttyS0',
        baudrate = 57600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=10
)

#ser.write(b"STOP;")
#time.sleep(1)

ser.write(b"RESET;")
time.sleep(0.5)

ser.write(b"FORMAT=D;")
time.sleep(0.5)

ser.write(b"CHANNEL=1;")
time.sleep(0.5)

ser.write(b"SAMPLERATE=160;")
time.sleep(0.5)

ser.write(b"START;")
#time.sleep(0.1)

index=0
data_list = []
while(True):
    #ser.write(b"START;")
    x=str(ser.read(1350))
    if index <= 2:
       index += 1
       continue
    
    #if index == 0:
    #   x_ = x.split('\\n')[15].split(',')
    #   #x_segmentation[15].split(',')
    #   for i in range(len(x_)):
    #       if ' ' in x_[i] or i == 1:
    #          continue
    #       if int(x_[i]) == 1:
    #          
    #          try:
    #             data_list.append(int(x_[i+2]))
    #          except:
    #             continue
    else:
       len_list = len(data_list)
       x_ = x.replace("b","").replace("'","").split(',')
       for i in range(len(x_)):
           if ' 'in x_[i] or len(x_[i])==0:
              continue
           try:
               if int(x_[i]) == 1:
                  data_list.append(int(x_[i+2]))
           except:
                  continue
       index += 1
       print(len(data_list)-len_list)
       #st()
    #index += 1
    #print(x)
