# TDAH - Thermal Detector of Atomic Hydrogen
This is the source code of software for my student project about the detection of atomic hydrogen using thermal detectors. In a nutshell, these devices measure the heat released by recombination of atomic hydrogen and determine consequences from it. Its also a proven fact, that the recombination coefficient of atomic hydrogen, and so the sensitivity of thermal detectors is closely related to the temperature of recombination area, so it is simply better to keep recombination area on some higher temperature. Problem is, that with recombination the detector without stabilization would raise its temperature and so would raise the recombination coefficient, and the experiment would simply become irrelevant. Except of this usage I have also found out, that it would be quite interesting to watch all the metrics of the experiment in realtime, so I have also included it in this little project. 
# How the software works
The work of the software is briefly illustrated by the following picture:

The PID process is, as visible on picture, made through thermometer, which is directly connected to detector. The computer gets the information about actual temperature from thermometer and then using PID calculates what output should the source should have and sends it directly to it. Due to this temperature of detector changes and so does the input of thermometer. This process repeats until temperature is stabilised and so the experiment is ready. Simple as it is. 
# About Code 
The code is 100% python based and for simplicity I have used Inlfuxdb for data logging of the detection process. I have also created custom influxdb dashboard, which I used throughout the whole experiment. The software itself is really simple, it is based on serial ports of two essential devices I use for keeping the detector running and properly working - programmable power supply Keysight E36232A and RDXL4SD portable thermometer. The E36232 power supply is used for heating and in combination with the RDXL4SD thermometer it also does temperature stabilization using python library simple-PID. The only ailment is, that for reading the serial ports properly I had to use two different libraries - pyvisa and pyserial.

# Prerequisites
To run this simple script you essentially need the exact two devices I have used for it since any other devices could simply work differently and simply wouldn‘t recognize the commands.

I am soon going to paste here the code itself, but before I have to make sure it 100% works with my detector. If you would like to know more about my project feel free to leave a comment in issues!

