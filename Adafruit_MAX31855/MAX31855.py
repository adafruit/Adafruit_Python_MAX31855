# Copyright (c) 2014 Adafruit Industries
# Author: Tony DiCola
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
import logging
import math

import Adafruit_GPIO as GPIO
import Adafruit_GPIO.SPI as SPI

# Default I2C address for device.
MCP9808_I2CADDR_DEFAULT        = 0x18

# Register addresses.
MCP9808_REG_CONFIG             = 0x01
MCP9808_REG_UPPER_TEMP         = 0x02
MCP9808_REG_LOWER_TEMP         = 0x03
MCP9808_REG_CRIT_TEMP          = 0x04
MCP9808_REG_AMBIENT_TEMP       = 0x05
MCP9808_REG_MANUF_ID           = 0x06
MCP9808_REG_DEVICE_ID          = 0x07

# Configuration register values.
MCP9808_REG_CONFIG_SHUTDOWN    = 0x0100
MCP9808_REG_CONFIG_CRITLOCKED  = 0x0080
MCP9808_REG_CONFIG_WINLOCKED   = 0x0040
MCP9808_REG_CONFIG_INTCLR      = 0x0020
MCP9808_REG_CONFIG_ALERTSTAT   = 0x0010
MCP9808_REG_CONFIG_ALERTCTRL   = 0x0008
MCP9808_REG_CONFIG_ALERTSEL    = 0x0002
MCP9808_REG_CONFIG_ALERTPOL    = 0x0002
MCP9808_REG_CONFIG_ALERTMODE   = 0x0001


class MAX31855(object):
	"""Class to represent an Adafruit MAX31855 thermocouple temperature
	measurement board.
	"""

	def __init__(self, clk=None, cs=None, do=None, spi=None, gpio=None):
		"""Initialize MAX31855 device with software SPI on the specified CLK,
		CS, and DO pins.  Alternatively can specify hardware SPI by sending an
		Adafruit_GPIO.SPI.SpiDev device in the spi parameter.
		"""
		self._logger = logging.getLogger('Adafruit_MAX31855.MAX31855')
		self._spi = None
		# Handle hardware SPI
		if spi is not None:
			self._logger.debug('Using hardware SPI')
			self._spi = spi
		elif clk is not None and cs is not None and do is not None:
			self._logger.debug('Using software SPI')
			# Default to platform GPIO if not provided.
			if gpio is None:
				gpio = GPIO.get_platform_gpio()
			self._spi = SPI.BitBang(gpio, clk, None, do, cs)
		else:
			raise ValueError('Must specify either spi for for hardware SPI or clk, cs, and do for softwrare SPI!')
		self._spi.set_clock_hz(5000000)
		self._spi.set_mode(0)
		self._spi.set_bit_order(SPI.MSBFIRST)

	def readInternalC(self):
		"""Return internal temperature value in degrees celsius."""
		v = self._read32()
		# Ignore bottom 4 bits of thermocouple data.
		v >>= 4
		# Grab bottom 11 bits as internal temperature data.
		internal = v & 0x7FF
		if v & 0x800:
			# Negative value, take 2's compliment. Compute this with subtraction
			# because python is a little odd about handling signed/unsigned.
			internal -= 4096
		# Scale by 0.0625 degrees C per bit and return value.
		return internal * 0.0625

	def readTempC(self):
		"""Return the thermocouple temperature value in degrees celsius."""
		v = self._read32()
		# Check for error reading value.
		if v & 0x7:
			return float('NaN')
		# Check if signed bit is set.
		if v & 0x80000000:
			# Negative value, take 2's compliment. Compute this with subtraction
			# because python is a little odd about handling signed/unsigned.
			v >>= 18
			v -= 16384
		else:
			# Positive value, just shift the bits to get the value.
			v >>= 18
		# Scale by 0.25 degrees C per bit and return value.
		return v * 0.25

	def _read32(self):
		# Read 32 bits from the SPI bus.
		raw = self._spi.read(4)
		if raw is None or len(raw) != 4:
			raise RuntimeError('Did not read expected number of bytes from device!')
		value = raw[0] << 24 | raw[1] << 16 | raw[2] << 8 | raw[3]
		self._logger.debug('Raw value: 0x{0:08X}'.format(value & 0xFFFFFFFF))
		return value
