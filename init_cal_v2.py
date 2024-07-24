import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setup(38, GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(40, GPIO.OUT,initial=GPIO.LOW)

#open cal#1 valve and close cal#2 valve (just in case)
print("Opening cal#1")
GPIO.output(38, True)
time.sleep(240)
#close both valves
GPIO.output(38, False)
GPIO.output(40, False)
time.sleep(2)
#open cal#2 valve and close cal#1 valve (just in case)
print("Opening cal#2")
GPIO.output(40, True)
time.sleep(240)
#close both valves
GPIO.output(38, False)
GPIO.output(40, False)
print("close both valves")
GPIO.cleanup()