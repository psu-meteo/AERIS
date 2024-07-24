import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setup(29, GPIO.OUT,initial=GPIO.HIGH)
GPIO.setup(31, GPIO.OUT,initial=GPIO.HIGH)

#open cal#1 valve
print("Opening cal#1")
GPIO.output(29, False)
time.sleep(240)
#close both valves
GPIO.output(29, True)
GPIO.output(31, True)
time.sleep(2)
#open cal#2 valve
print("Opening cal#2")
GPIO.output(31, False)
time.sleep(240)
#close both valves
GPIO.output(29, True)
GPIO.output(31, True)
print("close both valves")
GPIO.cleanup()
