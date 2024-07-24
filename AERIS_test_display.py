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

site = "cao2"
a_Serial = "100778"
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

#miss_str = ','.join(["-999"]*46)
miss_str = ["-999"]
for s in range(45):
    miss_str.append("-999")

#ser.write(b'\r\n')
#ser.write(b'\r\n')
#ser.readline()
#ser.reset_input_buffer() 
start_time = datetime.today()
#out_file = open('/home/admin/Projects/AERIS/data/temp.dat','w')
outfile='/home/admin/Projects/AERIS/data/' + site + '_' + a_Serial + '_' + datetime.today().strftime('%Y%m%d%H%M%S')+'.csv'
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
    sol1 = 0 if sol1V >=0.8 else 1
    sol2V = DAQC2.getADC(0,3)
    sol2 = 0 if sol2V >=0.8 else 1
    Vin = POW.getVin(0)
    
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
    #print(local)
     #read AERIS data stream
 
    #draw.rectangle((0, 0, width, height), outline=0, fill=0)
    #d.multiline_text((10, 10), "Hello\nWorld", font=fnt, fill=(0, 0, 0))
    t = ':'.join([hh,MM,ss])
    s = ''.join(['  S1:',s1,' S2:',s2])
    oled1 = ' '.join([t,s])
    draw.rectangle((0, 0, width, height), outline=0, fill=0)
    draw.text((0, 0), oled1, font=fnt, fill=255)
    draw.text((0, 12), 'C2H6: ', font=fnt, fill=255)
    #print(s)
    disp.image(image)
    disp.show()
    
    #x=ser.readline().strip()
    #data = x.decode("utf-8")
    time.sleep(0.1)
    
