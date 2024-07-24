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
# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0, 0, width, height), outline=0, fill=0)
# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height - padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0


# Load default font.
font = ImageFont.load_default()

starttime = time.monotonic()

ser = serial.Serial(
        #port='/dev/ttyAMA0', #Replace ttyS0 with ttyAM0 for Pi1,Pi2,Pi0
        port='/dev/ttyUSB0',
        baudrate = 9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=2
)
ai = [
    0.0,
    0.0,
    0.0,
    0.0,
    ]

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

    local = [str(now.year),str(now.month),str(now.day),str(now.hour),str(now.minute),str(now.second),str(pres1),str(pres2),str(sol1),str(sol2),str(Vin)]
#     print(local)
     #read AERIS data stream
    draw.text((x, top + 0), local, font=font, fill=255)
    x=ser.readline().strip()
    data = x.decode("utf-8")
    data = 'nothing,nothing'
    data_list = data.split(',')
    #print(data)
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
        outfile='/home/admin/Projects/AERIS/data/' + site + '_' + a_Serial + '_' + datetime.today().strftime('%Y%m%d%H%M%S')+'.csv'
    #print(now,ai)
    #data_file(now,ai,x)
    #time.sleep(1.0 - ((time.monotonic() - starttime) % 1.0))
    
