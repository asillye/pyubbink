import pymodbus
import logging

_log = logging

def _convert_from_bcd(bcd):
    """ Converts a bcd value to a decimal value
    :param value: The value to unpack from bcd
    :returns: The number in decimal form
    """
    place, decimal = 1, 0
    while bcd > 0:
        nibble = bcd & 0xf
        decimal += nibble * place
        bcd >>= 4
        place *= 10
    return decimal

class VigorDevice():
    UNIT = 20

    def __init__(self, client, unit=20):
        """ 
        VigorDevice class is a pymodbus wrapper with named commands for the Ubiflux Vigor W350/W400 devices.

        :param client: pymodbus client, typically ModbusSerialClient, SHOULD USE 'rtu' FRAMER!
        :param unit: Modbus slave address of the device (first byte in packages)
        """
        self.client = client
        self.UNIT = unit
        _log.debug("VigorDevice: " + str(client) + " modbus slave address " + str(unit) + " (decimal)")

    def _handle_error(self, rr, method, command):
        _log.error(method + ": error reading ModBus control register command=" + str(command) + ", result=" + str(rr))
        return "error"    

    def _handle_error_int(self, rr, method, command):
        _log.error(method + ": error reading ModBus control register command=" + str(command) + ", result=" + str(rr))
        return -1 

    def get_serial_number(self):
        command = 4010
        rr = self.client.read_input_registers(command, 3, unit=self.UNIT)
        if rr.isError():
            return self._handle_error(rr, "get_serial_number", command)

        serial = str(_convert_from_bcd(rr.registers[0])).zfill(4) + \
                 str(_convert_from_bcd(rr.registers[1])).zfill(4) + \
                 str(_convert_from_bcd(rr.registers[2])).zfill(4) 
        _log.debug("get_serial_number: serial is " + serial)
        return serial


    def get_supply_pressure(self):
        """ 
        Gets the supply pressure in Pascals.
        """
        command = 4023
        rr = self.client.read_input_registers(4023, 1, unit=self.UNIT)
        if rr.isError():
            return self._handle_error_int(rr, "get_supply_pressure", command)

        # NOTE: the documentation says the value is a value in tenths of Pascal, but seems it's just the plain value.
        result = rr.registers[0]
        _log.debug("get_supply_pressure: supply pressure is " + str(result) + " Pa")
        return result

    def get_extract_pressure(self):
        """ 
        Gets the extract pressure in Pascals.
        """
        command = 4024
        rr = self.client.read_input_registers(command, 1, unit=self.UNIT)
        if rr.isError():
            return self._handle_error_int(rr, "get_extract_pressure", command)

        # NOTE: the documentation says the value is a value in tenths of Pascal, but seems it's just the plain value.
        result = rr.registers[0] 
        _log.debug("get_extract_pressure: extract pressure is " + str(result) + " Pa")
        return result

    def get_supply_airflow_preset(self):
        """ 
        Gets the supply airflow preset in cubic meter per hour
        """
        command = 4031
        rr = self.client.read_input_registers(command, 1, unit=self.UNIT)
        if rr.isError():
            return self._handle_error_int(rr, "get_supply_airflow_preset", command)

        result = rr.registers[0]
        _log.debug("get_supply_airflow_preset: " + str(result) + " m3/h")
        return result

    def get_supply_airflow_actual(self):
        """ 
        Gets the actual supply airflow in cubic meter per hour
        """
        command = 4032
        rr = self.client.read_input_registers(command, 1, unit=self.UNIT)
        if rr.isError():
            return self._handle_error_int(rr, "get_supply_airflow_actual", command)

        result = rr.registers[0]
        _log.debug("get_supply_airflow_actual: " + str(result) + " m3/h")
        return result

    def get_extract_airflow_preset(self):
        """ 
        Gets the extract airflow preset in cubic meter per hour
        """
        command = 4041
        rr = self.client.read_input_registers(command, 1, unit=self.UNIT)
        if rr.isError():
            return self._handle_error_int(rr, "get_extract_airflow_preset", command)

        result = rr.registers[0]
        _log.debug("get_extract_airflow_preset: " + str(result) + " m3/h")
        return result

    def get_extract_airflow_actual(self):
        """ 
        Gets the actual extract airflow in cubic meter per hour
        """
        command = 4042
        rr = self.client.read_input_registers(command, 1, unit=self.UNIT)
        if rr.isError():
            return self._handle_error_int(rr, "get_extract_airflow_actual", command)

        result = rr.registers[0]
        _log.debug("get_extract_airflow_actual: " + str(result) + " m3/h")
        return result

    def get_supply_temperature(self):
        """ 
        Gets the supply airflow temperature in Celsius
        """
        command = 4036
        rr = self.client.read_input_registers(command, 1, unit=self.UNIT)
        if rr.isError():
            return self._handle_error_int(rr, "get_supply_temperature", command)

        result = rr.registers[0] / 10.0
        _log.debug("get_supply_temperature: " + str(result) + " Celsius")
        return result

    def get_extract_temperature(self):
        """ 
        Gets the extract airflow temperature in Celsius
        """
        command = 4046
        rr = self.client.read_input_registers(4046, 1, unit=self.UNIT)
        if rr.isError():
            return self._handle_error_int(rr, "get_extract_temperature", command)

        result = rr.registers[0] / 10.0
        _log.debug("get_extract_temperature: " + str(result) + " Celsius")
        return result

    def get_bypass_status(self):
        """ 
        Gets the bypass status eg. open, close etc.
        """
        command = 4050
        rr = self.client.read_input_registers(command, 1, unit=self.UNIT)
        if rr.isError():
            return self._handle_error(rr, "get_bypass_status", command)

        _bypass_modes = {
            0:"initializing",
            1:"opening",
            2:"closing",
            3:"open",
            4:"closed",
        }
        value = rr.registers[0]
        result = _bypass_modes.get(value, "unknown (" + str(value) + ")")

        _log.debug("get_bypass_status: " + result)
        return result

    def get_filter_status(self):
        """ 
        Gets the filter status: dirty/normal
        """
        command = 4100
        rr = self.client.read_input_registers(command, 1, unit=self.UNIT)
        if rr.isError():
            return self._handle_error(rr, "get_filter_status", command)

        value = rr.registers[0]
        if value == 1:
            result = "dirty"
        else:
            result = "normal"

        _log.debug("get_filter_status: " + result)
        return result



    def set_modbus_mode(self, mode):
        """
            Sets the control mode
        """
        command = 8000
        rr = self.client.read_holding_registers(command, 1, unit=self.UNIT)
        if rr.isError():
            return self._handle_error(rr, "set_modbus_mode.1", command)

        value = rr.registers[0]

        _log.debug("set_modbus_mode: ModBus control register is " + str(value))
        if value != mode:
            _log.debug("set_modbus_mode: setting ModBus control register to " + str(mode))
            rr = self.client.write_register(command, mode, unit=self.UNIT)
            if rr.isError():
                return self._handle_error(rr, "set_modbus_mode.2", command)
    
    def get_airflow_mode(self):
        command = 8000
        rr = self.client.read_holding_registers(command, 1, unit=self.UNIT)
        if rr.isError():
            return self._handle_error(rr, "get_airflow_mode.1", command)
        if rr.registers[0] == 0:
            return "wall_unit"
        if rr.registers[0] == 2:
            return "custom_value"

        command = 8001
        rr = self.client.read_holding_registers(command, 1, unit=self.UNIT)
        if rr.isError():
            return self._handle_error(rr, "get_airflow_mode.2", command)
        value = rr.registers[0]

        if value == 0: return "holiday"
        if value == 1: return "low"
        if value == 2: return "normal"
        if value == 3: return "high"

        return "unknown (" + str(value) + ")"

    def set_airflow_mode(self, mode):
        """ 
        Enables the control of the device through Modbus
        """
        if type(mode) == int:
            mode_value = min(3, max(0, mode))
        elif type(mode) == str:
            if mode == "holiday":
                mode_value = 0
            elif mode == "low":
                mode_value = 1
            elif mode == "normal":
                mode_value = 2
            elif mode == "high":
                mode_value = 3
            elif mode == "wall_unit":
                _log.debug("set_airflow_mode: reverting to wall unit control")
                self.set_modbus_mode(0)
                return

        self.set_modbus_mode(1)

        command = 8001
        rr = self.client.read_holding_registers(command, 1, unit=self.UNIT)
        if rr.isError():
            return self._handle_error(rr, "set_airflow_mode.1", command)

        value = rr.registers[0]
        if value != mode_value:
            _log.debug("set_airflow_mode: setting airflow mode to " + str(mode_value) + " in range [0-3]")
            rr = self.client.write_register(command, mode_value, unit=self.UNIT)
            if rr.isError():
                return self._handle_error(rr, "set_airflow_mode.2", command)
        else:
            _log.debug("set_airflow_mode: airflow mode is already " + str(value))

    def set_airflow_rate(self, value):
        """ 
        Sets the preset value of airflow in qubic meters (only Vigor W400 model)

        NOTE: if you read back the value with get_supply_airflow_preset, you have to wait  a short time before doing it
        """
        self.set_modbus_mode(2)

        if value < 50:
            preset_value = 0
        elif value > 400:
            preset_value = 400
        else:
            preset_value = value
                
        command = 8002
        rr = self.client.read_holding_registers(command, 1, unit=self.UNIT)
        if rr.isError():
            return self._handle_error(rr, "set_airflow_rate.1", command)

        value = rr.registers[0]
#        if value != preset_value:
        _log.debug("set_airflow_rate: setting airflow rate to " + str(preset_value) + " in range [0, 50-400]")
        rr = self.client.write_register(command, preset_value, unit=self.UNIT)
        if rr.isError():
            return self._handle_error(rr, "set_airflow_rate.2", command)
 #       else:
  #          _log.debug("set_airflow_rate: airflow mode is already " + str(value))


#_log.basicConfig(level=logging.DEBUG)
