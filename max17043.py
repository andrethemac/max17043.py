#!/usr/bin/env python3

"""
max17043 library for MicroPython
this is a lipo battery cells fuel gauge made by maxim
https://datasheets.maximintegrated.com/en/ds/MAX17043-MAX17044.pdf
small module by sparkfun
https://www.sparkfun.com/products/10617
based upon the max17043 library for arduino by lucadentella
https://github.com/lucadentella/ArduinoLib_MAX17043

Andre Peeters
2017/10/31
"""

from machine import I2C
import binascii

class max17043:
    REGISTER_VCELL = const(0X02)
    REGISTER_SOC = const(0X04)
    REGISTER_MODE = const(0X06)
    REGISTER_VERSION = const(0X08)
    REGISTER_CONFIG = const(0X0C)
    REGISTER_COMMAND = const(0XFE)

    def __init__(self, pins=('P9','P10')):
        """
        init the module and set the pins used for i2c
        scans for the i2c adress (returns the first 1 found)
        """
        self.pins = tuple(pins)
        self.i2c = I2C(0, pins=pins)
        self.i2c.init(I2C.MASTER) # init as a master
        self.max17043Address = (self.i2c.scan())[0]

    def __str__(self):
        """
        string representation of the values
        """
        rs  = "i2c address is {}\n".format( self.max17043Address )
        rs += "i2c pins are {}\n".format( self.pins )
        rs += "version is {}\n".format( self.getVersion() )
        rs += "vcell is {} v\n".format( self.getVCell() )
        rs += "soc is {} %\n".format( self.getSoc() )
        rs += "compensatevalue is {}\n".format( self.getCompensateValue() )
        rs += "alert threshold is {} %\n".format( self.getAlertThreshold() )
        rs += "in alert is {}".format( self.inAlert() )
        return rs

    def address(self):
        """
        return the i2c address
        """
        return self.max17043Address

    def reset(self):
        """
        reset
        """
        self.__writeRegister(REGISTER_COMMAND,binascii.unhexlify('0054'))

    def getVCell(self):
        """
        get the volts left in the cell
        """
        buf = self.__readRegister(REGISTER_VCELL)
        return (buf[0] << 4 | buf[1] >> 4) /1000.0

    def getSoc(self):
        """
        get the state of charge
        """
        buf = self.__readRegister(REGISTER_SOC)
        return (buf[0] + (buf[1] / 256.0) )

    def getVersion(self):
        """
        get the version of the max17043 module
        """
        buf = self.__readRegister(REGISTER_VERSION)
        return (buf[0] << 8 ) | (buf[1])

    def getCompensateValue(self):
        """
        get the compensation value
        """
        return self.__readConfigRegister()[0]

    def getAlertThreshold(self):
        """
        get the alert level
        """
        return ( 32 - (self.__readConfigRegister()[1] & 0x1f) )

    def setAlertThreshold(self, threshold):
        """
        sets the alert level
        """
        self.threshold = 32 - threshold if threshold < 32 else 32
        buf = self.__readConfigRegister()
        buf[1] = (buf[1] & 0xE0) | self.threshold
        self.__writeConfigRegister(buf)

    def inAlert(self):
        """
        check if the the max17043 module is in alert
        """
        return (self.__readConfigRegister())[1] & 0x20

    def clearAlert(self):
        """
        clears the alert
        """
        self.__readConfigRegister()

    def quickStart(self):
        """
        does a quick restart
        """
        self.__writeRegister(REGISTER_MODE,binascii.unhexlify('4000'))

    def __readRegister(self,address):
        """
        reads the register at address, always returns bytearray of 2 char
        """
        return self.i2c.readfrom_mem(self.max17043Address,address,2)

    def __readConfigRegister(self):
        """
        read the config register, always returns bytearray of 2 char
        """
        return self.__readRegister(REGISTER_CONFIG)

    def __writeRegister(self,address,buf):
        """
        write buf to the register address
        """
        self.i2c.writeto_mem(self.max17043Address,address,buf)

    def __writeConfigRegister(self,buf):
        """
        write buf to the config register
        """
        self.__writeRegister(REGISTER_CONFIG,buf)

    def deinit(self):
        """
        turn off the peripheral
        """
        self.i2c.deinit()
