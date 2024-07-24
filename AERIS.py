import piplates.DAQC2plate as DAQC2
import piplates.POWERplate as POW
import time
#from dateutil import tz
from datetime import datetime,timedelta
import serial
import pandas as pd

site = "cao2"
print("starting AERIS data collection....")

# use scheduler to execute loop every second?
starttime = time.monotonic()

ser = serial.Serial(
        port='/dev/ttyAMA0', #Replace ttyS0 with ttyAM0 for Pi1,Pi2,Pi0
        baudrate = 9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=0.8
)
ai = [
    0.0,
    0.0,
    0.0,
    0.0,
    ]

#miss_str = ','.join(["-999"]*46)
miss_str = ["-999"]
for x in range(45):
    miss_str.append("-999")

ser.write(b'\r\n')
ser.write(b'\r\n')
ser.readline()
#ser.reset_input_buffer() 
start_time = datetime.today()
#out_file = open('/home/admin/Projects/AERIS/data/temp.dat','w')
outfile='/home/admin/Projects/AERIS/data/' + site + datetime.today().strftime('%Y%m%d%H%M%S')+'.csv'
count = 0;
to_count = 0;
bit = 0;
while(True):
    count = count+1
    #now = datetime.today().strftime('%Y,%m,%d,%H,%M,%S')
    now = datetime.today()
     #read analog inputs
    pres1 = DAQC2.getADC(0,0)
    pres2 = DAQC2.getADC(0,1)
    sol1V = DAQC2.getADC(0,2)
    sol1 = 0 if sol1V >=1 else 1
    sol2V = DAQC2.getADC(0,3)
    sol2 = 0 if sol2V >=1 else 1
    Vin = POW.getVin(0)
    #print(sol1,sol2)
    local = [str(now.year),str(now.month),str(now.day),str(now.hour),str(now.minute),str(now.second),str(pres1),str(pres2),str(sol1),str(sol2),str(Vin)]
    #print(local)
     #read AERIS data stream
    x=ser.readline().strip()
    data = x.decode("utf-8")
    data_list = data.split(',')
    if (len(data_list) > 10):
        out_string = [local + data_list]
        to_count = 0;
    else:
        to_count = to_count + 1
        out_string = [local + miss_str]
        print("warning: missing serial data stream.")
        if (to_count == 60):
            to_count = 0
            print("reset serial port...")
            ser.close
            time.sleep(1)
            ser.open
            # ser.reset_input_buffer()
    df = pd.DataFrame(out_string)
    df.to_csv(outfile,mode='a',header=False,index=False)
    if ((now - start_time) >= timedelta(hours=1)):
        start_time = datetime.today()
        outfile='/home/admin/Projects/AERIS/data/' + site + datetime.today().strftime('%Y%m%d%H%M%S')+'.csv'
    #print(now,ai)
    #data_file(now,ai,x)
    time.sleep(1.0 - ((time.monotonic() - starttime) % 1.0))
    
