import serial
import pyvisa
import influxdb_client
from influxdb_client.client.write_api import ASYNCHRONOUS
from simple_pid import PID
from pyvisa.resources import MessageBasedResource
import time
flux_client = influxdb_client.InfluxDBClient(
    bucket = "Detector",
    org = "Me",
    token = "r84rvXMT_hF1TpSGNaO3Sk_yhzBwYWJJP22NzYk_hU-r1djCtdd6oEtc3z4hPDBXdTkmSuubk2Frg-7DF_oQkA==",
    url = "http://localhost:8086",
)
write_api = flux_client.write_api(write_options=ASYNCHRONOUS)
rm = pyvisa.ResourceManager()

print(rm.list_resources())

power_supply = rm.open_resource('USB0::0x2A8D::0x3002::MY59001350::INSTR', resource_pyclass=MessageBasedResource)
pressure_control = rm.open_resource('ASRL7::INSTR', resource_pyclass=MessageBasedResource)
pid = PID(0.0000125, 0.0005, 0.00125) #PID(0.000000000125, 0.0005, 0.000125) takh;e to ++- fungovalo

temp_setpoint = 100

pid.setpoint = temp_setpoint

pid.output_limit = (0,1)
power_supply.write('VOLT 0, (@1)')
time.sleep(10)
#
# if z == 20:
#
#     power_supply.write('VOLT 10, (@1)')
#
# else:
#
#     power_supply.write("VOLT 5")

# values = rm.query_ascii_values('?')

# power_supply.write('VOLT 15, (@1)')
# power_supply.write("CURR 3")
#
# power_supply.write("VOLT 5")

# actual_voltage = pyvisa.resources.MessageBasedResource(rm, 'USB0').query_ascii_values("VOLT?")
# 'USB0::0x2A8D::0x3002::MY59001350::INSTR'
temperature = 24.9
print((b"\r\x0241").decode())
print((b'\x18\x18\r').decode())
while True:

     with serial.serial_for_url('spy://COM6', timeout=1) as s:
        g = s.readline(16)

        result = g[12:15]

        if (g[11:15].decode()).isprintable() == False:
            pass

        else:

            temperature = float(g[11:15].decode())/10
            print(temperature)
            temperature_influx = influxdb_client.Point("Measurement_test").tag("Test2/21", "temperature").field("Temp", float(temperature))
            write_api.write(bucket="Detector2", org="Me", record=temperature_influx)
            # if len(temperature) != 0:
            #     #temperature = float(temperature[:2] + "." + temperature[2])
            #     temperature = float(temperature)/10
            #     temperature_influx = influxdb_client.Point("Measurement_test").tag("Test2/21", "temperature").field("Temp",
            #                                                                                              temperature)
            #     write_api.write(bucket="Detector2", org="Me", record=temperature_influx)


        voltage = float(power_supply.query("VOLT?"))
        control = pid(float(temperature))
        print(temperature, control)
        difference = temperature - temp_setpoint

        if difference > 0:

            atomic_hydrogen_heat = influxdb_client.Point("Measurement_test").tag("Test2/21", "Hydrogen_heat").field("Hydhe", difference)
            heat = difference*0.0036*133
            num_of_atoms = (2*6.02*(10**23)*heat)//(0.00015*435.94*5)
            flux_Hatom = influxdb_client.Point("Measurement_test").tag("Test2/21", "H_atoms").field("Hydrogen_atom", num_of_atoms)
            write_api.write(bucket="Detector2", org="Me", record=flux_Hatom)
            write_api.write(bucket="Detector2", org="Me", record=atomic_hydrogen_heat)


        pressure_control.query("PR3\r\n")
        p1 = pressure_control.query("\05")
        print(p1)

        if "," in p1:
            p1 = p1.replace(',', ".")
        pressure_pump1 = influxdb_client.Point("Measurement").tag("Test2/21", "Pressuree").field("Pump11", float(p1[2:10]))
        pressure_control.query("PR4\r\n")
        p2 = pressure_control.query("\05")
        # print(float(p2[2:11]))
        # print("pressure 1 =" + p1)
        # print("pressure2 ="+
        if "," in p2:
            p2 = p2.replace(',', ".")
        pressure_pump2 = influxdb_client.Point("Measurement").tag("Test2/21", "Pressuree").field("Pump22", float(p2[2:10]))


        voltage_influx = influxdb_client.Point("Measurement_test").tag("Test2/21","voltage").field("volt", float(voltage))
        write_api.write(bucket="Detector2", org="Me",record=voltage_influx)

        write_api.write(bucket="Detector2", org="Me", record=pressure_pump1)
        write_api.write(bucket="Detector2", org="Me", record=pressure_pump2)

        # write_api.write(bucket="Detector2", org="Me",record=)
        pid_influx = influxdb_client.Point("Measurement_test").tag("Test2/21","PID_control").field("control", control)
        write_api.write(bucket="Detector2", org="Me", record=pid_influx)
        power_supply.write("VOLT "+ str(control))
        # actual_voltage = pyvisa.resources.MessageBasedResource(rm, 'USB0::0x2A8D::0x3002::MY59001350::INSTR').query_ascii_values("VOLT?")

        # print(actual_voltage)