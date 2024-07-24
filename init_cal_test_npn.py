import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setup(29, GPIO.OUT,initial=GPIO.HIGH)
GPIO.setup(31, GPIO.OUT,initial=GPIO.HIGH)

#open cal#1 valve and close cal#2 valve (just in case)
print("Opening cal#1")
GPIO.output(29, False)
time.sleep(5)
GPIO.output(29, True)
GPIO.output(31, True)
time.sleep(1)
print("opening cal#2")
GPIO.output(31, False)
time.sleep(5)
GPIO.output(29, True)
GPIO.output(31, True)
GPIO.cleanup()
