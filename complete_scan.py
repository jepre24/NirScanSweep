from scan import Spectrometer, NNO_FILE_REF_CAL_COEFF, NNO_FILE_SCAN_DATA
import hid
from os import walk
import sys

def init_spectrometer():
# Try to open the device, otherwise read in file data
    h = hid.device()
    device_open = True
    
    try:
        print('Opening Device')
        h = Spectrometer(0x0451, 0x4200)
          # NIRScan Nano VendorID/ProductID

    except IOError as ex:
        print(ex)
        print("Looks like the NIRScan Nano isn't connected")
        print("Opening the .dat file instead")
        device_open = False
    return h, device_open
    
def complete_scan(h):    
    if device_open:
        # disable non-blocking mode, makes life easier, sacrifices speed
        #h.set_nonblocking(0)

        # Do scan
        h.perform_scan()
        
        # Get scan data
        scan_data = h.get_file(NNO_FILE_SCAN_DATA)
        print(scan_data)
        # Get calibration data
        reference_data = spectrometer.get_file(NNO_FILE_REF_CAL_COEFF)
        

        # combine the data and save the data file (readable by the GUI program provided by TI)
        byte_file_combined = bytearray(scan_data + reference_data)

        existing = ["-1.txt"]
        # List all data files, name the scan next to the highest scan number
        for (dirpath, dirnames, filenames) in walk("/home/user/NirScanSweep/data"):
            existing.extend(filenames)
            break
        existing = [int(file[: -4]) for file in existing]
        existing.sort()
        file_index = existing[-1] + 1
        file_save_name = str(file_index).zfill(4)
        sys.set_int_max_str_digits(0)
        
        numberList = []
        for i in byte_file_combined:
                numberList.append(i)
        # save scan as txt file in data folder
        newFile = open("/home/user/NirScanSweep/data/{}.txt".format(file_save_name), "w")
        newFile.write(str(numberList))
    else:
        # Open the binary
        file_save_name = "0000"
        with open("data/{}.dat".format(file_save_name), "rb") as binaryfile:
            myArr = bytearray(binaryfile.read())
        # send the first half through to the interpret function
        scan_data = myArr[:int(len(myArr)/2)]
    
# Initialize the spectrometer
#spectrometer, device_open = init_spectrometer()
#complete_scan(spectrometer)
