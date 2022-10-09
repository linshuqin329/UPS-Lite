#!/usr/bin/env python
import struct
import smbus
import sys
import time
import RPi.GPIO as GPIO

CW2015_ADDRESS   = 0X62
CW2015_REG_VCELL = 0X02
CW2015_REG_SOC   = 0X04
CW2015_REG_MODE  = 0X0A



def readVoltage(bus):
        "This function returns as float the voltage from the Raspi UPS Hat via the provided SMBus object"
        read = bus.read_word_data(CW2015_ADDRESS, CW2015_REG_VCELL)
        swapped = struct.unpack("<H", struct.pack(">H", read))[0]
        voltage = swapped * 0.305 /1000
        return voltage


def readCapacity(bus):
        "This function returns as a float the remaining capacity of the battery connected to the Raspi UPS Hat via the provided SMBus object"
        read = bus.read_word_data(CW2015_ADDRESS, CW2015_REG_SOC)
        swapped = struct.unpack("<H", struct.pack(">H", read))[0]
        capacity = swapped/256
        return capacity


def QuickStart(bus):
        "This function wake up the CW2015 and make a quick-start fuel-gauge calculations "
        bus.write_word_data(CW2015_ADDRESS, CW2015_REG_MODE, 0x30)
      



       
#----------------------------------------------------------------------------------
        
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(4,GPIO.IN)  # GPIO4 is used to detect whether an external power supply is inserted
  
bus = smbus.SMBus(1)  # 0 = /dev/i2c-0 (port I2C0), 1 = /dev/i2c-1 (port I2C1)


QuickStart(bus)

print ("  ")
print ("Initialize the CW2015 ......")


while True:

 print ("++++++++++++++++++++")
 print ("Voltage:%5.2fV" % readVoltage(bus))
 print ("Battery:%5i%%" % readCapacity(bus))
 
 if readCapacity(bus) == 100:
        print ("Battery FULL")
 if readCapacity(bus) < 5:
        print ("Battery LOW")




#GPIO is high when power is plugged in
 if (GPIO.input(4) == GPIO.HIGH):       
        print ("Power Adapter Plug In ") 
 if (GPIO.input(4) == GPIO.LOW):      
        print ("Power Adapter Unplug")





 print ("++++++++++++++++++++")
 time.sleep(2)
