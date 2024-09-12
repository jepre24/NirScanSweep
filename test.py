with open('PositionStepperMotor.txt', 'w') as file:
# Write a string to the file
	for i in range(20):
		# Take 20 scans at each 5 cm.
		print("Moteur")

		file.write(f'{i}\n')
		print(f'scan: {i}')
		if i == 15:
			break
		print('Scan')