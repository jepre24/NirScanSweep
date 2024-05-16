import gpiozero
import RPi.GPIO as GPIO
from time import sleep

from scan import Spectrometer, NNO_FILE_REF_CAL_COEFF, NNO_FILE_SCAN_DATA
#from complete_scan import init_spectrometer, complete_scan


def open_light_source(time=100):
	light = gpiozero.DigitalOutputDevice(11)
	light.on()
	sleep(time)
	return light
	
light = open_light_source()
close_light_source(light)
scscsc
def close_light_source(light):
	light.off()

def control_stepper(steps=1000, delay=0.001, direction='CW'):
	#9000 = 5cm
	DIR = 31
	STEP = 29
	
	GPIO.setmode(GPIO.BOARD)

	GPIO.setup(DIR, GPIO.OUT)
	GPIO.setup(STEP, GPIO.OUT)

	if direction == 'CW':
		GPIO.output(DIR, GPIO.HIGH)
	elif direction == 'CCW':
		GPIO.output(DIR, GPIO.LOW)
	
	for _ in range(steps):
		GPIO.output(STEP, GPIO.HIGH)
		sleep(delay)
		
		GPIO.output(STEP, GPIO.LOW)
		sleep(delay)
	GPIO.cleanup()

	
light = open_light_source()
spectrometer = init_spectrometer()
for i in range(20):
	control_stepper(9000)
	complete_scan(spectrometer)

#Comeback
control_stepper(180000, 0.001, 'CCW')

close_light_source(light)	



#spectrometer = Spectrometer(0x0451, 0x4200)
