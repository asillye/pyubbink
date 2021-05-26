from pymodbus.client.sync import ModbusSerialClient as ModbusClient
from pymodbus.client.sync import ModbusTcpClient
from  pyubbink import VigorDevice
from pymodbus.transaction import ModbusRtuFramer as ModbusFramer
import time

# client = ModbusClient(port='COM9', baudrate=9600, stopbits = 1, bytesize = 8, parity = 'N', method="rtu", timeout=60)


# To test with TCP:

# On home assistant server:
# 1. apk add ser2net
# 2. in ~/ser2net.conf add one single line:
#           13334:raw:0:/dev/ttyUSB1:9600 NONE 1STOPBIT
# 3. start ser2net
#           ser2net -c ~/ser2net.conf -n -d -l
#
# This will redirect the USB1 device to 13334 port
#
client = ModbusTcpClient(host="192.168.100.10", port=13334, framer=ModbusFramer, method="rtu")

vigor = VigorDevice(client)

client.connect()

print("Device serial number:    " + vigor.get_serial_number())

#vigor.set_airflow_mode("low")
vigor.set_airflow_rate(50)

time.sleep(5)

print("Intake temperature:      " + str(vigor.get_supply_temperature()) + " Celsius")
print("Intake pressure:         " + str(vigor.get_supply_pressure()) + " Pa")
print("Intake actual airflow:   " + str(vigor.get_supply_airflow_actual()) + " m3/h")
print("Intake airflow preset:   " + str(vigor.get_supply_airflow_preset()) + " m3/h")
print("Exhaust temperature:     " + str(vigor.get_extract_temperature()) + " Celsius")
print("Exhaust pressure:        " + str(vigor.get_extract_pressure()) + " Pa")
print("Exhaust actual airflow:  " + str(vigor.get_extract_airflow_actual()) + " m3/h")
print("Exhaust airflow preset:  " + str(vigor.get_extract_airflow_preset()) + " m3/h")

print("Airflow mode:            " + vigor.get_airflow_mode())
print("Bypass status:           " + vigor.get_bypass_status())
print("Filter status:           " + vigor.get_filter_status())

client.close()