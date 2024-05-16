#This code needs to run with spectrum_library which require python 32bit

from spectrum_library import scan_interpret
import json
import matplotlib.pyplot as plt
import os

def read_files_in_directory(directory='data'):
    #Funciton to read the txt files of spectrometer scan
    for filename in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, filename)):
            with open(os.path.join(directory, filename), 'r') as file:
                print(f"Reading file: {filename}")
                raw_data = file.read().replace('\n', '')
            # Split the string into a list of strings, then convert each string to an integer
            data = scan_interpret(list(map(int, raw_data.strip('[]').split(','))))
            data_dict = json.loads(data)

            #Choose the saving name
            print("Enter JSON save prefix")
            jsonFile = open("json/{}_{}.JSON".format('test', filename), "w")
            jsonFile.write(data)

            plt.plot(data_dict["wavelength"][0:data_dict["length"]], data_dict["intensity"][0:data_dict["length"]])
            plt.title(f'{filename}')
            plt.ylabel('Intensity')
            plt.xlabel('Wavelength / nm')
            plt.show()

# Usage:
read_files_in_directory('data')



