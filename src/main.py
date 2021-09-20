import time
from influxdb import InfluxDBClient
import datetime
import pytz
import serial
from pdb import set_trace as st
import warnings
warnings.filterwarnings("ignore")

# InfluxDB configuration
write_batch_size = 5000
host = 'sensorweb.us'
un = 'admin'
pw = 'sensorweb128'
db = 'newdevice'
sname = 'Z'
tag = {'board':'greenboard'}

#timez = 'America/New_York'
timez = 'UTC'
time_zone = pytz.timezone(timez)

# s_time = str(int(ct.timestamp()*1000*1000000))

dClient = InfluxDBClient(host=host,
                            port=8086,
                            username=un,
                            password=pw,
                            database=db,
                            ssl=True)

sample_rate = 1 / 160
time_interval = sample_rate * 1000 # in milisecond


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

while(True):
    data_list = []
    #ser.write(b"START;")
    x=str(ser.read(1350))
    if index <= 2:
       index += 1
       continue

    else:
       if index == 3:
         # current time
         ct = datetime.datetime.now(pytz.UTC)
         #ct = time_zone.localize(ct)
         current_time_stamp = ct
       # len_list = len(data_list)
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


       data = []
       #st()
       for point in data_list:
      # i = 0
         current_time_stamp += datetime.timedelta(milliseconds=time_interval)
         write_time = current_time_stamp.strftime('%Y-%m-%dT%H:%M:%S.%fZ')

         data.append(
         {
            "measurement": sname,
            "tags" : tag,
            "fields" : {
               "value": point
            },
            "time": write_time
           }
         )
       #print(data)
       #print(f'Uploaded')
       dClient.write_points(data, database = db, time_precision = 'ms', batch_size = write_batch_size, protocol = 'json')
