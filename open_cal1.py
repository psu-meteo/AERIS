import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setup(29, GPIO.OUT,initial=GPIO.HIGH)

#open cal#1 valve
print("Opening cal#1")
GPIO.output(29, False)

