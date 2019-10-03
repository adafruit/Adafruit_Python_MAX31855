DEPRECATED LIBRARY Adafruit Python MAX31855
======================================

This library has been deprecated! We are leaving this up for historical and research purposes but archiving the repository.

We are now only supporting the use of our CircuitPython libraries for use with Python.

Check out this guide for info on using this sensor with the CircuitPython library: https://learn.adafruit.com/thermocouple/python-circuitpython

Adafruit Python MAX31855
------------------------

Python library for accessing the MAX31855 thermocouple temperature sensor on a Raspberry Pi or Beaglebone Black.

Designed specifically to work with the Adafruit MAX31855 sensor ----> https://www.adafruit.com/products/269

To install, first make sure some dependencies are available by running the following commands (on a Raspbian
or Beaglebone Black Debian install):

````
sudo apt-get update
sudo apt-get install build-essential python-dev python-smbus
````

Then download the library by clicking the download zip link to the right and unzip the archive somewhere on your Raspberry Pi or Beaglebone Black.  Then execute the following command in the directory of the library:

````
sudo python setup.py install
````

Make sure you have internet access on the device so it can download the required dependencies.

See examples of usage in the examples folder.

Adafruit invests time and resources providing this open source code, please support Adafruit and open-source hardware by purchasing products from Adafruit!

Written by Tony DiCola for Adafruit Industries.
MIT license, all text above must be included in any redistribution
