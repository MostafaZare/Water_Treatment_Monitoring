
"""Below is an example script GPIOExample.py that uses the GPIOControl class to control a GPIO pin. 
This example demonstrates initializing the GPIO, setting it high, reading its value, and then cleaning up. 
It also includes error handling and encapsulates these steps in a simple command-line interface for toggling the GPIO state."""

#!/usr/bin/env python3
import sys
from hardware_interface.gpiocontrol import GPIOControl

def main():
    if len(sys.argv) < 3:
        print("Usage: GPIOExample.py <GPIO_PIN> <ACTION>")
        print("ACTION can be 'high', 'low', or 'read'")
        sys.exit(1)

    gpio_pin = int(sys.argv[1])
    action = sys.argv[2].lower()

    gpio_control = GPIOControl(gpio_pin)

    try:
        if action == 'high':
            gpio_control.set_high()
            print(f"GPIO {gpio_pin} set to HIGH")
        elif action == 'low':
            gpio_control.set_low()
            print(f"GPIO {gpio_pin} set to LOW")
        elif action == 'read':
            value = gpio_control.read_value()
            print(f"GPIO {gpio_pin} is {value}")
        else:
            print("Invalid action. Use 'high', 'low', or 'read'.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        gpio_control.cleanup()

if __name__ == "__main__":
    main()
"""Run the script with the GPIO pin number and the desired action (high, low, or read) as command-line arguments.
It creates an instance of the GPIOControl class.
Depending on the action specified, it sets the pin high, sets the pin low, or reads the value of the pin.
It includes error handling to catch any exceptions that might occur during GPIO operations.
It ensures that the GPIO pin is cleaned up at the end of the operations, even if an error occurs.
"""

#To use this script, you would call it from the command line (bash), for example:
python GPIOExample.py 4 high
#This would set GPIO pin 4 to high. Similarly, you can set it to low or read its value.
