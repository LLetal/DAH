import serial
import pyvisa
import influxdb_client
from influxdb_client.client.write_api import ASYNCHRONOUS
from simple_pid import PID
from pyvisa.resources import MessageBasedResource

import time

def pidsetup(P, I, D, temperature):
    pid = PID(P,I,D)
    pid.setpoint = temperature
    return(pid)

def hardware(power_supply_usb, maxigauge_usb):
    power_supply = pyvisa.ResourceManager().open_resource(power_supply_usb, resource_pyclass=MessageBasedResource)
    maxigauge =  pyvisa.ResourceManager().open_resource(
         maxigauge_usb, resource_pyclass=MessageBasedResource)
    return(power_supply, maxigauge)

def data_send(setup_list, tag_name, field_name, value):
    data = influxdb_client.point(setup_list[2]).tag(setup_list[3], tag_name).field(field_name, value)
    write_api.write(setup_list[0], setup_list[1], data)

def flux_setup(bucket, org, point_name, tag_general):
    return([bucket, org, point_name, tag_general])

def pid_loop(thermometer_usb, setup_name_list, hardware1, hardware2, pid, stab_temp, command1="VOLT?",
             command2="MEAS:CURR?", temperature=30):
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
                        temperature = float(g[11:15].decode()) / 10
                        data_send(setup_name_list, "Thermometer", "Temperature", temperature)

                voltage = float(hardware1.query(command1))
                current = float(hardware1.query(command2))

                difference = stab_temp - voltage * current

                if difference > 0:  # to avoid irrational informations

                    num_of_atoms = difference // (4.52 * 1.602 * 10 ** -19)

                    data_send(setup_name_list, "H atom source", "H atom flux", num_of_atoms)

                # pressure initialization phase, needed to do it like this again due to funny hardware
                # The setup is inherently for MaxiGauge, but in the future I will add some options
                # for using different hardware
                hardware2.query("PR3\r\n")
                p1 = hardware2.query("\05")

                if "," in p1:
                    p1 = p1.replace(',', ".")

                pressure_control.query("PR4\r\n")

                p2 = pressure_control.query("\05")
                if "," in p2:
                    p2 = p2.replace(',', ".")

                loss = (5.67 * 10 ** (-8)) * 0.005 * 0.02 * (temperature + 273.15) ** 4

                # write sequence, names of variables are fixed for exactly same experiment. In the future
                # I will add more option to change these names.
                data_send(setup_name_list,"Pump1", "Pressure", float(p1[2:10]))
                data_send(setup_name_list,"Pump2", "Pressure", float(p2[2:10]))
                data_send(setup_name_list, "Power supply", "Voltage", voltage)
                data_send(setup_name_list, "Power supply", "Current", current)
                data_send(setup_name_list, "Power supply", "Output", current*voltage)
                data_send(setup_name_list, "Radiative heat", "Loss r", loss)

                hardware1.write("VOLT " + str(pid(float(temperature))))

            except UnicodeError:
                print("Not decodable")
            # the sleep is here again due to glitching thermometer
            time.sleep(0.5)

