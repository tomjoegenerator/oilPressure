# SPDX-FileCopyrightText: 2023 Joseph Sundermier, Thomas Crist
#
# SPDX-License-Identifier: MIT
#
# This program was written to read the voltage drop across a oil pressure transducer with an MCP3008 ADC over the SPI bus.  It then converts
# the voltage to a pressure using a power fit.  It then writes out the oil pressure to a userdefined.json file to be read by the genmon.py
# program and display it on the monitor page.

import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
import json
import os
import time
from datetime import datetime

# Hardware SPI config, did not work reliably.
#mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(0, 0))
# Software SPI configuration,these are my pins convential is (clk=11, cs=1, miso=9, mosi=10), these can be changed to meet your requierments.
mcp = Adafruit_MCP3008.MCP3008(clk=11, cs=8, miso=9, mosi=10)

# Function to read the ADC
def readADC():
   try:
      # Read ADC in difference mode using pins 0 and 1, then convert to a voltage.
      value = mcp.read_adc_difference(0)
      voltage = value * 3.3 / 1027
   except:
      # Handles a I/O error while reading the sensor.
      pressure = "error"
   else:
      # Convert voltage to pressure using a power function a=261.27 and b=1.7026.
      pressure = 261.27 * pow(voltage, 1.7026)
      # If the sensor is not connected voltage > 0.50, or shorted out voltage < 0.02, returns an error.
      if voltage <= 0.02:
         pressure = "error"
      elif voltage >= 0.50:
         pressure = "error"
      else:
         # First convert to a decimal and then a string so it can be outputted in a json file. I  don't really understand, but it works.
         pressure = "%d" % pressure
         pressure = str(pressure)
   finally:
      return pressure

# Function to get the current date and time.
def dateTime():
   now = datetime.now()
   now = now.strftime("%A %B %d, %Y %H:%M:%S")
   return now

# Function to write out the userdefined.json file if it does not exist or is corrupt.
def makeFile():
   data = {
   "Oil pressure": "initializing",
   }
   with open('userdefined.json', 'w') as f:
      json.dump(data, f)
   f.close()

while (True):
   # If userdefined.json exists do not create file.
   if os.path.exists('userdefined.json'):
      pass
   else:
      makeFile()
   # Opens a json file and reads in the data as an array, if file is corrupt recreate it..
   with open('userdefined.json', 'r') as f:
      try:
         data = json.load(f)
      except:
         # If userdefined.json is corrupt, removes it and recreates it.
         os.remove("userdefined.json")
         makeFile()
         with open('userdefined.json', 'r') as f:
            data = json.load(f)
      f.close()
   # Modifies with new reading.
   data['Oil pressure'] = readADC()
   # Writes out the array as a json file.
   with open('userdefined.json', 'w') as f:
      json.dump(data, f)
   f.close()
   # Waits a period of time to for next reading, genmon waits 5 seconds so that good for me..
   time.sleep(5)
