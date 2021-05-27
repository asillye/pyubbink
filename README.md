# PyUbbink package #

This is an unofficial implementation of the Ubbink Ubiflux Vigor ventillation system Modbus communications.

![Vigor](https://www.ubbink.com/getmedia/7f656140-af4e-48f9-b96e-2ad9b97db3dd/Ubiflux-Vigor)

# Hardware prerequisites #

- Ubiflux Vigor W325 or W400 device
- USB - RS458 dongle

# Hardware setup #

You have to connect your computer or Pi to the Vigor device with a (preferably) twisted pair of wire. Connect the A, B ports of the dongle to the red Modbus port on the Vigor device, A -> 2, B -> 3. If your dongle has a GND port, connect it to 1. (In my setup, I only use two wires, without GND)


# Software Prerequisites #

- Install Python 3, did not checked the actual minimum version, 3.7+ will be fine
- Install pymodbus:
  ```pip install pymodbus --upgrade```
- Install PyUbbink:
  ```pip install pyubbink```
- For the dongle - depending on the version you have - you might need a CH341 chip driver. For Windows, search ```CH341SER``` and you will find it. For Pi + HomeAssistant it worked for me without additional driver.

# Usage #

## Creating the pymodbus client ###
Create a pymodbus serial client, typically  ```ModbusSerialClient```. Use the device name where you connected. For Windows, simply use the COM port name.

```client = ModbusClient(port='/dev/ttyUSB0', baudrate=19200, stopbits = 1, bytesize = 8, parity = 'N', method="rtu")```

In the wall unit, you can change the serial speed to other values - make sure you use the same settings.

The RTU mode is important as Vigor devices use RTU framing.

## Connection ##
Use the ```connect``` method in the pymodbus client to open the serial port: 
```client.connect()```

When connected you can attach the ```pyubbink``` wrapper ```vigor = VigorDevice(client)```

The default ModBus slave address is ```20```. If you change that on the wall unit you can specify it with the ```unit``` parameter, like ```VigorDevice(client, 42)```

When done use ```close```: ```client.close()```


## Obtaining device information ##

```get_serial_number()``` returns the serial number as a string.

## Obtaining sensor values ##

| Sensor       | Method    | Unit    |
|---|---|---|
| Intake temperature     | ```get_supply_temperature()```     | Celsius |
| Intake pressure   | ```get_supply_pressure()```   | Pa      |
| Intake actual airflow  | ```get_supply_airflow_actual()```  | m3/h    |
| Intake airflow preset  | ```get_supply_airflow_preset()```  | m3/h    |
| Exhaust temperature    | ```get_extract_temperature()```    | Celsius |
| Exhaust pressure       | ```get_extract_pressure()```       | Pa      |
| Exhaust actual airflow | ```get_extract_airflow_actual()``` | m3/h    |
| Exhaust airflow preset | ```get_extract_airflow_preset()``` | m3/h    |  

## Obtaining statuses ##

Here are some statuses you can query:

| Status   | Method    | Possible values     |
|---|---|---|
| Bypass status      | ```get_bypass_status()``` | ```"opening"```,```"closing"```, ```"open"```, ```"closed"``` state of the bypass valve,<br>```"initializing"``` during boot
| Filter status      | ```get_filter_status()``` | ```"normal"```, ```"dirty"```
| Airflow mode       | ```get_airflow_mode()```  | Wall unit: ```"wall_unit"```  in this case the wall unit controls the device<br>Standard presets: ```"holiday"```,```"low"```,```"normal"```,```"high"``` the last selected preset set by ```set_airflow_mode()```<br>Custom: ```"custom"``` if the last setting was done with ```set_custom_airflow_rate()```

## Actions ##

The following methods are to change the airflow.
**If the wall unit is in manual mode, it seems all of these are ignored, and the only manual setting of the wall unit used.** Once you set it back to clock program, the last setting applied by these method will be used.

Also, it seems, if these settings applied without reasonable delay (>5 secs), the device seems ignoring them.

| Action |  Method     | Parameters      |
|---|---|---|
| Revert to wall unit   | ```set_airflow_mode("wall_unit")``` | Use the ```"wall_unit``` to hand back the control to the wall unit.
| Choose preset   | ```set_airflow_mode(mode)``` | Selects one of the presets: ```"holiday"```,```"low"```,```"normal"```,```"high"``` 
| Custom rate     | ```set_custom_airflow_rate(rate)``` | 0, 50-400, if out of range the value will be adjusted to a valid one. <br>This option is only available for Vigor W400 (according the documentation. I have W400 and it works.)


# Full example #

```python
from pymodbus.client.sync import ModbusSerialClient as ModbusClient
from pyubbink import VigorDevice
import time

client = ModbusClient(port='/dev/ttyUSB0', baudrate=19200, stopbits = 1, bytesize = 8, parity = 'N', method="rtu", timeout=60)
vigor = VigorDevice(client)

client.connect()
print("Device serial number:    " + vigor.get_serial_number())

print("Intake temperature:      " + str(vigor.get_supply_temperature()) + " Celsius")
print("Intake pressure:    " + str(vigor.get_supply_pressure()) + " Pa")
print("Intake actual airflow:   " + str(vigor.get_supply_airflow_actual()) + " m3/h")
print("Intake airflow preset:   " + str(vigor.get_supply_airflow_preset()) + " m3/h")
print("Exhaust temperature:     " + str(vigor.get_extract_temperature()) + " Celsius")
print("Exhaust pressure:   " + str(vigor.get_extract_pressure()) + " Pa")
print("Exhaust actual airflow:  " + str(vigor.get_extract_airflow_actual()) + " m3/h")
print("Exhaust airflow preset:  " + str(vigor.get_extract_airflow_preset()) + " m3/h")

print("Airflow mode:       " + vigor.get_airflow_mode())
print("Bypass status:      " + vigor.get_bypass_status())
print("Filter status:      " + vigor.get_filter_status())

# choose a preset
vigor.set_airflow_mode("low")
time.sleep(60)

# choose a custom rate
vigor.set_airflow_rate(135)
time.sleep(60)

# revert back to wall unit
vigor.set_airflow_mode("wall_unit")

client.close()
```

# References #

## General description ##

https://www.ubbink.com/nl-be/ventilatie/woonhuisventilatie/woonhuisventilatie/warmteterugwinunits

https://www.ubbink.com/en-gb/ventilation/residential-ventilation/residential-ventilation/ubiflux-mvhr-heat-recovery-units

## Manual ##

Interestingly, only the Dutch version contains the ModBus commands.
https://www.ubbink.com/getmedia/b970e7e8-a20f-4265-82c0-948590c74311/Ubiflux-Vigor-W325-installatiehandleiding-versie-12-2018-NL.PDF

When looking at the PDF, pay attention to the hex and decimal values. In the documentation, they are sometimes hex, sometimes decimal.

## Hardware ##

Search for ```CH340 USB to RS485 485 Converter Adapter Module``` Looks like:

![Black Dongle](https://i.ebayimg.com/images/g/Fw0AAOSw8G1d71s5/s-l640.jpg)

or

![Blue Dongle](https://i.ebayimg.com/images/g/Nx4AAOSwpAhgMkTw/s-l640.jpg)

For me, this blue one did not work, but I might got a defective one.