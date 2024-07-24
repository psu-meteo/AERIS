import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setup(29, GPIO.OUT,initial=GPIO.HIGH)
GPIO.setup(31, GPIO.OUT,initial=GPIO.HIGH)

#close both valves
print("Close both valves.")
GPIO.output(29, True)
GPIO.output(31, True)
GPIO.cleanup()
