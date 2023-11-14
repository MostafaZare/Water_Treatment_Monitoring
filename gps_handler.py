
"""A comprehensive gps_handler.py module may include functions for 
initializing the GPS device, reading data, error handling, and potentially logging or storing the GPS data."""

# gps_handler.py
import logging
from gps import *
from time import sleep

class GPSHandler:
    def __init__(self):
        self.gpsd = gps(mode=WATCH_ENABLE)
        self.logger = logging.getLogger(self.__class__.__name__)
        self.running = True

    def fetch_data(self):
        """Retrieve the latest GPS data."""
        try:
            report = self.gpsd.next()
            if report['class'] == 'TPV':
                latitude = getattr(report, 'lat', 0.0)
                longitude = getattr(report, 'lon', 0.0)
                altitude = getattr(report, 'alt', 'Not Available')
                speed = getattr(report, 'speed', 'Not Available')
                return {
                    'latitude': latitude,
                    'longitude': longitude,
                    'altitude': altitude,
                    'speed': speed
                }
        except KeyError as e:
            self.logger.error(f"Key error: {e}")
            return None
        except StopIteration:
            self.gpsd = None
            self.logger.error("GPSD has terminated")
            return None
        except Exception as e:
            self.logger.error(f"Unhandled exception: {e}")
            return None

    def start_tracking(self):
        """Start tracking GPS data in a loop."""
        while self.running:
            data = self.fetch_data()
            if data:
                self.logger.info(f"GPS Data: {data}")
                # Here you could also store the data to a database or a file
            sleep(5)  # Wait for a while before reading next data

    def stop_tracking(self):
        """Stop the GPS data fetching loop."""
        self.running = False

# Example usage
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    gps_handler = GPSHandler()
    try:
        gps_handler.start_tracking()
    except (KeyboardInterrupt, SystemExit):
        gps_handler.stop_tracking()
        logging.info("GPS tracking stopped.")

""" the GPSHandler class is responsible for interacting with the GPS device using the gps module. 
It contains methods to fetch and process GPS data and to start and stop data tracking in a loop. 
Error handling is included to manage potential issues during GPS data retrieval.
The fetch_data method retrieves the current data and captures it in a dictionary. 
If there is an error, such as a key error or an iteration stoppage, it logs the error and returns None.
The start_tracking method runs a loop that continuously fetches and logs GPS data at regular intervals (every 5 seconds in this case).
The stop_tracking method allows for a graceful shutdown of the tracking loop."""
