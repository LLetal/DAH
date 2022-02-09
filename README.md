# TDAH - Thermal Detector of Atomic Hydrogen
This is source code of software for my student project about detection of atomic hydrogen. The code is 100% python based and for simplicity I used Inlfuxdb to save the results of the detection. The software itself is really simple, it is based on serial ports of two essential devices I used for keeping the detector running and properly working, programmable power supply Keysight E36232A and RDXL4SD portable thermomether. The E36232 power supply is used for heating and in combination with the RDXL4SD thermometer it also does temperature stabilisation using python library simple-PID.
# Prerequisites
To run this simple script you essentially need the exact two devices I have used for it, since any other devices could simply work different. 
