import piplates.DAQC2plate as DAQC2
import piplates.POWERplate as POW
import time
#from dateutil import tz
from datetime import datetime,timedelta
import serial
import pandas as pd
import subprocess
from board import SCL, SDA
import busio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306
import sys

POW.enablePOWERSW(0)
DAQC2.enableDINint(0, 7, 'r')

site = "psu"
a_Serial = "100XYZ"
print("starting AERIS data collection....")

# Create the I2C interface for display
i2c = busio.I2C(SCL, SDA)
# Create the SSD1306 OLED class.
# The first two parameters are the pixel width and pixel height.  Change these
# to the right size for your display!
disp = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)
# Clear display.
disp.fill(0)
disp.show()
# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
image = Image.new("1", (width, height))
draw = ImageDraw.Draw(image)
# Load default font.
fnt = ImageFont.load_default()

starttime = time.monotonic()

try:
    ser = serial.Serial(
            #port='/dev/ttyAMA0', #Replace ttyS0 with ttyAM0 for Pi1,Pi2,Pi0
            port='/dev/ttyUSB0',
            baudrate = 9600,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=1.5
    )
except:
    print('no serial device.')
    draw.rectangle((0, 0, width, height), outline=0, fill=0)
    draw.text((0, 0), 'no serial device', font=fnt, fill=255)
    draw.text((0, 8), 'please connect USB', font=fnt, fill=255)
    draw.text((0, 16), 'cable to AERIS.', font=fnt, fill=255)
    disp.image(image)
    disp.show()
    sys.exit()
    
miss_str = ["-999"]
for s in range(45):
    miss_str.append("-999")

start_time = datetime.today()
outfile='/home/admin/Projects/AERIS/data/' + site + '_' + a_Serial + '_' + datetime.today().strftime('%Y%m%d%H%M%S')+'.csv'
count = 0;
to_count = 0;
bit = 0;
while(True):
    count = count+1
    now = datetime.today()
     #read analog inputs
    pres1 = DAQC2.getADC(0,0)
    pres2 = DAQC2.getADC(0,1)
    sol1V = DAQC2.getADC(0,2)
    sol1 = 0 if sol1V >=0.8 else 1
    sol2V = DAQC2.getADC(0,3)
    sol2 = 0 if sol2V >=0.8 else 1
    Vin = POW.getVin(0)
    calb = DAQC2.getDINbit(0,6)
    #print(calb)
    yy = str(now.year)
    mm = '{0:02d}'.format(now.month)
    dd = '{0:02d}'.format(now.day)
    hh = '{0:02d}'.format(now.hour)
    MM = '{0:02d}'.format(now.minute)
    ss = '{0:02d}'.format(now.second)
    p1 = str(pres1)
    p2 = str(pres2)
    s1 = str(sol1)
    s2 = str(sol2)
    sVin = str(Vin)
    
    local = [yy,mm,dd,hh,MM,ss,p1,p2,s1,s2,sVin]
    
#    print(local)
   #read AERIS data stream
    x=ser.readline().strip()

    data = x.decode("utf-8")
    data_list = data.split(',')
    #print(data_list[2])
    print(data_list)
    if (len(data_list) > 10):
        out_string = [local + data_list]
        to_count = 0;
    else:
        to_count = to_count + 1
        out_string = [local + miss_str]
        #print("warning: missing serial data stream.")
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
        outfile='/home/admin/Projects/AERIS/data/' + site + '_' + a_Serial + '_' + datetime.today().strftime('%Y%m%d%H%M%S')+'.csv'
    
    if (calb == 0):
        result = subprocess.run(["python", "init_cal_v4.py"], capture_output=False, text=True)
        print('begin cal')
    t = ':'.join([hh,MM,ss])
    s = ''.join(['  S1:',s1,' S2:',s2])
    oled1 = ' '.join([t,s])
    draw.rectangle((0, 0, width, height), outline=0, fill=0)
    draw.text((0, 0), ''.join(['Site: ',site]), font=fnt, fill=255)
    draw.text((0, 8), oled1, font=fnt, fill=255)
    draw.text((0, 16), 'C2H6: ', font=fnt, fill=255)
    #print(''.join(['Site: ',site]))
    disp.image(image)
    disp.show()
    #time.sleep(1.0 - ((time.monotonic() - starttime) % 1.0))
    
