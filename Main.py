import gpiozero
import RPi.GPIO as GPIO
from time import sleep
#import pigpio
#Module pigpio plus performant pour le contrôle des pins GPIOs! Tests à faire!

from scan import Spectrometer, NNO_FILE_REF_CAL_COEFF, NNO_FILE_SCAN_DATA
from complete_scan import init_spectrometer, complete_scan
from StepperMotor import controlStepperMotor

#Nombre de steps nécessaire pour que le moteur se déplace de 5 cm. !!Ajuster avec valeur exacte!!
cm5 = 9000

#Nombre de scans par cycle de mesures.
NbScan = 20 

#Get the last known position of the collimator.
with open('PositionStepperMotor.txt', 'r') as file:
	# get the last position of the collimator
		position = file.read()

if int(position) > 0:
	# if position of the collimator is not initial position, move back to initial position.
	controlStepperMotor(cm5*position, 0.001, 'CCW')

def open_light_source(time=300):
	light = gpiozero.DigitalOutputDevice(11)
	light.on()
	sleep(time)
	return light

def close_light_source(light):
	light.off()


# ouvre la source de lumière et attends 5 minutes pour la stabilisation.
light = open_light_source()
# initialise la communication avec le spectromètre.
spectrometer = init_spectrometer()

for i in range(NbScan):
	j= i+1
	
	# Take 20 scans at 5 cm each.
	controlStepperMotor(cm5)

	with open('PositionStepperMotor.txt', 'w') as file:
	# Write the current position of the collimator to the file
		file.write(f'{j}')

	complete_scan(spectrometer)

# Call back the step motor to home position.
controlStepperMotor(cm5*NbScan, 0.001, 'CCW')

with open('PositionStepperMotor.txt', 'w') as file:
	# Write the current position of the collimator to the file
		file.write('0')

close_light_source(light)	
