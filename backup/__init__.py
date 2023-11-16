"""The __init__.py file in Python is used to mark directories on disk as a Python package directory.
"If you have a directory containing a __init__.py file, when you import the package in a Python script, the __init__.py executes and defines what symbols the package exposes to the outside world.
"you can put the initialization code for the package in this file.
"Below is an example of a simple __init__.py which might also include importing certain modules from the package for easier access:"""

# __init__.py
from .config_manager import ConfigManager
from .device_manager import DeviceManager
from .thingsboard_client import ThingsboardClient
# ... import other components as needed

# You can also define initialization code here
print("Package initialized.")

"""This file should be placed in the root of your Python package directory. 
"If you are using Python 3.3 or above, __init__.py files are no longer required to define a directory as a Python package, 
"but they are still used to define what gets imported when import * is called on a package. 
"So, it's often still a good practice to include them.
"If you don't need any package-level initialization or symbols definition, then simply creating an empty file named __init__.py is sufficient"""
