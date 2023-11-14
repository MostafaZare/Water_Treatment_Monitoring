#This modbus_lib.py provides a simple ModbusDevice class that encapsulates the creation of a Modbus client and provides methods for reading and writing to registers.
#It uses the pymodbus library for actual Modbus communication.
#modbus_lib.py

import serial
from pymodbus.client.sync import ModbusSerialClient as ModbusClient
from pymodbus.exceptions import ModbusException

class ModbusDevice:
    def __init__(self, port, slave_id, baudrate=9600, parity=serial.PARITY_NONE, stopbits=1, bytesize=8, timeout=3):
        self.client = ModbusClient(method='rtu', port=port, baudrate=baudrate, parity=parity, stopbits=stopbits, bytesize=bytesize, timeout=timeout)
        self.slave_id = slave_id
        self.connection = self.client.connect()

    def read_registers(self, address, count, unit=1):
        if not self.connection:
            raise ConnectionError("Failed to connect to Modbus device")
        
        try:
            result = self.client.read_holding_registers(address, count, unit=self.slave_id)
            if not result.isError():
                return result.registers
            else:
                raise ModbusException("Modbus read error")
        except ModbusException as e:
            print(f"Modbus read exception: {e}")
            return None

    def write_register(self, address, value, unit=1):
        if not self.connection:
            raise ConnectionError("Failed to connect to Modbus device")
        
        try:
            result = self.client.write_register(address, value, unit=self.slave_id)
            return not result.isError()
        except ModbusException as e:
            print(f"Modbus write exception: {e}")
            return False

    def close(self):
        self.client.close()

# Example usage:
if __name__ == '__main__':
    # Configuration for the Modbus device
    PORT = '/dev/ttyS0'
    SLAVE_ID = 1
    BAUDRATE = 9600
    PARITY = serial.PARITY_NONE
    STOPBITS = 1
    BYTESIZE = 8
    TIMEOUT = 3  # seconds
    
    # Create a Modbus device instance
    modbus_device = ModbusDevice(PORT, SLAVE_ID, BAUDRATE, PARITY, STOPBITS, BYTESIZE, TIMEOUT)
    
    # Read registers example
    try:
        registers = modbus_device.read_registers(0, 10)
        print(f"Registers: {registers}")
    except ConnectionError as e:
        print(f"Connection error: {e}")
    
    # Write to a register example
    success = modbus_device.write_register(0, 100)
    if success:
        print("Write successful")
    else:
        print("Write failed")

    # Close the connection
    modbus_device.close()
