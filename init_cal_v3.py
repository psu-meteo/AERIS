import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setup(38, GPIO.OUT,initial=GPIO.HIGH)
GPIO.setup(40, GPIO.OUT,initial=GPIO.HIGH)

#open cal#1 valve
print("Opening cal#1")
GPIO.output(38, False)
time.sleep(240)
#close both valves
GPIO.output(38, True)
GPIO.output(40, True)
time.sleep(2)
#open cal#2 valve
print("Opening cal#2")
GPIO.output(40, False)
time.sleep(240)
#close both valves
GPIO.output(38, True)
GPIO.output(40, True)
print("close both valves")
GPIO.cleanup()
