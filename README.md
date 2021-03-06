# TDAH - Thermal Detector of Atomic Hydrogen
This is the source code of software for my student project about the detection of atomic hydrogen using thermal detectors. In a nutshell, these devices measure the heat released by recombination of atomic hydrogen and determine consequences from it. Its also a proven fact, that the recombination coefficient of atomic hydrogen, and so the sensitivity of thermal detectors is closely related to the temperature of recombination area, so it is simply better to keep recombination area on some higher temperature. Problem is, that with recombination the detector without stabilization would raise its temperature and so would raise the recombination coefficient, and the experiment would simply become irrelevant. Except for this usage I have also found out, that it would be quite interesting to watch all the metrics of the experiment in real-time, so I have also included it in this little project. 
\
![Aparature](https://raw.githubusercontent.com/LLetal/DAH/main/Pictures/aparature.png)
**Figure 1** Aparature\
![H atom source](https://github.com/LLetal/DAH/blob/main/Pictures/20220124_154920.jpg)
**Figure 2** H atom source\
![Detector of H](https://github.com/LLetal/DAH/blob/main/Pictures/2022-01-20%2009.34.26.jpg)
**Figure 3** Detector of H\
![Detector of H inside of aparature](https://github.com/LLetal/DAH/blob/main/Pictures/2022-01-20%2011.50.04.jpg)
**Figure 4** Detector of H inside of aparature

# Motivation for the work 
Atomic hydrogen is dominant element inside of space nebulas. Logically because of this, the research of atomic hydrogen is essential for further understanding of initial formation of space bodies, such as planets, stars or asteroids. Regarding this, studying of atomic hydrogen also helps us with better understanding of molecular synthesis and even in determination of age of space bodies. Problem is, that atomic hydrogen mostly dont exist on Earth, so we need to acquire it from dissociating of molecular hydrogen using various methods. Problem is, that we cant quite accuratelly theoretically determine how many atoms are produced from the source. Relating to this fact, in order to simulate the conditions inside space nebula recquired for exact experiment we need to use experimental methods of calibration. Two most common methods are chemical calibration and calibration using detector of atomic hydrogen. In my project I covered the second method, because it compared to chemical calibration allows realtime monitoring of atomic hydrogen flux and so the easier calibration of atomic hydrogen source.

# How the software works

The work of the software is briefly illustrated by the following picture:
\
![Simple scheme](https://github.com/LLetal/DAH/blob/main/Pictures/detector-scheme.svg)
\
**Figure 5** PID Scheme

The PID process is, as visible in the picture, made through a thermometer, which is directly connected to the detector. The computer gets the information about actual temperature from the thermometer and then using PID calculates what output should the source should have and sends it directly to it. Due to this temperature of the detector changes and so does the input of the thermometer. This process repeats until the temperature is stabilized and so the experiment is ready. The setup also monitors the pressure inside a vacuum chamber. At the same as this is happening computer is also sending the data to an external influxdb server. Its also worth of mentioning, that all communication, except the one with influxdb, is established via serial port.

# About Code 
The code is 100% python based and for simplicity I have used Inlfuxdb for data logging of the detection process. I have also created a custom influxdb dashboard, which I used throughout the whole experiment. 

![Dashboard](https://github.com/LLetal/DAH/blob/main/Pictures/Dashboard1.0.png)
**Figure 6** Used dashboard

The software itself is really simple, it is based on serial ports of two essential devices I use for keeping the detector running and properly working - programmable power supply Keysight E36232A and Omega RDXL4SD portable thermometer. The E36232 power supply is used for heating and in combination with the RDXL4SD thermometer it also does temperature stabilization using python library simple-PID, as explained above. Data about the temperature inside vacuum chambers is collected from Pfeiffer Maxigauge TPG 256. The only ailment is, that for reading the serial ports properly I had to use two different libraries - pyvisa and pyserial. The sometimes irrational parts of code are there on purpose because without them the communication with devices wouldn't work.

# Prerequisites
To run this simple script you essentially need the exact two devices(not counting the Maxigauge data collection, which is optionable) I have used for it since any other device could simply work differently and simply wouldn???t recognize the commands.

# TODO
Implement grafana, make pip library and implement my own PID to replace the simple-pid library.

