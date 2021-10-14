import time
from influxdb import InfluxDBClient
import datetime
import pytz
import serial
import subprocess
from pdb import set_trace as st
import warnings
warnings.filterwarnings("ignore")

# InfluxDB configuration
write_batch_size = 5000
host = 'sensorweb.us'
un = 'admin'
pw = 'sensorweb128'
#host = 'homedots.us'
#un = 'test'
#pw = 'HomeDots'
#db = 'newdevice'
db = 'shake'
sname = 'Z'
tag = {'board':'greenboard'}

#timez = 'America/New_York'
timez = 'UTC'
time_zone = pytz.timezone(timez)

# s_time = str(int(ct.timestamp()*1000*1000000))


# This function write an array of data to influxdb. It assumes the sample interval is 1/fs.
# influx - the InfluxDB info including ip, db, user, pass. Example influx = {'ip': 'https://sensorweb.us', 'db': 'algtest', 'user':'test', 'passw':'sensorweb'}
# dataname - the dataname such as temperature, heartrate, etc
# timestamp - the epoch time (in second) of the first element in the data array, such as datetime.now().timestamp()
# fs - the sampling interval of readings in data
# unit - the unit location name tag
def write_influx(influx, unit, table_name, data_name, data, start_timestamp, fs):
    # print("epoch time:", timestamp)
    max_size = 100
    count = 0
    total = len(data)
    prefix_post  = "curl -s -POST \'"+ influx['ip']+":8086/write?db="+influx['db']+"\' -u "+ influx['user']+":"+ influx['passw']+" --data-binary \' "
    http_post = prefix_post
    for value in data:
        count += 1
        http_post += "\n" + table_name +",location=" + unit + " "
        http_post += data_name + "=" + str(value) + " " + str(int(start_timestamp*10e8))
        start_timestamp +=  1/fs
        if(count >= max_size):
            http_post += "\'  &"
            # print(http_post)
            print("Write to influx: ", table_name, data_name, count)
            subprocess.call(http_post, shell=True)
            total = total - count
            count = 0
            http_post = prefix_post
    if count != 0:
        http_post += "\'  &"
        # print(http_post)
        print("Write to influx: ", table_name, data_name, count, data)
        subprocess.call(http_post, shell=True)






# dClient = InfluxDBClient(host=host,
#                             port=8086,
#                             username=un,
#                             password=pw,
#                             database=db,
#                             ssl=True)
dest = {'ip':'https://sensorweb.us', 'db':'shake', 'user':'admin', 'passw':'sensorweb128'}



sample_rate = 1 / 80
time_interval = sample_rate * 1000 # in milisecond


ser = serial.Serial(
        port='/dev/ttyS0',
        # port='/dev/ttyAMA0',
        baudrate = 57600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=10
)

#ser.write(b"STOP;")
#time.sleep(1)

# ser.write(b"RESET;")
# time.sleep(0.5)
#
ser.write(b"FORMAT=D;")
time.sleep(0.5)
#
# ser.write(b"CHANNEL=1;")
# time.sleep(0.5)
#
ser.write(b"SAMPLERATE=80;")
time.sleep(0.5)
#
ser.write(b"START;")
# time.sleep(0.5)



index=0
print(str(ser.read(1000)))
st()

while(ser.isOpen()):
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

       ### write every point

   ### write use write_influx
    current_time_stamp = datetime.datetime.now(pytz.UTC)
    write_influx(dest, 'greenboard', 'Z', 'value', data_list, current_time_stamp, fs=80)
    # for point in data_list:





      #
      #  ### write into json
      #  data = []
      #  current_time_stamp = datetime.datetime.now(pytz.UTC)
      #  for point in data_list:
      # # i = 0
      #    current_time_stamp += datetime.timedelta(milliseconds=time_interval)
      #    #current_time_stamp = datetime.datetime.now(pytz.UTC)
      #    write_time = current_time_stamp.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
      #
      #    data.append(
      #    {
      #       "measurement": sname,
      #       "tags" : tag,
      #       "fields" : {
      #          "value": float(point)
      #       },
      #       "time": write_time
      #      }
      #    )
      #
      #  dClient.write_points(data, database = db, time_precision = 'ms', batch_size = write_batch_size, protocol = 'json')
