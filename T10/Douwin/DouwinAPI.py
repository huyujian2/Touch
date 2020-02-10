import serial
from serial import *
import serial.tools.list_ports
import os
import sys,os
import math
import fileinput
import binascii
from os import walk
import numpy as np
import matplotlib.pyplot as plt



L = sys.path
L.append(os.getcwd()) # need to add current working directory
# to python path to import defined functions
import time
from time import sleep

import io
import string
import array
import re
import binascii
import struct

class TempControl:
    #define variable
    myPLCSerialPort = None
    strErrorMessage = "ok"

    command_start = [0x3D, 0x20, 0x73, 0x74, 0x61, 0x72, 0x20, 0x31, 0x31, 0x0D, 0x0A]
    command_stop = [0x3D, 0x20, 0x73, 0x74, 0x61, 0x72, 0x20, 0x31, 0x30, 0x0D, 0x0A]
    command_deviceStop = [0x3D, 0x20, 0x70, 0x61, 0x75, 0x73, 0x65, 0x20, 0x31, 0x0D, 0x0A]
    command_deviceContinue = [0x3D, 0x20, 0x63, 0x6F, 0x74, 0x75, 0x20, 0x31, 0x0D, 0x0A]
    command_GetCurrentTemp = [0x3F, 0x20, 0x63, 0x31, 0x0D, 0x0A]
    command_SetAimsTemp = [0x3D, 0x20, 0x73, 0x70, 0x31, 0x20] #command+value(int)+<cr>
    command_GetAimsTemp = [0x3F, 0x20, 0x73, 0x70, 0x31, 0x0D, 0x0A]

    # Open the serial port
    def OpenSerial(self, serialName=""):
        try:
            port_list = list(serial.tools.list_ports.comports())
            if len(port_list) < 0:
                self.strErrorMessage = "There is no serial port"
                return -1
            if len(serialName) < 1:
                for i in range(0, len(port_list), 1):
                    print port_list[i].device
                    self.myPLCSerialPort = serial.Serial(port=port_list[i].device,
                                                         timeout=1,
                                                         baudrate=9600,
                                                         parity=PARITY_NONE)
                    if self.myPLCSerialPort.is_open:
                        return 0
                self.strErrorMessage = "Did not find suitable serial port"
                return -1
            else:
                self.myPLCSerialPort = serial.Serial(port=serialName,baudrate=9600,timeout=1,parity=PARITY_NONE)
                return 0
        except:
            self.strErrorMessage = "OpenSerial except fail"
            return -1

    # ********************************************************************#

    # ********************************************************************#
    # Close the serial port
    def CloseSerial(self):
        try:
            if self.myPLCSerialPort.is_open:
                self.myPLCSerialPort.close()
            return 0
        except:
            self.strErrorMessage = "CloseSerial except fail"
            return -1
    # *********************************************************************#
    def Start_Douwin(self):
        if(self.myPLCSerialPort.isOpen() == False):
            self.strErrorMessage =  "The serial port is not opened"
            return  -1
        try:
            start_write = self.myPLCSerialPort.write(self.command_start)
            time.sleep(0.1)
            read_data = self.myPLCSerialPort.read_all()
            hex_data = binascii.hexlify(read_data)
            if(hex_data[0:] == "1311" or len(hex_data)==4):
                return 0
            else:
                return -1
        except:
            self.strErrorMessage = "Start_Douwin except fail"
            return -1


    # ********************************************************************#
    def Stop_Douwin(self):
        if (self.myPLCSerialPort.isOpen() == False):
            self.strErrorMessage = "The serial port is not opened"
            return -1
        try:
            start_write = self.myPLCSerialPort.write(self.command_stop)
            time.sleep(0.1)
            read_data = self.myPLCSerialPort.read_all()
            hex_data = binascii.hexlify(read_data)
            if(hex_data[0:] == "1311" or len(hex_data)==4):
                return 0
            else:
                return -1
        except:
            self.strErrorMessage = "Stop_Douwin except fail"
            return -1
    # ********************************************************************#
    def DeviceStop_Douwin(self):
        if (self.myPLCSerialPort.isOpen() == False):
            self.strErrorMessage = "The serial port is not opened"
            return -1
        try:
            DeviceStop_write = self.myPLCSerialPort.write(self.command_deviceStop)
            time.sleep(0.1)
            read_data = self.myPLCSerialPort.read_all()
            hex_data = binascii.hexlify(read_data)
            if(hex_data[0:] == "1311" or len(hex_data)==4):
                return 0
            else:
                return -1
        except:
            self.strErrorMessage = "deviceStop_Douwin except fail"
            return -1
    # ********************************************************************#
    def DeviceContinue_Douwin(self):
        if (self.myPLCSerialPort.isOpen() == False):
            self.strErrorMessage = "The serial port is not opened"
            return -1
        try:
            DeviceContinue_write = self.myPLCSerialPort.write(self.command_deviceContinue)
            time.sleep(0.1)
            read_data = self.myPLCSerialPort.read_all()
            hex_data = binascii.hexlify(read_data)
            if(hex_data[0:] == "1311" or len(hex_data)==4):
                return 0
            else:
                return -1
        except:
            self.strErrorMessage = "deviceContinue_Douwin except fail"
            return -1
    # ********************************************************************#
    def GetCurrentTemp_Douwin(self):
        if (self.myPLCSerialPort.isOpen() == False):
            self.strErrorMessage = "The serial port is not opened"
            return -1
        try:
            GetCurrentTemp_write = self.myPLCSerialPort.write(self.command_GetCurrentTemp)
            time.sleep(0.1)
            read_data = self.myPLCSerialPort.read_all()
            sourceData = binascii.hexlify(read_data)
            if(sourceData[0:4] == "1311" ):
                fina1 =binascii.unhexlify(sourceData[4:6])+binascii.unhexlify(sourceData[6:8])
                return fina1
            else:
                return -1
        except:
            self.strErrorMessage = "GetCurrentTemp_Douwin except fail"
            return -1
    # ********************************************************************#
    def SetAimsTemp_Douwin(self,value):
        if (self.myPLCSerialPort.isOpen() == False):
            self.strErrorMessage = "The serial port is not opened"
            return -1
        try:
            if(len(value)>2 or int(value)<=0):
                value_hex1 = int('0x37',16)
                value_hex2 = int('0x30',16)
                final_list = [ value_hex1 , value_hex2 ,0x0D, 0x0A]
            elif(len(value)==2):
                value_hex1 = int(binascii.hexlify(value[0:1]),16)
                value_hex2 = int(binascii.hexlify(value[1:2]),16)
                final_list = [ value_hex1 , value_hex2 ,0x0D, 0x0A]
            elif(len(value)==1):
                value_hex1 = int(binascii.hexlify(value[0:1]),16)
                final_list = [ value_hex1 , 0x0D, 0x0A]
            command_SetAimsTemp = [0x3D, 0x20, 0x73, 0x70, 0x31, 0x20]
            command_SetAimsTemp.extend(final_list)
            set_write = self.myPLCSerialPort.write(command_SetAimsTemp)
            time.sleep(0.1)
            read_data = self.myPLCSerialPort.read_all()
            hex_data = binascii.hexlify(read_data)
            if(hex_data[0:] == "1311"):
                return 0
            else:
                return -1
        except:
            self.strErrorMessage = "SetAimsTemp_Douwin except fail"
            return -1
    # ********************************************************************#
    def GetAimsTemp_Douwin(self):
        if (self.myPLCSerialPort.isOpen() == False):
            self.strErrorMessage = "The serial port is not opened"
            return -1
        try:
            GetAimsTemp_write = self.myPLCSerialPort.write(self.command_GetAimsTemp)
            time.sleep(0.2)
            read_data = self.myPLCSerialPort.read_all()
            sourceData = binascii.hexlify(read_data)
            sourceData = binascii.hexlify(read_data)
            if(sourceData[0:4] == "1311" ):
                fina1 =binascii.unhexlify(sourceData[4:6])+binascii.unhexlify(sourceData[6:8])
                return fina1
            else:
                return -1
        except:
            self.strErrorMessage = "GetAimsTemp_Douwin except fail"
            return -1
    # ********************************************************************#