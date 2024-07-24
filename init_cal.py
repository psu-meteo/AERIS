import RPi.GPIO as GPIO
import time
from datetime import datetime

site =  "cao2"

GPIO.setmode(GPIO.BOARD)
GPIO.setup(38, GPIO.OUT)
GPIO.setup(40, GPIO.OUT)
#outfile='/home/admin/Projects/AERIS/data/' + site + '_cal_log.txt'
#logfile = open(outfile,"a+")

#open cal#1 valve and close cal#2 valve (just in case)
print("Opening cal#1")
GPIO.output(38, False)
GPIO.output(40, True)
#logstring = datetime.today().strftime('%Y%m%d%H%M%S') + ",1,0"
#logfile.write(logstring)
time.sleep(240)
#close both valves
GPIO.output(38, True)
GPIO.output(40, True)
#logstring = datetime.today().strftime('%Y%m%d%H%M%S') + ",0,0"
#logfile.writelines(logstring)
time.sleep(2)
#open cal#2 valve and close cal#1 valve (just in case)
print("Opening cal#2")
GPIO.output(38, True)
GPIO.output(40, False)
#logstring = datetime.today().strftime('%Y%m%d%H%M%S') + ",0,1"
#logfile.writelines(logstring)
time.sleep(240)
#close both valves
GPIO.output(38, True)
GPIO.output(40, True)
print("close both valves")
#logstring = datetime.today().strftime('%Y%m%d%H%M%S') + ",0,0"
#logfile.writelines(logstring)
#logfile.close()