import logging
from thingsboard_client import ThingsBoardClient
from device_manager import DeviceManager
from state_manager import StateManager
from state_manager.config_loader import ConfigLoader
from handlers import GPSHandler, FlowCalculationHandler
from utilities import RuntimeTracker

"Configuration"
THINGSBOARD_HOST = 'demo.thingsboard.io'
ACCESS_TOKEN = 'YOUR_ACCESS_TOKEN'

def main():
    # Set up logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    "Load configuration"
    config_loader = ConfigLoader()
    config = config_loader.load_config()

    "Initialize ThingsBoard client"
    tb_client = ThingsBoardClient(THINGSBOARD_HOST, ACCESS_TOKEN)
    tb_client.connect()

    "Initialize Device Manager"
    device_manager = DeviceManager(config)

    "Initialize State Manager"
    state_manager = StateManager(config)

    "Initialize GPS Handler"
    gps_handler = GPSHandler()

    "Initialize Flow Calculation Handler"
    flow_handler = FlowCalculationHandler()

    "Initialize Runtime Tracker"
    runtime_tracker = RuntimeTracker(logger)

    try:
        "Start the Runtime Tracker"
        runtime_tracker.start()

        "Main application loop"
        while True:
            "Process devices"
            device_manager.process_devices()

            "Handle GPS data"
            gps_data = gps_handler.fetch_data()
            if gps_data:
                tb_client.publish_telemetry(gps_data)

            "Calculate flow rates"
            flow_data = flow_handler.calculate_flow()
            if flow_data:
                tb_client.publish_telemetry(flow_data)

            "Check for state updates"
            state_manager.sync_state()

            "TODO: Add more application logic here"

    except KeyboardInterrupt:
        logger.info("Application stopped by user")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
    finally:
        "Stop the Runtime Tracker"
        runtime_tracker.stop()

        "Disconnect from ThingsBoard"
        tb_client.disconnect()

        "Perform any necessary cleanup"
        device_manager.cleanup()
        gps_handler.cleanup()
        flow_handler.cleanup()

        "Log the total runtime"
        total_runtime = runtime_tracker.get_total_runtime()
        logger.info(f"Total runtime before shutdown: {total_runtime}")

if __name__ == "__main__":
    main()
