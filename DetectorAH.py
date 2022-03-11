import serial
import pyvisa
import influxdb_client
from influxdb_client.client.write_api import ASYNCHRONOUS
from simple_pid import PID
from pyvisa.resources import MessageBasedResource
import time
#influx initialization
flux_client = influxdb_client.InfluxDBClient(
    bucket = "Detector",
    org = "Me",
    token = "<insert-token>",
    url = "http://localhost:8086",
)
write_api = flux_client.write_api(write_options=ASYNCHRONOUS)
rm = pyvisa.ResourceManager()

tags = "3/2/2022"
#Hardware and PID setup part
stabilization_output = 0.94 #output needed to keep the temperature stabilised
power_supply = rm.open_resource('USB0::0x2A8D::0x3002::MY59001350::INSTR', resource_pyclass=MessageBasedResource)
pressure_control = rm.open_resource('ASRL6::INSTR', resource_pyclass=MessageBasedResource)
pid = PID(0.00125, 0.00003, 0.00125)
temp_setpoint = 180
pid.setpoint = temp_setpoint
power_supply.write('VOLT 0, (@1)')
temperature = 24.9

#main loop
while True:

    #this terribly looking code is needed to keep the thermometer running, mine had some bug so I had to write this thing
    # to avoid crashing of whole aparature
     with serial.serial_for_url('spy://COM7', timeout=1) as s:
        g = s.readline(16)
        result = g[11:15]
        if (g[11:15].decode()).isprintable() == False:
            pass
        try:
            g[11:15].decode("utf-8")
            if (g[11:15].decode()).isprintable() == False:
                pass

            else:
                if g[11:15].decode("utf-8") == "1010":
                    pass
                else:
                    temperature = float(g[11:15].decode())/10
                    temperature_influx = influxdb_client.Point("Measurement").tag("Test2/21", "temperature").field("Temp", temperature)
                    write_api.write(bucket="Detector2", org="Me", record=temperature_influx)


            voltage = float(power_supply.query("VOLT?"))
            control = pid(float(temperature))
            current = float(power_supply.query("MEAS:CURR?"))
            difference = 0.94-voltage*current

            if difference > 0: #to avoid irrational informations

                num_of_atoms = difference//(4.52*1.602*10**-19)

                flux_Hatom = influxdb_client.Point("Measurement_test").tag(tags, "H_atoms").field("Hydrogen_atom", num_of_atoms)

                write_api.write(bucket="Detector", org="Me", record=flux_Hatom)

            #pressure initialization phase, needed to do it like this again due to funny hardware
            pressure_control.query("PR3\r\n")
            p1 = pressure_control.query("\05")
            if "," in p1:
                p1 = p1.replace(',', ".")

            pressure_control.query("PR4\r\n")
            p2 = pressure_control.query("\05")
            if "," in p2:
                p2 = p2.replace(',', ".")

            loss = (5.67*10**(-8))*0.005*0.02*(temperature+273.15)**4

            #write sequence
            pressure_pump1 = influxdb_client.Point("Measurement").tag(tags, "Pressuree").field("Pump11", float(p1[2:10]))
            pressure_pump2 = influxdb_client.Point("Measurement").tag(tags, "Pressuree").field("Pump22", float(p2[2:10]))
            voltage_influx = influxdb_client.Point("Measurement").tag(tags,"voltage").field("volt", voltage)
            current_influx = influxdb_client.Point("Measurement").tag(tags,"Current").field("amper", current)
            output_influx = influxdb_client.Point("Measurement").tag(tags,"Output").field("watt", current*voltage)
            radiation_influx = influxdb_client.Point("Measurement").tag(tags,"radiation_loss").field("watts", loss)
            write_api.write(bucket="Detector", org="Me",record=voltage_influx)
            write_api.write(bucket="Detector", org="Me", record=current_influx)
            write_api.write(bucket="Detector", org="Me", record=output_influx)
            write_api.write(bucket="Detector", org="Me", record=radiation_influx)
            write_api.write(bucket="Detector", org="Me", record=pressure_pump1)
            write_api.write(bucket="Detector", org="Me", record=pressure_pump2)

            power_supply.write("VOLT "+ str(control))

        except UnicodeError:
            print("Not decodable")
        time.sleep(0.5)# the sleep is here again due to glitching thermometer
