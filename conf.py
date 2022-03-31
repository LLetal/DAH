from simple_pid import PID

#influxdb setup
fluxbucket = "Detector"
fluxorg = "Me"
fluxtoken = "<insert-token>"
serverurl = "http://localhost:8086"
Point_name = "ExperimentH"
tag_sys = "Hardware"
tag_det = "Detector"

#PID setup
P = 0.00125 # Proportional component
I = 0.00003 # Integral component
D = 0.00125 # Derivative component
temp_setpoint = 180 # stabilization temperature
starting_temp = 24.9 # Temperature at which the detector starts meassurement
pid_setup = PID(P, I, D)

# Hardware setup reading
stabilization_output = 0.94 #output needed to keep the temperature stabilised
power_supply_usb = 'USB0::0x2A8D::0x3002::MY59001350::INSTR'
Maxigauge = 'ASRL6::INSTR' #device for monitoring of pressure
thermometer_usb = 'spy://COM7'
rm = pyvisa.ResourceManager()
power_supply = rm.open_resource(power_supply_usb, resource_pyclass=MessageBasedResource)
pressure_control = rm.open_resource(power_supply, resource_pyclass=MessageBasedResource)