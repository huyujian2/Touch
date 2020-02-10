'''
Release Note:
1.add function(FixtureStatus): get the curtain sensor status:
    return 1  -->  治具处于正常状态
    return -1 -->  Fixture status except fail
    return -2 -->  触碰到光栅
    return -3 -->  急停按钮被按压
'''

import sys,os
import math
import fileinput
import binascii
from os import walk
import datetime


L = sys.path
L.append(os.getcwd()) # need to add current working directory
# to python path to import defined functions
import time
from time import sleep
import serial
import serial.tools.list_ports

import io
import string
import array
import re
import binascii
import struct


class GOEControlClass:

    def __init__(self):

        # defined Class Variables
        self.ReadPLCVersion = "%01#RDD0030000302"
        # Step move
        self.MoveForwardStep_xAxis = "%01#WCSR00201"
        self.MoveBackwardStep_xAxis = "%01#WCSR00211"
        self.MoveForwardStep_yAxis = "%01#WCSR00241"
        self.MoveBackwardStep_yAxis = "%01#WCSR00251"
        self.MoveForwardStep_zAxis = "%01#WCSR00281"
        self.MoveBackwardStep_zAxis = "%01#WCSR00291"
        # Step set
        self.SetStep_xAxis = "%01#WDD0100001001"
        self.SetStep_yAxis = "%01#WDD0100801009"
        self.SetStep_zAxis = "%01#WDD0101601017"
        # Step get
        self.GetStep_xAxis = "%01#RDD0060000601"
        self.GetStep_yAxis = "%01#RDD0060200603"
        self.GetStep_zAxis = "%01#RDD0060400605"
        # Set speed
        self.SetSpeed_xAxis = "%01#WDD0020000201"
        self.SetSpeed_yAxis = "%01#WDD0021000211"
        self.SetSpeed_zAxis = "%01#WDD0022000221"
        # Get speed
        self.GetSpeed_xAxis = "%01#RDD0020000201"
        self.GetSpeed_yAxis = "%01#RDD0021000211"
        self.GetSpeed_zAxis = "%01#RDD0022000221"
        # Set move distance
        self.SetDistane_xAxis = "%01#WDD0020200203"
        self.SetDistane_yAxis = "%01#WDD0021200213"
        self.SetDistane_zAxis = "%01#WDD0022200223"
        # Move x&y&z
        self.XYMove = "%01#WCSR002F1"
        self.XYZMove = "%01#WCSR002B1"
        self.XMove = "%01#WCSR002C1"
        self.YMove = "%01#WCSR002D1"
        self.ZMove = "%01#WCSR002E1"
        # Get x&y&z
        self.GetCoordiante_xAxis = "%01#RDD0014600147"
        self.GetCoordiante_yAxis = "%01#RDD0015000151"
        self.GetCoordiante_zAxis = "%01#RDD0015400155"

        # Single of moving axis
        self.SingleMoveFinish_xAxis = "%01#RCSR0800"
        self.SingleMoveFinish_yAxis = "%01#RCSR0801"
        self.SingleMoveFinish_zAxis = "%01#RCSR0802"
        self.SingleMoveFinish_xyAxis = "%01#RCSR0803"
        # self.SingleMoveFinish_xyzAxis = "%01#RCSR0059"
        self.SingleHomeFinish_xAxis = "%01#RCSR0100"
        self.SingleHomeFinish_yAxis = "%01#RCSR0101"
        self.SingleHomeFinish_zAxis = "%01#RCSR0102"
        self.SingleHomeFinish_xyzAxis = "%01#RCSR0104"

        # Get Limit
        self.GetMaxLimit_xAxis = "%01#RDD0062000621"
        self.GetMaxLimit_yAxis = "%01#RDD0062200623"
        self.GetMaxLimit_zAxis = "%01#RDD0062400625"
        self.GetMinLimit_xAxis = "%01#RDD0063000631"
        self.GetMinLimit_yAxis = "%01#RDD0063200633"
        self.GetMinLimit_zAxis = "%01#RDD0063400635"

        # Set Limit
        self.SetMaxLimit_xAxis = "%01#WDD0210002101"
        self.SetMinLimit_xAxis = "%01#WDD0210402105"
        self.SetMaxLimit_yAxis = "%01#WDD0210802109"
        self.SetMinLimit_yAxis = "%01#WDD0211202113"
        self.SetMaxLimit_zAxis = "%01#WDD0211602117"
        self.SetMinLimit_zAxis = "%01#WDD0212002121"

        # reset
        self.ResetCommand_ON = "%01#WCSR00841"
        self.ResetCommand_OFF = "%01#WCSR00840"

        # Sensor
        self.CylinderSensorInCommand = "%01#RCSX0011"
        self.CylinderSensorOutCommand = "%01#RCSX0012"
        self.CalibrateSensor = "%01#RCSX001F"
        self.CurtainSensorCommand = "%01#RCSX0010"
        self.EStopStatusCommand = "01#RCSX0009"

        # Cylinder
        self.TrayCylinderOut_ON = "%01#WCSR02061"
        self.TrayCylinderIn_ON = "%01#WCSR02041"
        self.TrayCylinderOut_OFF = "%01#WCSR02060"
        self.TrayCylinderIn_OFF = "%01#WCSR02040"

        self.myPLCSerialPort = None
        self.strErrorMessage = "ok"

        self.DefaultAxis_x = 36
        self.DefaultAxis_y = 14
        self.DefaultAxis_y = 24.5

        self.Axis_x = 1
        self.Axis_y = 2
        self.Axis_z = 3
        self.Axis_xy = 4
        self.Axis_xyz = 5
        self.MaxLimit = 6
        self.MinLimit = 7
        self.Out = 8
        self.In = 9

        self.CylinderSensorIn = 10
        self.CylinderSensorOut = 11

        # For Fixture status
        self.CurtainSensor = 13
        self.EStop = 14
        self.CurtainSensorStatus = True

        self.ZAxisX1Limit = 402
        self.ZAxisX2Limit = 403
        self.ZAxisY1Limit = 404
        self.ZAxisY2Limit = 405
        self.ZAxisY3Limit = 406
        self.ZAxisY4Limit = 407

        self.TouchA = 500
        self.TouchB = 501
        self.TouchC = 502
        self.TouchD = 503
        self.Touch_LOCK = 506
        self.Touch_OPEN = 507
        #other
        self.DUT1 = 508
        self.DUT2 = 509
        self.DUT3 = 5081
        self.DUT4 = 5091
        self.Red_OFF = 4101
        self.Red_ON = 4100
        self.Yellow_OFF = 4201
        self.Yellow_ON = 4200
        self.Green_ON = 4301
        self.Green_OFF = 4300
        #other
        self.DUT_LOCK = 510
        self.DUT_OPEN = 511
        self.CheckDUT1 = 512
        self.CheckDUT2 = 513

        self.LightCurtainOn = 514
        self.LightCurtainOff = 515

        self.TouchASensor = "%01#RCSX0300"
        self.TouchBSensor = "%01#RCSX0301"
        self.TouchCSensor = "%01#RCSX0302"
        self.TouchDSensor = "%01#RCSX0303"
        self.DUT1Sensor = "%01#RCSX0304"
        self.DUT2Sensor = "%01#RCSX0305"
        self.CheckZ = "%01#RCSX001B"

        # Calibration
        self.SetUpx = -9999
        self.SetUpy = -9999
        self.SetLeftx = -9999
        self.SetLefty = -9999
        self.SetDownx = -9999
        self.SetDowny = -9999
        self.SetRightx = -9999
        self.SetRighty = -9999
        self.SetZx = -9999
        self.SetZy = -9999
        self.offset = -9999

        self.ZIncrementx = 0
        self.ZIncrementy = 0
        self.YAxisCalIncrementX = 0
        self.YAxisCalIncrementY = 0
        self.YAxisCalDecrementX = 0
        self.YAxisCalDecrementY = 0

        self.XAxisCalIncrementX = 0
        self.XAxisCalIncrementY = 0
        self.XAxisCalDecrementX = 0
        self.XAxisCalDecrementY = 0

        # ********************************************************************************************#
    # return error message to UI
    def GetErrorMessage(self):
        return self.strErrorMessage

    # ********************************************************************************************#

    # ********************************************************************#
    # Open the PLC port
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
                                                         baudrate=115200,
                                                         parity=serial.PARITY_ODD)
                    if self.myPLCSerialPort.is_open:
                        err = self.AutoChooseCom()
                        if err != 0:
                            self.myPLCSerialPort.close()
                        else:
                            #clear
                            ret = self.SignalReset(30)
                            if (ret == -1):
                                self.strErrorMessage = "SignalReset read error"
                                return -1
                            return 0
                self.strErrorMessage = "Did not find suitable serial port"
                return -1
            else:
                self.myPLCSerialPort = serial.Serial(port=serialName,
                                                     timeout=1,
                                                     baudrate=115200,
                                                     parity=serial.PARITY_ODD)
                #clear
                ret = self.SignalReset(30)
                if (ret == -1):
                    self.strErrorMessage = "SignalReset read error"
                    return -1
                return 0
        except:
            self.strErrorMessage = "OpenSerial except fail"
            return -1

    # ********************************************************************#

    # ********************************************************************#

    # ********************************************************************#
    def AutoChooseCom(self):
        try:

            command = '%01#RDD0015400155'
            bcc = self.__bccValue(command)
            command = command + bcc + '\r'
            command = command.upper()
            self.myPLCSerialPort.write(command)
            readStr = self.ReadData(0.1)
            time.sleep(0.5)
            #readString = self.myPLCSerialPort.read_all()
            if ("fail" in readStr):
                self.strErrorMessage = "ChooseCOM read command fail"
                return -1
            else:
                return 0
        except:
            self.strErrorMessage = "AutoChooseCom except fail"
            return -1

    # **************************************************************#

        # Close the PLC port
    def CloseSerial(self):
        try:
            if self.myPLCSerialPort.is_open:
                self.myPLCSerialPort.close()
            return 0
        except:
            self.strErrorMessage = "CloseSerial except fail"
            return -1
    # **************************************************************#

    # ********************************************************************#
    # Set Limit of X / Y / Z axis
    def SetLimit(self, ofWhatAxis,ofWhatLimit,Limit):
        try:
            if ofWhatAxis == self.Axis_x:
                if ofWhatLimit == self.MaxLimit:
                    command = self.SetMaxLimit_xAxis
                elif ofWhatLimit == self.MinLimit:
                    command = self.SetMinLimit_xAxis
            elif ofWhatAxis == self.Axis_y:
                if ofWhatLimit == self.MaxLimit:
                    command = self.SetMaxLimit_yAxis
                elif ofWhatLimit == self.MinLimit:
                    command = self.SetMinLimit_yAxis
            elif ofWhatAxis == self.Axis_z:
                if ofWhatLimit == self.MaxLimit:
                    command = self.SetMaxLimit_zAxis
                elif ofWhatLimit == self.MinLimit:
                    command = self.SetMinLimit_zAxis

            # Set ZAxisX1Limit
            elif (ofWhatAxis == self.ZAxisX1Limit):
                command = '%01#WDD0212402125'
            # Set ZAxisX2Limit
            elif (ofWhatAxis == self.ZAxisX2Limit):
                command = '%01#WDD0212602127'
            # Set ZAxisY1Limit
            elif (ofWhatAxis == self.ZAxisY1Limit):
                command = '%01#WDD0212802129'
            # Set ZAxisY2Limit
            elif (ofWhatAxis == self.ZAxisY2Limit):
                command = 'H%01#WDD0213002131'
            # Set ZAxisY3Limit
            elif (ofWhatAxis == self.ZAxisY3Limit):
                command = '%01#WDD0213202133'
            # Set ZAxisY4Limit
            elif (ofWhatAxis == self.ZAxisY4Limit):
                command = '%01#WDD0213402135'
            else:
                self.strErrorMessage = "SetPLCLimit input parameter is not correct"
                return -1

            finalByte = self.__flipByte(Limit)
            command = command + finalByte
            ret = self.__writeRead(command)
            if ret == 0:
                return 0
            else:
                return -1
        except:
            self.strErrorMessage = "SetLimit except fail"
            return -1
    # ********************************************************************#
    # Get Limit of X / Y / Z axis
    def GetLimit(self, ofWhatAxis, ofWhatLimit):
        try:
            if ofWhatAxis == self.Axis_x:
                if ofWhatLimit == self.MaxLimit:
                    command = self.GetMaxLimit_xAxis
                elif ofWhatLimit == self.MinLimit:
                    command = self.GetMinLimit_xAxis
            elif ofWhatAxis == self.Axis_y:
                if ofWhatLimit == self.MaxLimit:
                    command = self.GetMaxLimit_yAxis
                elif ofWhatLimit == self.MinLimit:
                    command = self.GetMinLimit_yAxis
            elif ofWhatAxis == self.Axis_z:
                if ofWhatLimit == self.MaxLimit:
                    command = self.GetMaxLimit_zAxis
                elif ofWhatLimit == self.MinLimit:
                    command = self.GetMinLimit_zAxis

            #write command to get data
            bcc = self.__bccValue(command)
            command = command + bcc + '\r'
            command = command.upper()
            self.myPLCSerialPort.write(command)

            #read data
            readString = self.ReadData(0.1)
            if("fail" in readString):
                self.strErrorMessage = "read data timeout"
                return -9999
            else:
                value = self.__getValueOfByte(readString)
                return (value*10)
        except:
            self.strErrorMessage = "GetLimit except fail"
            return -9999

    # ********************************************************************#
    #Get current coordinate
    def GetCurrentCoordinates(self,ofWhatAxis):
        try:
            if (ofWhatAxis == self.Axis_x):
                command = self.GetCoordiante_xAxis
            elif (ofWhatAxis == self.Axis_y):
                command = self.GetCoordiante_yAxis
            elif (ofWhatAxis == self.Axis_z):
                command = self.GetCoordiante_zAxis
            bcc = self.__bccValue(command)
            command = command + bcc + '\r'
            command = command.upper()
            self.myPLCSerialPort.write(command)

            # read data
            readString = self.ReadData(0.1)
            if ("fail" in readString):
                self.strErrorMessage = "GetCurrentCoordinate timeout"
                return -9999
            else:
                value = self.__getValueOfByte(readString)
                return (value * 10)
        except:
            self.strErrorMessage = "GetCurrentCoordinate except fail"
            return -9999
    # ********************************************************************#

    # ********************************************************************#
    #Moving to specified Coordinates per Axis
    def MoveToCoordinates(self,ofWhatAxis,Value,timeout=10):
        try:
            #Read sensor
            ret = self.__readONorOFF(self.CylinderSensorInCommand)
            ret = int(ret)
            if ret == 0:
                self.strErrorMessage = "please Cylinder_IN first"
                log = open("__readONorOFF.txt",'a')
                log.write("__readONorOFF fail {0}".format(datetime.datetime.now()))
                log.close()
                return -1
            if ret == -1:
                self.strErrorMessage = "Cylinder sensor fail"
                log = open("CylinderSensor.txt",'a')
                log.write("CylinderSensor fail {0}".format(datetime.datetime.now()))
                log.close()
                return -1
            ret =self.FixtureStatus()
            if ret == -1:
                self.strErrorMessage = "Get fixture status fail"
                log = open("CylinderSensor.txt",'a')
                log.write("CylinderSensor fail {0}".format(datetime.datetime.now()))
                log.close()
                return -1
            if ret == -2:
                self.strErrorMessage = "Had touch Curtain"
                log = open("FixtureStatus.txt",'a')
                log.write("FixtureStatus fail, Had touch Curtain {0}".format(datetime.datetime.now()))
                log.close()
                return ret
            if ret == -3:
                self.strErrorMessage = "Had puss EStop"
                log = open("FixtureStatus.txt",'a')
                log.write("FixtureStatus fail, Had puss EStop {0}".format(datetime.datetime.now()))
                log.close()
                return ret
            finalByte = self.__flipByte(Value)
            if ofWhatAxis == self.Axis_x:
                command_first = "%01#WCSR002C0"
                command = self.SetDistane_xAxis + finalByte
                MoveCommand = self.XMove
                moveFinishCommand = self.SingleMoveFinish_xAxis
            elif ofWhatAxis == self.Axis_y:
                command_first = "%01#WCSR002D0"
                command = self.SetDistane_yAxis + finalByte
                MoveCommand = self.YMove
                moveFinishCommand = self.SingleMoveFinish_yAxis
            elif ofWhatAxis == self.Axis_z:
                command_first = "%01#WCSR002E0"
                command = self.SetDistane_zAxis + finalByte
                MoveCommand = self.ZMove
                moveFinishCommand = self.SingleMoveFinish_zAxis
            ret = self.__writeRead(command_first)
            if ret != 0:
                self.strErrorMessage = "MoveToCoordinates write distance fail"
                log = open("ClearCommand.txt",'a')
                log.write("ClearCommand fail {0}".format(datetime.datetime.now()))
                log.close()
                return -1

            ret = self.__writeRead(command)
            if ret != 0:
                self.strErrorMessage = "MoveToCoordinates write distance fail"
                log = open("SetMoveStep.txt",'a')
                log.write("SetMoveStep fail {0}".format(datetime.datetime.now()))
                log.close()
                return -1
            time.sleep(0.2)
            ret = self.__writeRead(MoveCommand)
            if ret != 0:
                log = open("__writeRead.txt",'a')
                log.write("__writeRead fail {0}".format(datetime.datetime.now()))
                log.close()
                self.strErrorMessage = "MoveToCoordinates move fail"
                return -1

            mytimeCount = 0
            while (self.GetmoveSignal(ofWhatAxis) == 1):
                time.sleep(0.005)
                mytimeCount = mytimeCount + 0.005
            if mytimeCount >= timeout:
                self.strErrorMessage = "MoveToCoordinates time out"
                log = open("GetmoveSignal.txt",'a')
                log.write("GetMoveSignal fail {0}".format(datetime.datetime.now()))
                log.close()
                return -1
            else:
                return 0
        except:
            self.strErrorMessage = "MoveToCoordinates except fail"
            log = open("__except.txt", 'a')
            log.write("__except fail {0}".format(datetime.datetime.now()))
            log.close()
            return -1
    # ********************************************************************#

    # ********************************************************************#
    # Set Increment / Decrement Value
    def SetStepValue(self, ofWhatAxis, Value):
        try:
            finalByte = self.__flipByte(Value)
            if ofWhatAxis == self.Axis_x:
                command = self.SetStep_xAxis + finalByte
            elif ofWhatAxis == self.Axis_y:
                command = self.SetStep_yAxis + finalByte
            elif ofWhatAxis == self.Axis_z:
                command = self.SetStep_zAxis + finalByte
            ret = self.__writeRead(command)
            if ret != 0:
                self.strErrorMessage = "SetStepValue set fail"
                return -1
            return 0
        except:
            self.strErrorMessage = "SetStepValue except fail"
            return -1
    # ********************************************************************#
    # ********************************************************************#
    def GetStepValue(self, ofWhatAxis):
        try:
            if (ofWhatAxis == self.Axis_x):
                command = self.GetStep_xAxis
            elif(ofWhatAxis == self.Axis_y):
                command = self.GetStep_yAxis
            elif(ofWhatAxis == self.Axis_z):
                command = self.GetStep_zAxis
            bcc = self.__bccValue(command)
            command = command + bcc + '\r'
            command = command.upper()
            self.myPLCSerialPort.write(command)
            #read data
            readString = self.ReadData(0.1)
            if("fail" in readString):
                self.strErrorMessage = "read data timeout"
                return -1
            value = self.__getValueOfByte(readString)
            return (value*10)
        except:
            self.strErrorMessage = "GetStepValue except fail"
            return -1
    # ********************************************************************#

    # ********************************************************************#
    def MoveStep(self, ofWhatAxis,timeout=10):
        try:
            if (ofWhatAxis == self.Axis_x):
                command = self.MoveForwardStep_xAxis
            elif(ofWhatAxis == self.Axis_y):
                command = self.MoveForwardStep_yAxis
            elif(ofWhatAxis == self.Axis_z):
                command = self.MoveForwardStep_zAxis

            ret = self.__writeRead(command)
            if(ret == -1):
                self.strErrorMessage = "MoveStep fail"
                return -1
            # return 0
            mytimeCount = 0
            while (self.GetmoveSignal(ofWhatAxis) == 1):
                time.sleep(0.1)
                mytimeCount = mytimeCount + 0.1
                if mytimeCount >= timeout:
                    self.strErrorMessage = "MoveStep time out"
                    return -1
            return 0
        except:
            self.strErrorMessage = "MoveIncrement except fail"
            return -1
    # ********************************************************************#

    #x and y move
    def SynchronousXY(self,xValue,yValue,timeout=10):
        try:
            #Read sensor
            ret = self.__readONorOFF(self.CylinderSensorInCommand)
            ret = int(ret)
            if ret == 0:
                self.strErrorMessage = "please Cylinder_IN first"
                return -1
            if ret == -1:
                self.strErrorMessage = "Cylinder sensor fail"
                return -1

            finalByte = self.__flipByte(xValue)
            command = self.SetDistane_xAxis + finalByte
            ret = self.__writeRead(command)
            if(ret != 0):
                self.strErrorMessage =  "SynchronousXY x fail"
                return -1
            finalByte = self.__flipByte(yValue)
            command = self.SetDistane_yAxis + finalByte
            ret = self.__writeRead(command)
            if(ret != 0):
                self.strErrorMessage = "SynchronousXY y fail"
                return -1
            bcc = self.__bccValue(self.XYMove)
            command = self.XYMove + bcc + '\r'
            command = command.upper()
            ret = self.__writeRead(command)
            if(ret != 0):
                self.strErrorMessage = "SynchronousXY  fail"
                return -1
            mytimeCount = 0
            while (self.GetmoveSignal(self.Axis_x) == 1):
                time.sleep(0.1)
                mytimeCount = mytimeCount + 0.1
                if mytimeCount >= timeout:
                    self.strErrorMessage = "SynchronousXY xy time out"
                    return -1
            mytimeCount = 0
            while (self.GetmoveSignal(self.Axis_y) == 1):
                time.sleep(0.1)
                mytimeCount = mytimeCount + 0.1
                if mytimeCount >= timeout:
                    self.strErrorMessage = "SynchronousXY xy time out"
                    return -1
            return 0
        except:
            self.strErrorMessage = "SynchronousXY except fail"
            return -1

    # ********************************************************************#



    # ********************************************************************#
    #check the single of moveing axis
    def GetmoveSignal(self, ofWhatAxis):
        try:
            if ofWhatAxis == self.Axis_x:
                command = self.SingleMoveFinish_xAxis
            elif ofWhatAxis ==self.Axis_y:
                command = self.SingleMoveFinish_yAxis
            elif ofWhatAxis ==self.Axis_z:
                command = self.SingleMoveFinish_zAxis
            elif ofWhatAxis ==self.Axis_xy:
                command = self.SingleMoveFinish_xyAxis
            elif ofWhatAxis ==self.Axis_xyz:
                command = self.SingleMoveFinish_xyzAxis

            bcc = self.__bccValue(command)
            command = command + bcc + '\r'
            command = command.upper()
            self.myPLCSerialPort.write(command)
            readString = self.ReadData(0.01)
            if("fail" in readString):
                self.strErrorMessage = "GetmoveSignal read time out"
                return -1
            readString = int(readString[6])
            if (readString == 0):
                return 0
            elif (readString == 1):
                return 1
            else:
                self.strErrorMessage = "GetmoveSignal error"
                return -1
        except:
            self.strErrorMessage = "GetmoveSignal except fail"
            return -1
    # ********************************************************************#

    # ********************************************************************#
    # Set speed
    def SetSpeed(self, ofWhatAxis, Value):
        try:
            if ofWhatAxis < self.Axis_xy:
                if ofWhatAxis == self.Axis_x:
                    command = self.SetSpeed_xAxis
                elif ofWhatAxis == self.Axis_y:
                    command = self.SetSpeed_yAxis
                elif ofWhatAxis == self.Axis_z:
                    command = self.SetSpeed_zAxis

                finalByte = self.__flipByte(Value)
                command = command + finalByte
                ret = self.__writeRead(command)
                if (ret != 0):
                    self.strErrorMessage = "SetSpeed:set speed fail"
                    return -1
                return 0
            else:
                for i in range(0, 3, 1):
                    if i == 0:
                        command = self.SetSpeed_xAxis
                    elif i == 1:
                        command = self.SetSpeed_yAxis
                    elif i == 2:
                        command = self.SetSpeed_zAxis

                    finalByte = self.__flipByte(Value)
                    command = command + finalByte
                    ret = self.__writeRead(command)
                    if (ret != 0):
                        self.strErrorMessage = "SetSpeed:set speed fail"
                        return -1
                return 0
        except:
            self.strErrorMessage = "SetSpeed except fail"
            return -1
    # ********************************************************************#
    # Get speed
    def GetSpeed(self, ofWhatAxis):
        try:
            if ofWhatAxis == self.Axis_x:
                command = self.GetSpeed_xAxis
            elif ofWhatAxis == self.Axis_y:
                command = self.GetSpeed_yAxis
            elif ofWhatAxis == self.Axis_z:
                command = self.GetSpeed_zAxis
            # write
            bcc = self.__bccValue(command)
            command = command + bcc + '\r'
            command = command.upper()
            self.myPLCSerialPort.write(command)

            # read data
            readString = self.ReadData(0.1)
            if ("fail" in readString):
                self.strErrorMessage = "GetAxisSpeed:read data timeout"
                return -1
            value = self.__getValueOfByte(readString)
            iSpeed = int(value)
            return iSpeed
        except:
            self.strErrorMessage = "GetAxisSpeed except fail"
            return -1
    # ********************************************************************#
    #Reset
    def SignalReset(self,timeout=10):
        try:
            #clear
            self.CurtainSensorStatus = True
            command = self.ResetCommand_OFF
            bcc = self.__bccValue(command)
            command = command + bcc + '\r'
            ret = self.__writeRead(command)
            if (ret == -1):
                self.strErrorMessage = "SignalReset read error"
                return -1

            mytimeCount = 0
            command = self.ResetCommand_ON
            bcc = self.__bccValue(command)
            command = command + bcc + '\r'
            ret = self.__writeRead(command)
            if ret != 0:
                self.strErrorMessage = "SignalReset fail"
                return -1

            #xyz home
            mytimeCount = 0
            while (self.GetHomeFinishState(self.Axis_xyz) == 1):
                if (mytimeCount > timeout):
                    self.strErrorMessage = "SignalReset Reset time out"
                    return -1
                time.sleep(0.5)
                mytimeCount = mytimeCount + 0.5
            if mytimeCount > timeout:
                self.strErrorMessage = "SignalReset Axis_xyz out"
                return -1

            #DUT open or lock
            mytimeCount = 0
            while (self.GetSensorStatus(self.DUT1) == 1):
                if (mytimeCount > timeout):
                    self.strErrorMessage = "SignalReset Reset time out"
                    return -1
                time.sleep(0.5)
                mytimeCount = mytimeCount + 0.5
            if mytimeCount > timeout:
                self.strErrorMessage = "SignalReset DUT1Sensor out"
                return -1

            #cylinder out
            mytimeCount = 0
            while (self.GetSensorStatus(self.CylinderSensorOut) == 0):
                if (mytimeCount > timeout):
                    self.strErrorMessage = "SignalReset Reset time out"
                    return -1
                time.sleep(0.5)
                mytimeCount = mytimeCount + 0.5
            if mytimeCount > timeout:
                self.strErrorMessage = "SignalReset DUT1Sensor out"
                return -1

            command = self.ResetCommand_OFF
            bcc = self.__bccValue(command)
            command = command + bcc + '\r'
            ret = self.__writeRead(command)
            if (ret == -1):
                self.strErrorMessage = "SignalReset read error"
                return -1
            return 0
        except:
            self.strErrorMessage = "SignalReset except fail"
            return -1

    # ********************************************************************#
    def GetHomeFinishState(self, ofWhatAxis):
        if (self.myPLCSerialPort.isOpen() == False):
            self.strErrorMessage = "The serial port is not opened"
            return -1
        try:
            if (ofWhatAxis == self.Axis_xyz):
                command = self.SingleHomeFinish_xyzAxis
            elif (ofWhatAxis == self.Axis_x):
                command = self.SingleHomeFinish_xAxis
            elif (ofWhatAxis == self.Axis_y):
                command = self.SingleHomeFinish_yAxis
            elif (ofWhatAxis == self.Axis_z):
                command = self.SingleHomeFinish_zAxis

            bcc = self.__bccValue(command)
            command = command + bcc + '\r'
            command = command.upper()
            self.myPLCSerialPort.write(command)
            readString = self.ReadData(0.01)
            if ("fail" in readString):
                self.strErrorMessage = "GetHomeFinishState read time out"
                return -1
            readString = int(readString[6])
            if (readString == 1):
                return 0
            elif (readString == 0):
                return 1
        except:
            self.strErrorMessage = "GetHomeFinishState error"
            return -1

    # ********************************************************************#
    def TopCapTouch(self, Axis_x=40, Axis_y=9, Axis_z=20, timeout=10):
        if (self.myPLCSerialPort.isOpen() == False):
            self.strErrorMessage = "The serial port is not opened"
            return -1
        try:
            ret = self.MoveToCoordinates(self.Axis_x, Axis_x, timeout)
            if ret != 0:
                self.strErrorMessage = "MoveToCoordinates Axis_x move fail"
                return -1
            ret = self.MoveToCoordinates(self.Axis_y, Axis_y, timeout)
            if ret != 0:
                self.strErrorMessage = "MoveToCoordinates Axis_y move fail"
                return -1
            ret = self.MoveToCoordinates(self.Axis_z, Axis_z, timeout)
            if ret != 0:
                self.strErrorMessage = "MoveToCoordinates Axis_z move fail"
                return -1
            return 0
        except:
            self.strErrorMessage = "TopCapTouch error"
            return -1
    # ********************************************************************#

    # ********************************************************************************************#
    #TouchLockOrOpen
    def TouchAndDUTLcokOrOpen(self, index, state):
        if (self.myPLCSerialPort.isOpen() == False):
            self.strErrorMessage = "The serial port is not opened"
            return -1
        try:
            if (index == self.TouchA):
                if (state == self.Touch_LOCK):
                    command = "%01#WCSR00401"
                elif (state == self.Touch_OPEN):
                    command = "%01#WCSR00400"
            elif (index == self.TouchB):
                if (state == self.Touch_LOCK):
                    command = "%01#WCSR00411"
                elif (state == self.Touch_OPEN):
                    command = "%01#WCSR00410"
            elif (index == self.TouchC):
                if (state == self.Touch_LOCK):
                    command = "%01#WCSR00421"
                elif (state == self.Touch_OPEN):
                    command = "%01#WCSR00420"
            elif (index == self.TouchD):
                if (state == self.Touch_LOCK):
                    command = "%01#WCSR00431"
                elif (state == self.Touch_OPEN):
                    command = "%01#WCSR00430"

            elif (index == self.DUT1):
                if (state == self.DUT_LOCK):
                    command = "%01#WCSR00441"
                elif (state == self.DUT_OPEN):
                    command = "%01#WCSR00440"
            elif (index == self.DUT2):
                if (state == self.DUT_LOCK):
                    command = "%01#WCSR00451"
                elif (state == self.DUT_OPEN):
                    command = "%01#WCSR00450"
            elif (index == self.DUT3):
                if (state == self.DUT_LOCK):
                    command = "%01#WCSR00461"
                elif (state == self.DUT_OPEN):
                    command = "%01#WCSR00460"
            elif (index == self.DUT4):
                if (state == self.DUT_LOCK):
                    command = "%01#WCSR00471"
                elif (state == self.DUT_OPEN):
                    command = "%01#WCSR00470"


            ret = self.__writeRead(command)
            if (ret != 0):
                self.strErrorMessage = "TouchLcokOrOpen Red command fail"
                return -1
            else:
                if (index == self.TouchA):
                    sensor = self.TouchA
                elif (index == self.TouchB):
                    sensor = self.TouchB
                elif (index == self.TouchC):
                    sensor = self.TouchC
                elif (index == self.TouchD):
                    sensor = self.TouchD

                elif (index == self.DUT1):
                    sensor = self.DUT1
                elif (index == self.DUT2):
                    sensor = self.DUT2

                if (state == self.Touch_LOCK):
                    exceptValue = 1
                elif (state == self.Touch_OPEN):
                    exceptValue = 0
                elif (state == self.DUT_LOCK):
                    exceptValue = 1
                elif (state == self.DUT_OPEN):
                    exceptValue = 0

                timeout = 3
                myTimeout = 0
                while (True):
                    ret = self.GetSensorStatus(sensor)
                    if (exceptValue == ret):
                        break
                    elif (ret == -1):
                        self.strErrorMessage = "DUTLcokOrOpen read error"
                        return -1
                    elif (myTimeout > timeout):
                        self.strErrorMessage = "DUTLcokOrOpen time out"
                        return -1
                    time.sleep(0.1)
                    myTimeout = myTimeout + 0.1
            return 0
        except:
            self.strErrorMessage = "DUTLcokOrOpen error"
            return -1
    # ********************************************************************#

    # ********************************************************************************************#
    # ********************************************************************#


    def GetSensorStatus(self, ofWhatSensor):
        try:
            if ofWhatSensor == self.CylinderSensorIn:
                command = self.CylinderSensorInCommand
            elif ofWhatSensor == self.CylinderSensorOut:
                command = self.CylinderSensorOutCommand
            elif ofWhatSensor == self.CalibrateSensor:
                command = self.CalibrateSensor

            #for TravelNestAndTouch
            elif ofWhatSensor == self.TouchA:
                command = self.TouchASensor
            elif ofWhatSensor == self.TouchB:
                command = self.TouchBSensor
            elif ofWhatSensor == self.TouchC:
                command = self.TouchCSensor
            elif ofWhatSensor == self.TouchD:
                command = self.TouchDSensor
            elif ofWhatSensor == self.DUT1:
                command = self.DUT1Sensor
            elif ofWhatSensor == self.DUT2:
                command = self.DUT2Sensor

            elif ofWhatSensor==self.CheckDUT1:
                command = "%01#RCSX000E"
            elif ofWhatSensor==self.CheckDUT2:
                command = "%01#RCSX000F"

            ret = self.__readONorOFF(command)
            ret = int(ret)
            if ret == -1:
                self.strErrorMessage = "GetSensorStatus fail"
                return -1
            else:
                return ret
        except:
            self.strErrorMessage = "GetSensorStatus except fail"
            return -9999
    # ********************************************************************#

    # ********************************************************************#
    def Set_CylinderFunction(self, direction,timeout=10):
        try:
            # check z_axis safe
            ret = self.__readONorOFF(self.CheckZ)
            ret = int(ret)
            if ret != 1:
                self.strErrorMessage = "z_axis not safe"
                return -1
            if direction == self.Out:
                command = self.TrayCylinderOut_ON
                sensorCommand = self.CylinderSensorOut
                commandOff = self.TrayCylinderOut_OFF
                bNeedOff = 1
            elif direction == self.In:
                # check DUT1
                ret = self.TouchAndDUTLcokOrOpen(self.DUT1, self.DUT_LOCK)
                if ret != 0:
                    self.strErrorMessage = "DUT1 not LOCK completely"
                    return -1
                # # Read DUT1
                command = "%01#RCSX000E"
                ret_dut1 = self.__readONorOFF(command)
                ret_dut1 = int(ret_dut1)
                if ret_dut1 == -1:
                    self.strErrorMessage = "DUT1 sensor not feel"
                    return -1
                # Read DUT2
                command = "%01#RCSX000F"
                ret_dut2 = self.__readONorOFF(command)
                ret_dut2 = int(ret_dut2)
                if ret_dut2 == -1:
                    self.strErrorMessage = "DUT2 sensor not feel"
                    return -1
                # Read DUT3
                command = "%01#RCSX0308"
                ret_dut3 = self.__readONorOFF(command)
                ret_dut3 = int(ret_dut3)
                if ret_dut3 == -1:
                    self.strErrorMessage = "DUT3 sensor not feel"
                    return -1
                # Read DUT3
                command = "%01#RCSX0309"
                ret_dut4 = self.__readONorOFF ( command )
                ret_dut4 = int ( ret_dut4 )
                if ret_dut4 == -1:
                    self.strErrorMessage = "DUT4 sensor not feel"
                    return -1
                if not ((ret_dut1 or ret_dut2) or (ret_dut3 or ret_dut4)):
                    self.strErrorMessage = "DUT sensor not feel"
                    return -1

                command = self.TrayCylinderIn_ON
                sensorCommand = self.CylinderSensorIn
                commandOff = self.TrayCylinderIn_OFF
                bNeedOff = 1
            ret = self.__writeRead(command)
            if (ret != 0):
                self.strErrorMessage = "Set_CylinderFunction write commandon fail"
                return -1

            myTimeCount = 0
            while(myTimeCount < timeout):
                ret = self.GetSensorStatus(sensorCommand)
                if ret == -1:
                    return -1
                elif ret == 0:
                    time.sleep(0.5)
                    myTimeCount = myTimeCount + 0.5
                    continue
                elif ret == 1:
                    break
            if myTimeCount >= timeout:
                return -1
                self.strErrorMessage = "Set_CylinderFunction timeout"
            if(bNeedOff == 1):
                ret = self.__writeRead(commandOff)
                if (ret != 0):
                    self.strErrorMessage = "Set_CylinderFunction write commandoff fail"
                    return -1
                else:
                    return 0
            # if direction == self.Out:
            #     # check DUT1
            #     ret = self.TouchAndDUTLcokOrOpen(self.DUT1, self.DUT_OPEN)
            #     if ret != 0:
            #         self.strErrorMessage = "DUT1 not OPEN completely"
            #         return -1
            #     # check DUT2
            #     ret = self.TouchAndDUTLcokOrOpen(self.DUT2, self.DUT_OPEN)
            #     if ret != 0:
            #         self.strErrorMessage = "DUT2 not OPEN completely"
            #         return -1
            # return 0
        except:
            self.strErrorMessage = "Set_CylindeFunction except fail"
            return -1
    # ********************************************************************#
    # ********************************************************************#


    # Read Sensors
    def GetVer(self):
        if (self.myPLCSerialPort.isOpen() == False):
            self.strErrorMessage = "The serial port is not opened"
            return -1
        #PLC Version
        PLCcommand = '%01#RDD0030000302'
        #Server version
        # Sercommand = '%01#RDD0035000351'
        PLcver = self.__readVer(PLCcommand)
        # Server = self.__readONorOFF(Sercommand)
        ver = 'PLCVer: ' + PLcver
        print ver
        ver = "PLCVer: 1.0"
        PLcver = str(PLcver)
        if (PLcver.__len__() < 1):
            self.strErrorMessage = "Getversion Read command fail"
            return -1
        return ver
    # ********************************************************************#
    # ********************************************************************************************#

    def SetLightCurtain(self, state):
        try:
            if (state == self.LightCurtainOn):
                command = "%01#WCSR01300"

            elif (state == self.LightCurtainOff):
                command = "%01#WCSR01301"
            else:
                self.strErrorMessage = "SetLight curtain Input parameter error"
                return -1
            print "command = " + command
            ret = self.__writeRead(command)
            if (ret != 0):
                self.strErrorMessage = "SetLight curtain command fail"
                return -1
            return 0
        except:
            self.strErrorMessage = "SetLight curtain error"
            return -1

    # ********************************************************************************************#
    # ********************************************************************************************#

    # Set Left / Right LED Color
    def SetLedLightColor(self, ofWhichLED, ofWhatColor):
        try:
            if (self.myPLCSerialPort.isOpen() == False):
                self.strErrorMessage = "The serial port is not opened"
                return -1
            # Set DUT1 Color
            if (ofWhichLED == self.DUT1):
                # LEFT LED RED Color
                if (ofWhatColor == self.Red_OFF):
                    command = '%01#WCSR00850'
                elif (ofWhatColor == self.Red_ON):
                    command = '%01#WCSR00851'
                # LEFT LED Yellow Color
                elif (ofWhatColor == self.Yellow_OFF):
                    command = '%01#WCSR00860'
                elif (ofWhatColor == self.Yellow_ON):
                    command = '%01#WCSR00861'
                # LEFT LED Green Color
                elif (ofWhatColor == self.Green_OFF):
                    command = '%01#WCSR00870'
                elif (ofWhatColor == self.Green_ON):
                    command = '%01#WCSR00871'
                else:
                    self.strErrorMessage = "Input parameter error"
                    return -1  # Color Parameter Error
            # Set DUT2 Color
            if (ofWhichLED == self.DUT2):
                # LEFT LED RED Color
                if (ofWhatColor == self.Red_OFF):
                    command = '%01#WCSR008A0'
                elif (ofWhatColor == self.Red_ON):
                    command = '%01#WCSR008A1'
                # LEFT LED Yellow Color
                elif (ofWhatColor == self.Yellow_OFF):
                    command = '%01#WCSR008B0'
                elif (ofWhatColor == self.Yellow_ON):
                    command = '%01#WCSR008B1'
                # LEFT LED Green Color
                elif (ofWhatColor == self.Green_OFF):
                    command = '%01#WCSR008C0'
                elif (ofWhatColor == self.Green_ON):
                    command = '%01#WCSR008C1'
                else:
                    self.strErrorMessage = "Input parameter error"
                    return -1  # Color Parameter Error
            # Set DUT3 Color
            if (ofWhichLED == self.DUT3):
                # LEFT LED RED Color
                if (ofWhatColor == self.Red_OFF):
                    command = '%01#WCSR01200'
                elif (ofWhatColor == self.Red_ON):
                    command = '%01#WCSR01201'
                # LEFT LED Yellow Color
                elif (ofWhatColor == self.Yellow_OFF):
                    command = '%01#WCSR01210'
                elif (ofWhatColor == self.Yellow_ON):
                    command = '%01#WCSR01211'
                # LEFT LED Green Color
                elif (ofWhatColor == self.Green_OFF):
                    command = '%01#WCSR01220'
                elif (ofWhatColor == self.Green_ON):
                    command = '%01#WCSR01221'
                else:
                    self.strErrorMessage = "Input parameter error"
                    return -1  # Color Parameter Error

            # Set DUT4 Color
            if (ofWhichLED == self.DUT4):
                # LEFT LED RED Color
                if (ofWhatColor == self.Red_OFF):
                    command = '%01#WCSR01230'
                elif (ofWhatColor == self.Red_ON):
                    command = '%01#WCSR01231'
                # LEFT LED Yellow Color
                elif (ofWhatColor == self.Yellow_OFF):
                    command = '%01#WCSR01240'
                elif (ofWhatColor == self.Yellow_ON):
                    command = '%01#WCSR01241'
                # LEFT LED Green Color
                elif (ofWhatColor == self.Green_OFF):
                    command = '%01#WCSR01250'
                elif (ofWhatColor == self.Green_ON):
                    command = '%01#WCSR01251'
                else:
                    self.strErrorMessage = "Input parameter error"
                    return -1  # Color Parameter Error
            ret = self.__writeRead(command)
            if (ret != 0):
                self.strErrorMessage = "Red command fail"
                return -1
            return ret
        except:
            self.strErrorMessage = "SetLedLightColor error"
            return -1  # Color Parameter Error

    # ********************************************************************#
    def LoadCalbrationInitialFile(self):
        try:
            # 1:Get initial calibration coordinate
            calInitialFile = os.getcwd() + "//CalibrationInitial.txt"
            if not os.path.exists(calInitialFile):
                self.strErrorMessage = "CalibrationInitial.txt does not exist"
                return -1
            with open(calInitialFile, "r") as reader:
                for line in reader.readlines():
                    index = line.find("=")
                    if index < 0:
                        continue
                    line = line.strip().strip('\n')
                    if "ZIncrementX" in line:
                        self.ZIncrementx = float(line[index + 1:])
                    elif "ZIncrementY" in line:
                        self.ZIncrementy = float(line[index + 1:])
                    elif "YAxisCalIncrementX" in line:
                        self.YAxisCalIncrementX = float(line[index + 1:])
                    elif "YAxisCalIncrementY" in line:
                        self.YAxisCalIncrementY = float(line[index + 1:])
                    elif "YAxisCalDecrementX" in line:
                        self.YAxisCalDecrementX = float(line[index + 1:])
                    elif "YAxisCalDecrementY" in line:
                        self.YAxisCalDecrementY = float(line[index + 1:])
                    elif "XAxisCalIncrementX" in line:
                        self.XAxisCalIncrementX = float(line[index + 1:])
                    elif "XAxisCalIncrementY" in line:
                        self.XAxisCalIncrementY = float(line[index + 1:])
                    elif "XAxisCalDecrementX" in line:
                        self.XAxisCalDecrementX = float(line[index + 1:])
                    elif "XAxisCalDecrementY" in line:
                        self.XAxisCalDecrementY = float(line[index + 1:])
                reader.close()
            return 0
        except:
            self.strErrorMessage = "Set_CylindeFunction except fail"
            return -1

    # ********************************************************************#

    # ********************************************************************#
    def Calibrate(self,ofWhichAxis, incrementOrDecrement):
        try:
            shouldCalibrate = 1
            LoopCounter = 0
            Coordinates = 0.0
            isSuccess = 0
            if ("increment" in incrementOrDecrement):
                StepValue = 0.1 #0.05
            if ("decrement" in incrementOrDecrement):
                StepValue = -0.1 #-0.05
            ret = self.SetStepValue(self.Axis_x, StepValue)
            if ret != 0:
                return -1
            ret = self.SetStepValue(self.Axis_y, StepValue)
            if ret != 0:
                return -1
            ret = self.SetStepValue(self.Axis_z, StepValue)
            if ret != 0:
                return -1

            while (shouldCalibrate):
                err = self.GetSensorStatus(self.CalibrateSensor)
                if(err == -1):
                    return -1
                elif(err == 0):
                    if("increment" in incrementOrDecrement):
                        ret = self.MoveStep(ofWhichAxis)
                        if(ret == -1):
                            return -1
                    elif("decrement" in incrementOrDecrement):
                        ret = self.MoveStep(ofWhichAxis)
                        if(ret == -1):
                            return -1
                elif(err == 1):
                    if ("increment" in incrementOrDecrement):
                        ret = self.SetStepValue(ofWhichAxis, float(-3*StepValue))
                        ret = self.MoveStep(ofWhichAxis)
                        if ret == -1:
                            return -1
                    elif("decrement" in incrementOrDecrement):
                        ret = self.SetStepValue(ofWhichAxis, float(-3*StepValue))
                        ret = self.MoveStep(ofWhichAxis)
                        if ret == -1:
                            return -1
                    LoopCounter = LoopCounter + 1
                    if (LoopCounter == 1):
                        StepValue = StepValue/5.00
                    elif (LoopCounter == 2):
                        ret = self.GetCurrentCoordinates(ofWhichAxis)
                        if(ret == -9999):
                            return -1
                        else:
                            return float(ret)
                    #add back step

                    ret = self.SetStepValue(self.Axis_x, StepValue)
                    if ret != 0:
                        return -1
                    ret = self.SetStepValue(self.Axis_y, StepValue)
                    if ret != 0:
                        return -1
                    ret = self.SetStepValue(self.Axis_z, StepValue)
                    if ret != 0:
                        return -1
        except:
            self.strErrorMessage = "Calibrate error"
            return -1

    # ********************************************************************#

    # ********************************************************************#
    def Calibration(self,*args,**kwargs):
        try:
            # self.SetUpx = kwargs["Upx"]
            # self.SetUpy = kwargs["Upy"]
            # self.SetLeftx = kwargs["Leftx"]
            # self.SetLefty = kwargs["Lefty"]
            # self.SetDownx = kwargs["Downx"]
            # self.SetDowny = kwargs["Downy"]
            # self.SetRightx = kwargs["Rightx"]
            # self.SetRighty = kwargs["Righty"]
            # self.SetZx = kwargs["Zx"]
            # self.SetZy = kwargs["Zy"]
            # self.offset = kwargs["offset"]

            #1:Load cal initial file
            ret = self.LoadCalbrationInitialFile()
            if ret != 0:
                return -1

            #3:set speed
            ret = self.SetSpeed(self.Axis_xyz,15)
            if ret != 0:
                return -1

            #4:calibrate z axis
            print self.ZIncrementx,self.ZIncrementy
            ret = self.SynchronousXY(self.ZIncrementx,self.ZIncrementy)
            if ret != 0:
                return -1

            #2:z axis move
            ret = self.MoveToCoordinates(self.Axis_z,0)
            if ret != 0:
                return -1

            CalibrationBlockHeight = self.offset
            Zvsl_Finsl = self.Calibrate(self.Axis_z, "increment")
            #Zvsl_Finsl = Zvsl_Finsl + CalibrationBlockHeight
            Zvsl_Finsl = Zvsl_Finsl
            if (Zvsl_Finsl == -1):
                print "Z axis calibration error"
                return -1
            else:
                print "Z axis calibration value=" + str(Zvsl_Finsl)



            #5:calibrate x axis
            ret = self.MoveToCoordinates(self.Axis_z, 0)
            if ret != 0:
                return -1
            ret = self.SynchronousXY(self.XAxisCalDecrementX, self.XAxisCalDecrementY)
            if ret != 0:
                return -1
            ret = self.MoveToCoordinates(self.Axis_z, Zvsl_Finsl + 3.5)
            if ret != 0:
                return -1
            Xvsl_Dec = self.Calibrate(self.Axis_x, "decrement")
            if (Xvsl_Dec == -1):
                print "Z axis calibration error"
                return -1
            ret = self.SynchronousXY(self.XAxisCalDecrementX, self.XAxisCalDecrementY)
            if ret != 0:
                return -1

            ret = self.MoveToCoordinates(self.Axis_z, 0)
            if ret != 0:
                return -1
            ret = self.SynchronousXY(self.XAxisCalIncrementX, self.XAxisCalIncrementY)
            if ret != 0:
                return -1
            ret = self.MoveToCoordinates(self.Axis_z, Zvsl_Finsl + 3.5)
            if ret != 0:
                return -1
            Xvsl_Inc = self.Calibrate(self.Axis_x, "increment")
            if (Xvsl_Inc == -1):
                print "Y axis calibration error"
                return -1
            Xvsl_Finsl = (Xvsl_Inc+Xvsl_Dec)/2
            print Xvsl_Finsl
            ret = self.SynchronousXY(self.XAxisCalIncrementX, self.XAxisCalIncrementY)
            if ret != 0:
                return -1
            ret = self.MoveToCoordinates(self.Axis_z, 0)
            if ret != 0:
                return -1


            #6:calibrate y axis
            ret = self.SynchronousXY(self.YAxisCalDecrementX, self.YAxisCalDecrementY)
            if ret != 0:
                return -1
            ret = self.MoveToCoordinates(self.Axis_z, Zvsl_Finsl + 3.5)
            if ret != 0:
                return -1
            Yvsl_Dec = self.Calibrate(self.Axis_y, "decrement")
            if (Yvsl_Dec == -1):
                print "Y axis calibration error"
                return -1
            ret = self.SynchronousXY(self.YAxisCalDecrementX, self.YAxisCalDecrementY)
            if ret != 0:
                return -1
            ret = self.MoveToCoordinates(self.Axis_z, 0)
            if ret != 0:
                return -1



            ret = self.SynchronousXY(self.YAxisCalIncrementX, self.YAxisCalIncrementY)
            if ret != 0:
                return -1
            ret = self.MoveToCoordinates(self.Axis_z, Zvsl_Finsl + 3.5)
            if ret != 0:
                return -1
            Yvsl_Inc = self.Calibrate(self.Axis_y, "increment")
            if (Yvsl_Inc == -1):
                print "Z axis calibration error"
                return -1
            Yvsl_Finsl = (Yvsl_Inc+Yvsl_Dec)/2
            print Yvsl_Finsl
            ret = self.SynchronousXY(self.YAxisCalIncrementX, self.YAxisCalIncrementY)
            if ret != 0:
                return -1
            ret = self.MoveToCoordinates(self.Axis_z, 0)
            if ret != 0:
                return -1
            ret = self.SynchronousXY(self.ZIncrementx, self.ZIncrementy)
            if ret != 0:
                return -1

            #7:writr file
            output = open("calibration.txt", 'a')
            output.write("calibrationx =" + str(Xvsl_Finsl) + "\n")
            output.write("calibrationy =" + str(Yvsl_Finsl) + "\n")
            output.write("calibrationz =" + str(Zvsl_Finsl) + "\n")
            output.close()
            return 0
        except:
            self.strErrorMessage = "Calibration except fail"
            return -1
    # ********************************************************************#

    # ********************************************************************#
    def FixtureStatus(self):
        try:
            if CurtainSensorStatus == True:
                command = self.CurtainSensorCommand
                CurtainSensorCommandRet = self.__readONorOFF(command)
                CurtainSensorCommandRet = int(ret)
                if CurtainSensorCommandRet == 0:
                    return -2  #something had touched curtain
                if CurtainSensorCommandRet == -1:
                    self.strErrorMessage = "FixtureStatus fail"
                    return -1
                command = self.EStopStatusCommand
                EStopStatusCommandRet = self.__readONorOFF(command)
                EStopStatusCommandRet = int(ret)
                if EStopStatusCommandRet == 0:
                    return -3  #Had puss E-Stop button
                if EStopStatusCommandRet == -1:
                    self.strErrorMessage = "FixtureStatus fail"
                    return -1
                else:
                    return 1
            else:
                return -2
        except:
            self.strErrorMessage = "Fixture status except fail"
            return -1

    # __readONorOFF function
    def __readVer(self, command):
        bcc = self.__bccValue(command)
        command = command + bcc + '\r'
        command = command.upper()
        self.myPLCSerialPort.write(command)
        readString = self.ReadData(0.1)  # self.ser.readline()
        if ("fail" in readString):
            return -1
        readState1 = readString[6:8]
        readState2 = readString[8:10]
        s1 = binascii.a2b_hex(readState1)
        s2 = binascii.a2b_hex(readState2)
        ver = s1 + '.' + s2
        return ver

    # flip Byte Function
    def __flipByte(self, code):
        code = float(code)
        code = code * 5000.0 / 5.0
        X = binascii.hexlify(struct.pack('>i', code))

        byte1 = X[0:2]
        byte2 = X[2:4]
        byte3 = X[4:6]
        byte4 = X[6:8]
        finalbyte = byte4 + byte3 + byte2 + byte1
        finalbyte = finalbyte.upper()
        return finalbyte
    # **************************************************************#

    # **************************************************************#
    # Write and Read Command
    def __writeRead(self, command):
        try:
            bcc = self.__bccValue(command)
            command = command + bcc + '\r'
            command = command.upper()
            self.myPLCSerialPort.write(command)
            readString = self.ReadData(0.1)
            if (readString[3] == '$'):
                return 0
            else:
                return -1
        except:
            return -1
    # **************************************************************#


    # **************************************************************#
    # Get BCC Value
    def __bccValue(self, code):
        code1 = ord(code[0])
        code2 = ord(code[1])
        bcc = code1 ^ code2
        for i in range(code.__len__() - 2):
            codetem = ord(code[i + 2])
            bcc = bcc ^ codetem
        bcc = binascii.hexlify(struct.pack('>i', bcc))
        bcc = bcc[6:8]
        return bcc
    # **************************************************************#


    # **************************************************************#
    #read data
    def ReadData(self,timeDelay):
        try:
            for i in range(0, 5, 1):
                time.sleep(timeDelay)
                readString = self.myPLCSerialPort.read_all()
                if (len(readString) > 1):
                    return readString
            return "fail"
        except:
            self.strErrorMessage = "ReadData except fail"
            return "except fail"
    # **************************************************************#



    # **************************************************************#

    # **************************************************************#
    # __getValueOfByte function
    def __getValueOfByte(self, ByteString):
        finalbyte = ByteString[6:14]
        byte1 = finalbyte[0:2]
        byte2 = finalbyte[2:4]
        byte3 = finalbyte[4:6]
        byte4 = finalbyte[6:8]
        finalbyte = byte4 + byte3 + byte2 + byte1
        # finalbyte = int(finalbyte, 16)
        # finalbyte = struct.unpack('!i', finalbyte.decode('hex'))[0]
        finalbyte = struct.unpack('!i', binascii.unhexlify(finalbyte))[0]
        finalbyte = float(finalbyte)
        Value = finalbyte * 5.0 / 5000.0
        return Value
     # **************************************************************#


    # **************************************************************#
    # __readONorOFF function
    def __readONorOFF(self, command):
        bcc = self.__bccValue(command)
        command = command + bcc + '\r'
        command = command.upper()
        self.myPLCSerialPort.write(command)
        readString = self.ReadData(0.1)  # self.ser.readline()
        if ("fail" in readString):
            return -1
        readState = readString[6]
        return readState
    # **************************************************************#