#!/bin/bash
# start_script.sh
# This script is used to start the IoT system services.

echo "Starting IoT System Services..."

# Change to the script's directory
cd "$(dirname "$0")"

# Start the ThingsBoard client service
echo "Starting ThingsBoard Client..."
python3 thingsboard_client/thingsboard_client.py &

# Start the device manager
echo "Starting Device Manager..."
python3 device_manager/device_manager.py &

# Start the state manager
echo "Starting State Manager..."
python3 state_manager/state_manager.py &

# Initialize and start the Modbus service if required
echo "Starting Modbus Service..."
python3 device_manager/modbus_lib.py &

# Start the main application
echo "Starting Main Application..."
python3 main/main.py &

# Add any additional services here
# ...

echo "All services started successfully."

#The cd "$(dirname "$0")" line changes the current directory to the directory where the script is located. This is useful to ensure that relative paths in the script are executed correctly.
#Each service is started in the background (denoted by the & at the end of each line), allowing the script to continue running and start the next service.
#You can replace the paths and the python filenames with the actual paths and filenames in your project.
#Any "additional methods" would be other necessary services or initialization steps your system might require.
#Make sure to give the proper execute permissions to your script with chmod +x start_script.sh.
