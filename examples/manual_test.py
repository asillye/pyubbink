import asyncio
from pymodbus.client import AsyncModbusTcpClient
from pymodbus.framer import ModbusRtuFramer
from pyubbink import VigorDevice

# To test with TCP:
#
# On home assistant server:
# 1. apk add ser2net
# 2. in ~/ser2net.conf add one single line:
#           13334:raw:0:/dev/ttyUSB1:9600 NONE 1STOPBIT
# 3. start ser2net
#           ser2net -c ~/ser2net.conf -n -d -l
#
# This will redirect the USB1 device to 13334 port

async def main():
    client = AsyncModbusTcpClient(host="192.168.100.10", port=13334, framer=ModbusRtuFramer)

    async with VigorDevice(client) as vigor:
        sensors = await vigor.get_all_sensors()

        print("Device serial number:    " + sensors["serial_number"])
        print("Intake temperature:      " + str(sensors["supply_temperature"]) + " Celsius")
        print("Intake pressure:         " + str(sensors["supply_pressure"]) + " Pa")
        print("Intake actual airflow:   " + str(sensors["supply_airflow_actual"]) + " m3/h")
        print("Intake airflow preset:   " + str(sensors["supply_airflow_preset"]) + " m3/h")
        print("Exhaust temperature:     " + str(sensors["extract_temperature"]) + " Celsius")
        print("Exhaust pressure:        " + str(sensors["extract_pressure"]) + " Pa")
        print("Exhaust actual airflow:  " + str(sensors["extract_airflow_actual"]) + " m3/h")
        print("Exhaust airflow preset:  " + str(sensors["extract_airflow_preset"]) + " m3/h")
        print("Airflow mode:            " + sensors["airflow_mode"])
        print("Bypass status:           " + sensors["bypass_status"])
        print("Filter status:           " + sensors["filter_status"])

        await vigor.set_airflow_mode("low")
        await asyncio.sleep(60)

        await vigor.set_custom_airflow_rate(135)
        await asyncio.sleep(60)

        await vigor.set_airflow_mode("wall_unit")

asyncio.run(main())
