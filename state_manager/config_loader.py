# config_loader.py

"""The config_loader.py script is typically responsible for parsing configuration files and 
providing an accessible interface for the rest of the application to retrieve configuration settings. """

import yaml
import os
import logging

class ConfigLoader:
    def __init__(self, config_files):
        self.config_data = {}
        self.logger = logging.getLogger(self.__class__.__name__)
        self.load_configs(config_files)

    def load_configs(self, config_files):
        """Loads configuration data from a list of YAML config files."""
        for config_file in config_files:
            if os.path.exists(config_file):
                with open(config_file, 'r') as file:
                    try:
                        config = yaml.safe_load(file)
                        self.config_data.update(config)
                        self.logger.info(f"Configuration loaded from {config_file}")
                    except yaml.YAMLError as e:
                        self.logger.error(f"Error loading configuration from {config_file}: {e}")
            else:
                self.logger.warning(f"Config file {config_file} does not exist.")

    def get(self, key, default=None):
        """Retrieves a configuration value for a given key."""
        return self.config_data.get(key, default)

    def set(self, key, value):
        """Sets a configuration value."""
        self.config_data[key] = value

    def save_config(self, config_file):
        """Saves the current configuration to a YAML file."""
        with open(config_file, 'w') as file:
            try:
                yaml.dump(self.config_data, file)
                self.logger.info(f"Configuration saved to {config_file}")
            except yaml.YAMLError as e:
                self.logger.error(f"Error saving configuration to {config_file}: {e}")

# Example usage
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    config_files = ['default_config.yaml', 'user_config.yaml']
    config_loader = ConfigLoader(config_files)

    # Get a config value
    database_url = config_loader.get('database_url', 'localhost')
    logging.info(f"Database URL: {database_url}")

    # Set a new config value
    config_loader.set('cache_timeout', 3600)

    # Save the current configuration
    config_loader.save_config('current_config.yaml')

"This ConfigLoader class uses the PyYAML library to parse YAML configuration files. 
"It provides methods to load configurations from multiple files, allowing for a layered approach where default settings can be overridden by user-specific configurations. 
"The get method fetches configuration values with an optional default, and the set method allows for runtime configuration changes. 
"The save_config method persists the current configuration state back to a file.
