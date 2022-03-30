import serial
import pyvisa
import influxdb_client
from influxdb_client.client.write_api import ASYNCHRONOUS
from simple_pid import PID
from pyvisa.resources import MessageBasedResource
from conf.py import serverurl, fluxtoken, fluxorg, fluxbucket, Point_name, temp_setpoint, starting_temp, P, I, D, \
    power_supply, pressure_control, tag_sys, tag_det
import time
# influx initialization
flux_client = influxdb_client.InfluxDBClient(
    bucket = fluxbucket,
    org = fluxorg,
    token = fluxtoken,
    url = serverurl,
)
write_api = flux_client.write_api(write_options=ASYNCHRONOUS)

rm = pyvisa.ResourceManager()

pid_setup = PID(P, I, D)

tags = "Hardware"


pid.setpoint = temp_setpoint

power_supply.write('VOLT 0, (@1)')

temperature = starting_temp

# main loop
while True:

    # this terribly looking code is needed to keep the thermometer running, mine had some bug so
    # I had to write this thing
    # to avoid crashing of whole aparature
     with serial.serial_for_url(thermometer_usb, timeout=1) as s:
        g = s.readline(16)
        result = g[11:15]

        try:
            g[11:15].decode("utf-8")
            if (g[11:15].decode()).isprintable() is False:
                pass

            else:
                if g[11:15].decode("utf-8") == "1010":
                    pass

                else:
                    temperature = float(g[11:15].decode())/10
                    temperature_influx = influxdb_client.Point(Point_name).tag(tags, "Thermometer").field("Temperature", temperature)
                    write_api.write(bucket=fluxbucket, org=fluxorg, record=temperature_influx)

            voltage = float(power_supply.query("VOLT?"))
            current = float(power_supply.query("MEAS:CURR?"))
            difference = 0.94-voltage*current

            if difference > 0: # to avoid irrational informations

                num_of_atoms = difference//(4.52*1.602*10**-19)

                flux_Hatom = influxdb_client.Point(Point_name).tag(tags, "H atom source").field("H atom flux", num_of_atoms)

                write_api.write(bucket=fluxbucket, org=fluxorg, record=flux_Hatom)

            # pressure initialization phase, needed to do it like this again due to funny hardware
            pressure_control.query("PR3\r\n")
            p1 = pressure_control.query("\05")

            if "," in p1:
                p1 = p1.replace(',', ".")

            pressure_control.query("PR4\r\n")

            p2 = pressure_control.query("\05")
            if "," in p2:
                p2 = p2.replace(',', ".")

            loss = (5.67*10**(-8))*0.005*0.02*(temperature+273.15)**4

            # write sequence
            pump1 = influxdb_client.Point(Point_name).tag(tags, "Pump1").field("Pressure", float(p1[2:10]))

            pump2 = influxdb_client.Point(Point_name).tag(tags, "Pump2").field("Pressure", float(p2[2:10]))

            voltage = influxdb_client.Point(Point_name).tag(tags, "Power supply").field("Voltage", voltage)
            current = influxdb_client.Point(Point_name).tag(tags, "Power supply").field("Current", current)
            output = influxdb_client.Point(Point_name).tag(tags, "Power supply").field("Output", current*voltage)
            radiation = influxdb_client.Point(Point_name).tag(tags, "Radiative_heat").field("Loss_r", loss)
            write_api.write(bucket=fluxbucket, org=fluxorg,record=voltage)
            write_api.write(bucket=fluxbucket, org=fluxorg, record=current)
            write_api.write(bucket=fluxbucket, org=fluxorg, record=output)
            write_api.write(bucket=fluxbucket, org=fluxorg, record=radiation)
            write_api.write(bucket=fluxbucket, org=fluxorg, record=pump1)
            write_api.write(bucket=fluxbucket, org=fluxorg, record=pump2)

            power_supply.write("VOLT "+ str(pid(float(temperature))))

        except UnicodeError:
            print("Not decodable")
        # the sleep is here again due to glitching thermometer
        time.sleep(0.5)