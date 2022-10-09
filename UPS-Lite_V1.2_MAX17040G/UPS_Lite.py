#!/usr/bin/env python
import struct
import smbus
import sys
import time
import RPi.GPIO as GPIO



def readVoltage(bus):

        "This function returns as float the voltage from the Raspi UPS Hat via the provided SMBus object"
        address = 0x36
        read = bus.read_word_data(address, 0X02)
        swapped = struct.unpack("<H", struct.pack(">H", read))[0]
        voltage = swapped * 1.25 /1000/16
        return voltage


def readCapacity(bus):
        "This function returns as a float the remaining capacity of the battery connected to the Raspi UPS Hat via the provided SMBus object"
        address = 0x36
        read = bus.read_word_data(address, 0X04)
        swapped = struct.unpack("<H", struct.pack(">H", read))[0]
        capacity = swapped/256
        return capacity


def QuickStart(bus):
        address = 0x36
        bus.write_word_data(address, 0x06,0x4000)
      

def PowerOnReset(bus):
        address = 0x36
        bus.write_word_data(address, 0xfe,0x0054)
       

	   
	   
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(4,GPIO.IN)
	   
bus = smbus.SMBus(1)  # 0 = /dev/i2c-0 (port I2C0), 1 = /dev/i2c-1 (port I2C1)

PowerOnReset(bus)
QuickStart(bus)


print "  "
print "Initialize the MAX17040 ......"


while True:

 print "++++++++++++++++++++"
 print "Voltage:%5.2fV" % readVoltage(bus)

 print "Battery:%5i%%" % readCapacity(bus)
 
 
 if readCapacity(bus) == 100:

        print "Battery FULL"

 if readCapacity(bus) < 5:

        print "Battery LOW"


		
		
		
 if (GPIO.input(4) == GPIO.HIGH):
        
		print "Power Adapter Plug In " 
		
 if (GPIO.input(4) == GPIO.LOW):
        
		print "Power Adapter Unplug"
		
		
 print "++++++++++++++++++++"
 time.sleep(2)
