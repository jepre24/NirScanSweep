from time import sleep
import RPi.GPIO as GPIO


def controlStepperMotor(steps=1000, delay=0.001, direction='CW'):
	#9000 steps = 5cm, *Not precisely*, More precision required
	DIR = 12 # Pin GPIO Raspberry 
	STEP = 13 # Pin GPIO Raspberry 
	
	GPIO.setmode(GPIO.BOARD)

	GPIO.setup(DIR, GPIO.OUT)
	GPIO.setup(STEP, GPIO.OUT)

	if direction == 'CW':
		# Direction from home
		GPIO.output(DIR, GPIO.HIGH)
	elif direction == 'CCW':
		# Direction to home
		GPIO.output(DIR, GPIO.LOW)
	
	for _ in range(steps):
		# PWM signal to control motor speed
		GPIO.output(STEP, GPIO.HIGH)
		sleep(delay)
		
		GPIO.output(STEP, GPIO.LOW)
		sleep(delay)
	GPIO.cleanup()