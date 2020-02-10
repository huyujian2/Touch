#Tony modify : 2019-8-29

import os
import sys,os
import math
import fileinput
import binascii
from os import walk
from ast import literal_eval


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
    # defined Class Variables
    X_axis = 100
    Y_axis = 200
    Z_axis = 300
    XY_axis = 400
    XYZ_axis = 401

    #To set Z axis limit
    ZAxisX1Limit = 402
    ZAxisX2Limit = 403
    ZAxisY1Limit = 404
    ZAxisY2Limit = 405
    ZAxisY3Limit = 406
    ZAxisY4Limit = 407

    USBSensor = 408
    DCSensor = 409
    DUT1 = 500
    DUT2 = 501
    DUT3 = 502
    DUT4 = 503
    Set_DM_5V_ON = 504
    Set_DM_5V_OFF = 505
    DUT_LOCK = 506
    DUT_OPEN= 507

    Cylinder_IN = 508
    Cylinder_OUT = 509

    EStopOn = 510
    EStopOff = 511
    LightCurtainOn = 519
    LightCurtainOff = 520

    Cylinder_UP = 512
    Cylinder_DOWN = 513
    Cylinder_LOCK = 514
    Cylinder_OPEN = 515

    Alarm_On = 516
    Alarm_Off = 517
    DUTALL = 518

    StartButtonsTrigger = 529

    Max_limit = 1100
    Min_limit = 1200

    DUT_In = 2100
    DUT_Out = 2200
    DUTRight_In = 2110
    DUTRight_Out = 2210

    LED_Left = 3100
    LED_Right = 3200

    Red_OFF = 4101
    Red_ON = 4100
    Yellow_OFF = 4201
    Yellow_ON = 4200
    Green_ON = 4301
    Green_OFF = 4300

    USBLeft_ON = 5101
    USBLeft_OFF = 5100
    USBRight_ON = 5201
    USBRight_OFF = 5200

    Sensor_X_Max = 6100
    Sensor_X_Min = 6110
    Sensor_X_Origin = 6120

    Sensor_Y_Max = 6200
    Sensor_Y_Min = 6210
    Sensor_Y_Origin = 6220

    Sensor_Z_Max = 6300
    Sensor_Z_Min = 6310
    Sensor_Z_Origin = 6320

    Sensor_LeftHolder_In = 6400
    Sensor_LeftHolder_Out = 6410
    Sensor_RightHolder_In = 6500
    Sensor_RightHolder_Out = 6510

    Sensor_LeftDUT = 6600
    Sensor_RightDUT = 6700

    Sensor_Curtain = 6800

    Sensor_Calibrate = 6900 # %01#RCSX001F
    Sensor_TouchFinger = 7000

    SerialPortOpen = False

    myTollerance = 0.0000001
    myWaitTime = 0.1
    strErrorMessage ="ok"

    #add new sensor
    CylinderINSensor = 7001
    CylinderOUTSensor = 7002
    FingerprintWorkSensor = 7004
    DUTLockSensor = 7005
    USBSensor = 7006
    DCSensor = 7007
    CheckDUT1Sensor = 7010
    CheckDUT2Sensor = 7011
    CheckDUT3Sensor = 7012
    CheckDUT4Sensor = 7013
    OSS1CheckSensor = 7014
    OSS2CheckSensor = 7015
    OSS3CheckSensor = 7016
    OSS4CheckSensor = 7017
    USBALLSensor = 7018
    RUNPatternSensor = 7019

    XAxisCalibration = 0
    YAxisCalibration = 0
    ZAxisCalibration = 0

    bFirstRunFunction = True
    bDrawCircle = False
    bDisableUSBSensor = False

    ZAxisMaxLimit = 0
    ZAxisMinLimit = 0
    XAxisMaxLimit = 0
    XAxisMinLimit = 0
    YAxisMaxLimit = 0
    YAxisMinLimit = 0

    Pin1 = 1
    Pin2 = 2
    Pin3 = 3

    USBLock = 4
    USBUnlock = 5

    DCLock = 6
    DCUnlock = 7

    LigentSerialPort = None

    LigentSerialPortName = ""

    # *********************add L240T device command********************************#
    command_line1 = '010306000002C483'
    command_line2 = '0103061400028487'
    command_line3 = '010306280002448B'
    command_line4 = '010306780002449A'
    command_lines = '01039C480008EA4A'
    command_SetLinesZero = '01100652000204000000059CE9'

    # *********************add L240T device command********************************#

    def SetUSBSensorFlag(self, state):
        self.bDisableUSBSensor = state

    def DrawCicleFlag(self,state):
        self.bDrawCircle = state

    def RestAllFunction(self):
        try:
            for i in  range(0,33,1):
                if(i == 0):
                    command = "%01#WCSR00200"#Set Step Size X +
                    strMessage = "Set Step Size X + error"
                elif(i == 1):
                    command = "%01#WCSR00210"#Set Step Size X -
                    strMessage = "Set Step Size X - error"
                elif(i == 2):
                    command = "%01#WCSR00240"#Set Step Size Y -
                    strMessage = "Set Step Size Y + error"
                elif(i == 3):
                    command = "%01#WCSR00250"#Set Step Size Y -
                    strMessage = "Set Step Size Y - error"
                elif(i == 4):
                    command = "%01#WCSR00280"#Set Step Size Z +
                    strMessage = "Set Step Size Z + error"
                elif(i == 5):
                    command = "%01#WCSR00290"#Set Step Size Z -
                    strMessage = "Set Step Size Z - error"
                elif(i == 6):
                    command = "%01#WCSR002F0"#Syn Move X&Y
                    strMessage = "Syn Move X&Y error"
                elif(i == 7):
                    command = "%01#WCSR002C0"#Asyn Move X
                    strMessage = "Asyn Move X error"
                elif(i == 8):
                    command = "%01#WCSR002D0"#Asyn Move Y
                    strMessage = "Asyn Move Y error"
                elif(i == 9):
                    command = "%01#WCSR002E0"#Asyn Move Z
                    strMessage = "Asyn Move Z error"
                elif(i == 10):
                    command = "%01#WCSR00770"#Set Cylinder1 IN
                    strMessage = "Set Cylinder1 IN error"
                elif(i == 11):
                    command = "%01#WCSR00790"#Set Cylinder1 OUT
                    strMessage = "Set Cylinder1 OUT error"
                elif(i == 12):
                    command = "%01#WCSR00780"#Set Cylinder2 Down
                    strMessage = "Set Cylinder2 Down error"
                elif(i == 13):
                    command = "%01#WCSR01100"#DUT Lock
                    strMessage = "DUT Lock error"
                elif(i == 14):
                    command = "%01#WCSR01120"#DUT USB 1
                    strMessage = "DUT USB 1 error"
                elif (i == 15):
                    command = "%01#WCSR01140"#DUT USB 2
                    strMessage = "DUT USB 2 error"
                elif (i == 16):
                    command = "%01#WCSR01160"#DUT USB 3
                    strMessage = "DUT USB 3 error"
                elif (i == 17):
                    command = "%01#WCSR01180"#DUT USB 4
                    strMessage = "DUT USB 4 error"
                elif (i == 18):
                    command = "%01#WCSR00850"#Set Red OFF DUT1
                    strMessage = "Set Red OFF DUT1 error"
                elif (i == 19):
                    command = "%01#WCSR00860"#Set Yellow OFF DUT1
                    strMessage = "Set Yellow OFF DUT1 error"
                elif (i == 20):
                    command = "%01#WCSR00870"#Set Green OFF DUT1
                    strMessage = "Set Green OFF DUT1 error"
                elif (i == 21):
                    command = "%01#WCSR008A0"#Set Red OFF DUT2
                    strMessage = "Set Red OFF DUT2 error"
                elif (i == 22):
                    command = "%01#WCSR008B0"#Set Yellow OFF DUT2
                    strMessage = "Set Yellow OFF DUT2 error"
                elif (i == 23):
                    command = "%01#WCSR008C0"#Set Green OFF DUT2
                    strMessage = "Set Green OFF DUT2 error"
                elif (i == 24):
                    command = "%01#WCSR01200"#Set Red OFF DUT3
                    strMessage = "Set Red OFF DUT3 error"
                elif (i == 25):
                    command = "%01#WCSR01210"#Set Yellow OFF DUT3
                    strMessage = "Set Yellow OFF DUT3 error"
                elif (i == 26):
                    command = "%01#WCSR01220"#Set Green OFF DUT3
                    strMessage = "Set Green OFF DUT3 error"
                elif (i == 27):
                    command = "%01#WCSR01230"#Set Red OFF DUT4
                    strMessage = "Set Red OFF DUT4 error"
                elif (i == 28):
                    command = "%01#WCSR01240"#Set Yellow OFF DUT4
                    strMessage = "Set Yellow OFF DUT4 error"
                elif (i == 29):
                    command = "%01#WCSR01250"#Set Green OFF DUT4
                    strMessage = "Set Green OFF DUT4 error"
                elif (i == 30):
                    command = "%01#WCSR00990"#Set E-STOP OFF
                    strMessage = "Set E-STOP OFF error"
                elif (i == 31):
                    command = "%01#WCSR00800"#4 USB OPEN ALL
                    strMessage = "4 USB OPEN ALL error"
                elif (i == 32):
                    command = "%01#WCSR00320"#4 USB OPEN ALL
                    strMessage = "Draw circle address error"


                bcc = self.__bccValue(command)
                command = command + bcc + '\r'
                command = command.upper()
                self.ser.write(command)
                time.sleep(0.01)
                readString = self.ReadData(0.1)
                if (readString[3] != '$'):
                    return -1
        except:
            self.strErrorMessage =  "RestFunction fail"
            return -1


    #DOE dot
    def DotFunction(self,dotXPosition,dotYPosition,dotZPosition,times):
        try:
            err = self.MoveToCoordinates(self.Z_axis,0,5)
            if (err != 0):
                return -1
            for i in range(0,times,1):
                err = self.MoveToCoordinates(self.X_axis,dotXPosition,5)
                if (err != 0):
                    return -1
                err = self.MoveToCoordinates(self.Y_axis,dotYPosition,5)
                if (err != 0):
                    return -1
                err = self.MoveToCoordinates(self.Z_axis,dotZPosition,5)
                if (err != 0):
                    return -1
                err = self.MoveToCoordinates(self.Z_axis, 0,5)
                if (err != 0):
                    return -1
                err = self.MoveToCoordinates(self.X_axis, 0,5)
                if (err != 0):
                    return -1
                err = self.MoveToCoordinates(self.Y_axis, 0,5)
                if (err != 0):
                    return -1
            return 0
        except:
            return -1

    #read data
    def ReadData(self,timeDelay):
        bReadData = False
        for i in range(0, 1, 1):
            readString = self.ser.readline()
            time.sleep(timeDelay)
            if(len(readString) > 1):
                return readString
            else:
                continue
        if(bReadData == False):
            return "fail"

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

    # Write and Read Command
    def __writeRead(self, command):
        try:
            bcc = self.__bccValue(command)
            command = command + bcc + '\r'
            command = command.upper()
            self.ser.write(command)
            readString = self.ReadData(0.1)
            if (readString[3] == '$'):
                return 0
            else:
                return -1
        except:
            return -1

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

    # __getValueOfByte function
    def __getValueOfByte(self,ByteString):
        finalbyte = ByteString[6:14]
        byte1 = finalbyte[0:2]
        byte2 = finalbyte[2:4]
        byte3 = finalbyte[4:6]
        byte4 = finalbyte[6:8]
        finalbyte = byte4 + byte3 + byte2 + byte1
        #finalbyte = int(finalbyte, 16)
        #finalbyte = struct.unpack('!i', finalbyte.decode('hex'))[0]
        finalbyte = struct.unpack('!i', binascii.unhexlify(finalbyte))[0]
        finalbyte = float(finalbyte)
        Value = finalbyte * 5.0 / 5000.0
        return Value

    #__readONorOFF function
    def __readONorOFF(self,command):
        bcc = self.__bccValue(command)
        command = command + bcc + '\r'
        command = command.upper()
        self.ser.write(command)
        readString = self.ReadData(0.1)#self.ser.readline()
        if("fail" in readString):
            return -1
        readState = readString[6]
        return readState

    # __readONorOFF function
    def __readVer(self, command):
        bcc = self.__bccValue(command)
        command = command + bcc + '\r'
        command = command.upper()
        self.ser.write(command)
        readString = self.ReadData(0.1)  # self.ser.readline()
        if ("fail" in readString):
            return -1
        readState1 = readString[6:8]
        readState2 = readString[8:10]
        s1 = binascii.a2b_hex(readState1)
        s2 = binascii.a2b_hex(readState2)
        ver = s1 + '.' + s2
        return ver

    # __getCoordinatesFromFile function
    def __getCoordinatesFromFile(self,FilePath):
        FinalSplitLine = []
        with open(FilePath) as f:
            for line in f:
                splitline = line.rstrip().split('\r')
                FinalSplitLine = FinalSplitLine + splitline
            f.close()
            return FinalSplitLine

    # printHello function
    def printHello(self):
        print('Hello')



# ********************************************************************************#
    #ChooseCOM function
    def ChooseCOM(self,serialName):
        try:
            self.ser = serial.Serial(port=serialName,
                                    timeout=0.01,
                                    baudrate=115200,
                                    parity=serial.PARITY_ODD)
            if(self.ser.isOpen()):
                command = '%01#RDD0015400155'
                bcc = self.__bccValue(command)
                command = command + bcc + '\r'
                command = command.upper()
                self.ser.write(command)
                readStr = self.ReadData(0.1)
                if("fail" in readStr):
                    self.strErrorMessage = "ChooseCOM read command fail"
                    return -1
                else:
                    err = self.GetAllAxisLimit()
                    if(err == -1):
                        return -1
                    err = self.RestAllFunction()
                    if(err == -1):
                        return -1
                    # err = self.LoadLimitTXT()
                    # if(err == -1):
                    #     return -1
                    return 0
            else:
                return 1
        except:
            self.strErrorMessage =  "ChooseCOM fail"
            return -1



# ********************************************************************************#
    # Open Serial
    def OpenSerial(self):
        try:
            port_list = list(serial.tools.list_ports.comports())
            length = len(port_list)
            if(len(port_list) < 0):
                self.strErrorMessage = "fail:There is no serial port"
                return -1
            bFindSerialPort = False
            for i in range(0,length):
                err =  self.ChooseCOM(port_list[i].device)
                if(err == 0):
                    bFindSerialPort = True
                    return 0
                else:
                    continue
            if(bFindSerialPort == False):
                self.strErrorMessage = "There is no report"
                return -1
        except:
            self.strErrorMessage =  "Open serial port fail"
            return -1
        return 0


# ********************************************************************************#
    # Close Serial
    def CloseSerial(self):
        try:
            if(self.ser.isOpen):
                self.ser.close()
            return 0
        except:
            self.strErrorMessage =   "CloseSerial fail"
            return -1



 # ********************************************************************************#
    # Read current X / Y / Z coordinates X:100 Y:
    def GetCurrentCoordinates(self,ofWhatAxis):
        if(self.ser.isOpen() == False):
            self.strErrorMessage = "the serial port is not opened"
            return -9999
        try:
            if (ofWhatAxis == self.X_axis):
                command = '%01#RDD0014600147'
            elif(ofWhatAxis == self.Y_axis):
                command = '%01#RDD0015000151'
            elif(ofWhatAxis == self.Z_axis):
                command = '%01#RDD0015400155'
            bcc = self.__bccValue(command)
            command = command + bcc + '\r'
            command = command.upper()
            self.ser.write(command)

            # read data
            bGetDataFromPLC = False
            readString =  self.ReadData(0.1)
            if ("fail" in readString):
                self.strErrorMessage = "GetCurrentCoordinates timeout"
                return -9999
            else:
                value = self.__getValueOfByte(readString)
                return (value*10)
        except:
            self.strErrorMessage = "GetCurrentCoordinates error"
            return -9999

# ********************************************************************************#
    # Moving to specified Coordinates per Axis
    def MoveToCoordinates(self,ofWhatAxis,Value,timeout):
        if(self.ser.isOpen() == False):
            self.strErrorMessage =  "The serial port is not opened"
            return -1
        # Move X-Axis
        if (ofWhatAxis == self.X_axis):
            if (Value == self.GetCurrentCoordinates(self.X_axis)):
                return 0
            
            if (Value < self.XAxisMinLimit):
                Value = self.XAxisMinLimit
            if(Value > self.XAxisMaxLimit):
                Value = self.XAxisMaxLimit

            command = '%01#WDD0020200203'
            finalByte = self.__flipByte(Value)
            command = command + finalByte
            ret = self.__writeRead(command)
            if (ret == 0):
                moveCommand = '%01#WCSR002C1'
                ret = self.__writeRead(moveCommand)
                if(ret == 0):
                    mytimeCount = 0
                    command = "%01#RCSX0009"
                    bcc = self.__bccValue(command)
                    command = command + bcc + '\r'
                    self.ser.write(command)
                    time.sleep(0.2)
                    string = self.ser.read_all()
                    if int(string[6]) == 0:
                        self.strErrorMessage = "MoveToCoordinates action fail"
                        return -1
                    while (self.GetmoveSignal(self.X_axis) == 0):
                        command = "%01#RCSX0009"
                        bcc = self.__bccValue(command)
                        command = command + bcc + '\r'
                        self.ser.write(command)
                        time.sleep(0.2)
                        string = self.ser.read_all()
                        if int(string[6]) == 0:
                            self.strErrorMessage = "MoveToCoordinates action fail"
                            return -1
                        if (mytimeCount > timeout):
                            self.strErrorMessage = "MoveToCoordinates read command timeout"
                            return -1
                        time.sleep(self.myWaitTime)
                        mytimeCount += self.myWaitTime

                    moveCommand = '%01#WCSR002C0'
                    ret = self.__writeRead(moveCommand)
                    return 0
                else:
                    self.strErrorMessage = "MoveToCoordinates write command fail"
                    return -1
            else:
                self.strErrorMessage = "MoveToCoordinates write command fail"
                return -1

        # Move Y-Axis
        elif (ofWhatAxis == self.Y_axis):
            if (Value == self.GetCurrentCoordinates(self.Y_axis)):
                return 0

            if (Value < self.YAxisMinLimit):
                Value = self.YAxisMinLimit
            if(Value > self.YAxisMaxLimit):
                Value = self.YAxisMaxLimit
            command = '%01#WDD0021200213'
            finalByte = self.__flipByte(Value)
            command = command + finalByte
            ret = self.__writeRead(command)
            if (ret == 0):
                moveCommand = '%01#WCSR002D1'
                ret = self.__writeRead(moveCommand)
                if(ret == 0):
                    mytimeCount = 0
                    command = "%01#RCSX0009"
                    bcc = self.__bccValue(command)
                    command = command + bcc + '\r'
                    self.ser.write(command)
                    time.sleep(0.2)
                    string = self.ser.read_all()
                    if int(string[6]) == 0:
                        self.strErrorMessage = "MoveToCoordinates action fail"
                        return -1
                    while (self.GetmoveSignal(self.Y_axis) == 0):
                        command = "%01#RCSX0009"
                        bcc = self.__bccValue(command)
                        command = command + bcc + '\r'
                        self.ser.write(command)
                        time.sleep(0.2)
                        string = self.ser.read_all()
                        if int(string[6]) == 0:
                            self.strErrorMessage = "MoveToCoordinates action fail"
                            return -1
                        if (mytimeCount > timeout):
                            self.strErrorMessage = "MoveToCoordinates read command timeout"
                            return -1
                        time.sleep(self.myWaitTime)
                        mytimeCount += self.myWaitTime

                    moveCommand = '%01#WCSR002D0'
                    ret = self.__writeRead(moveCommand)
                    return 0
                else:
                    self.strErrorMessage = "MoveToCoordinates write command fail"
                    return -1
            else:
                self.strErrorMessage = "MoveToCoordinates write command fail"
                return -1

        # Move Z-Axis
        elif (ofWhatAxis == self.Z_axis):
            if (Value == self.GetCurrentCoordinates(self.Z_axis)):
                return 0

            if (Value < self.ZAxisMinLimit):
                Value = self.ZAxisMinLimit
            if(Value > self.ZAxisMaxLimit):
                Value = self.ZAxisMaxLimit
            command = '%01#WDD0022200223'
            finalByte = self.__flipByte(Value)
            command = command + finalByte
            ret = self.__writeRead(command)
            if (ret == 0):
                moveCommand = '%01#WCSR002E1'
                ret = self.__writeRead(moveCommand)
                if(ret == 0):
                    mytimeCount = 0
                    command = "%01#RCSX0009"
                    bcc = self.__bccValue(command)
                    command = command + bcc + '\r'
                    self.ser.write(command)
                    time.sleep(0.2)
                    string = self.ser.read_all()
                    if int(string[6]) == 0:
                        self.strErrorMessage = "MoveToCoordinates action fail"
                        return -1
                    while (self.GetmoveSignal(self.Z_axis) == 0):
                        command = "%01#RCSX0009"
                        bcc = self.__bccValue(command)
                        command = command + bcc + '\r'
                        self.ser.write(command)
                        time.sleep(0.2)
                        string = self.ser.read_all()
                        if int(string[6]) == 0:
                            self.strErrorMessage = "MoveToCoordinates action fail"
                            return -1
                        if (mytimeCount > timeout):
                            self.strErrorMessage = "MoveToCoordinates read command timeout"
                            return -1
                        time.sleep(self.myWaitTime)
                        mytimeCount += self.myWaitTime

                    moveCommand = '%01#WCSR002E0'
                    ret = self.__writeRead(moveCommand)
                    return 0
                else:
                    self.strErrorMessage = "MoveToCoordinates write command fail"
                    return -1
            else:
                self.strErrorMessage = "MoveToCoordinates write command fail"
                return -1
        else:
            self.strErrorMessage = "MoveToCoordinates input parameter eror"
            return -1

 # ********************************************************************************#
    #move x&y
    def SynchronousXY(self,xValue,yValue,timeout):
        try:
            if (xValue < self.XAxisMinLimit):
                xValue = self.XAxisMinLimit
            if(xValue > self.XAxisMaxLimit):
                xValue = self.XAxisMaxLimit
            if (yValue < self.YAxisMinLimit):
                yValue = self.YAxisMinLimit
            if(yValue > self.YAxisMaxLimit):
                yValue = self.YAxisMaxLimit

            command = '%01#WDD0020200203'
            finalByte = self.__flipByte(xValue)
            command = command + finalByte
            ret = self.__writeRead(command)
            if(ret != 0):
                self.strErrorMessage =  "SynchronousXY %01#WDD0020200203 fail"
                return -1
            command = '%01#WDD0021200213'
            finalByte = self.__flipByte(yValue)
            command = command + finalByte
            ret = self.__writeRead(command)
            if(ret != 0):
                self.strErrorMessage = "SynchronousXY %01#WDD0021200213 fail"
                return -1
            if(self.bDrawCircle == True):
                # command = '%01#WCSR00321'
                command = '%01#WCSR002F1'
            else:
                # command = '%01#WCSR00321'
                command = '%01#WCSR002F1'
            bcc = self.__bccValue(command)
            command = command + bcc + '\r'
            command = command.upper()
            ret = self.__writeRead(command)
            if(ret != 0):
                self.strErrorMessage = "SynchronousXY %01#WCSR002F1 fail"
                return -1
            else:
                mytimeCount = 0
                while (self.GetmoveSignal(self.X_axis) == 1):
                    if (mytimeCount > timeout):
                        self.strErrorMessage = "SynchronousXY time out"
                        return -1
                    time.sleep(self.myWaitTime)
                    mytimeCount += self.myWaitTime

                mytimeCount = 0
                while (self.GetmoveSignal(self.Y_axis) == 1):
                    if (mytimeCount > timeout):
                        self.strErrorMessage = "SynchronousXY time out"
                        return -1
                    time.sleep(self.myWaitTime)
                    mytimeCount += self.myWaitTime
                return 0
        except:
            self.strErrorMessage = "SynchronousXY fail"
            return -1

#********************************************************************************#
    # Set Increment / Decrement Value
    def SetStepValue(self,ofWhatAxis,Value):
        if(self.ser.isOpen() == False):
            self.strErrorMessage = "the serial port is not opened"
            return -1
        try:
            if (ofWhatAxis == self.X_axis):
                command = '%01#WDD0100001001'
            elif(ofWhatAxis == self.Y_axis):
                command = '%01#WDD0100801009'
            elif(ofWhatAxis == self.Z_axis):
                command = '%01#WDD0101601017'
            finalByte = self.__flipByte(Value)
            command = command + finalByte
            ret = self.__writeRead(command)
            if(ret == -1):
                self.strErrorMessage = "SetStepValue read command fail"
                return -1
            return ret
        except:
            self.strErrorMessage = "SetStepValue error"
            return -1
 # ********************************************************************************#

# ********************************************************************************#
    def GetStepValue(self, ofWhatAxis):
        try:
            if (ofWhatAxis == self.X_axis):
                command = "%01#RDD006000060054"
            elif(ofWhatAxis == self.Y_axis):
                command = "%01#RDD006020060254"
            elif(ofWhatAxis == self.Z_axis):
                command = "%01#RDD006040060454"
            bcc = self.__bccValue(command)
            command = command + bcc + '\r'
            command = command.upper()
            self.ser.write(command)
            #read data
            readString = self.ReadData(0.1)
            if("fail" in readString):
                self.strErrorMessage = "read data timeout"
                return -1
            value = self.__getValueOfByte(readString)
            return value
        except:
            self.strErrorMessage = "GetStepValue error"
            return -1

# ********************************************************************************#


    # Move Increment
    def MoveIncrement(self,ofWhatAxis):
        if(self.ser.isOpen() == False):
            self.strErrorMessage =  "The serial port is not opened"
            return -1
        try:
            if (ofWhatAxis == self.X_axis):
                command = '%01#WCSR00201'
            elif(ofWhatAxis == self.Y_axis):
                command = '%01#WCSR00241'
            elif(ofWhatAxis == self.Z_axis):
                command = '%01#WCSR00281'
            ret = self.__writeRead(command)
            if(ret == -1):
                self.strErrorMessage = "MoveIecrement read command fail"
                return -1
            timeout = 10
            if (ofWhatAxis == self.X_axis):
                # wait for x-axis is ready
                mytimeCount = 0
                while (self.GetmoveSignal(self.X_axis) == 1):
                    if (mytimeCount > timeout):
                        self.strErrorMessage = "MoveIecrement time out"
                        return -1
                    time.sleep(self.myWaitTime)
                    mytimeCount += self.myWaitTime

                xCurrentPosition = self.GetCurrentCoordinates(self.X_axis)
                if(xCurrentPosition == -9999):
                    return -1
                if(xCurrentPosition < (self.XAxisMinLimit+1) or xCurrentPosition > (self.XAxisMaxLimit-1)):
                    self.strErrorMessage = "X asix is exceed limit"
                    return -1

            elif (ofWhatAxis == self.Y_axis):
                mytimeCount = 0
                while (self.GetmoveSignal(self.Y_axis) == 1):
                    if (mytimeCount > timeout):
                        self.strErrorMessage = "MoveIecrement time out"
                        return -1
                    time.sleep(self.myWaitTime)
                    mytimeCount += self.myWaitTime

                yCurrentPosition = self.GetCurrentCoordinates(self.Y_axis)
                if(yCurrentPosition == -9999):
                    return -1
                if(yCurrentPosition < (self.YAxisMinLimit+1) or yCurrentPosition > (self.YAxisMaxLimit-1)):
                    self.strErrorMessage = "Y asix is exceed limit"
                    return -1

            elif (ofWhatAxis == self.Z_axis):
                print("start to move z")
                mytimeCount = 0
                while (self.GetmoveSignal(self.Z_axis) == 1):
                    print("move signal = " + str(self.GetmoveSignal(self.Z_axis)))
                    if (mytimeCount > timeout):
                        self.strErrorMessage = "Move Iecrement time out"
                        return -1
                    time.sleep(self.myWaitTime)
                    mytimeCount += self.myWaitTime

                zCurrentPosition = self.GetCurrentCoordinates(self.Z_axis)
                if(zCurrentPosition == -9999):
                    return -1
                if(zCurrentPosition < (self.ZAxisMinLimit+1) or zCurrentPosition > (self.ZAxisMaxLimit-1)):
                    self.strErrorMessage = "Z asix is exceed limit"
                    return -1
            return 0
        except:
            self.strErrorMessage = "MoveIncrement error"
            return -1

    # Move decrement
    def MoveDecrement(self,ofWhatAxis):
        if(self.ser.isOpen() == False):
            self.strErrorMessage = "the serial port is not opened"
            return -1
        try:
            if (ofWhatAxis == self.X_axis):
                command = '%01#WCSR00211'
            elif(ofWhatAxis == self.Y_axis):
                command = '%01#WCSR00251'
            elif(ofWhatAxis == self.Z_axis):
                command = '%01#WCSR00291'
            ret = self.__writeRead(command)
            if(ret == -1):
                self.strErrorMessage = "MoveDecrement read command fail"
                return -1
            timeout = 5
            if (ofWhatAxis == self.X_axis):
                # wait for x-axis is ready
                mytimeCount = 0
                while (self.GetmoveSignal(self.X_axis) == 1):
                    if (mytimeCount > timeout):
                        self.strErrorMessage = "MoveDecrement time out"
                        return -1
                    time.sleep(self.myWaitTime)
                    mytimeCount += self.myWaitTime

                xCurrentPosition = self.GetCurrentCoordinates(self.X_axis)
                if(xCurrentPosition == -9999):
                    return -1
                if(xCurrentPosition < (self.XAxisMinLimit+1) or xCurrentPosition > (self.XAxisMaxLimit-1)):
                    self.strErrorMessage = "X asix is exceed limit"
                    return -1
            elif (ofWhatAxis == self.Y_axis):
                mytimeCount = 0
                while (self.GetmoveSignal(self.Y_axis) == 1):
                    if (mytimeCount > timeout):
                        self.strErrorMessage = "MoveDecrement time out"
                        return -1
                    time.sleep(self.myWaitTime)
                    mytimeCount += self.myWaitTime

                yCurrentPosition = self.GetCurrentCoordinates(self.Y_axis)
                if(yCurrentPosition == -9999):
                    return -1
                if(yCurrentPosition < (self.YAxisMinLimit+1) or yCurrentPosition > (self.YAxisMaxLimit-1)):
                    self.strErrorMessage = "Y asix is exceed limit"
                    return -1
            elif (ofWhatAxis == self.Z_axis):
                mytimeCount = 0
                while (self.GetmoveSignal(self.Z_axis) == 1):
                    if (mytimeCount > timeout):
                        self.strErrorMessage = "MoveDecrement time out"
                        return -1
                    time.sleep(self.myWaitTime)
                    mytimeCount += self.myWaitTime

                zCurrentPosition = self.GetCurrentCoordinates(self.Z_axis)
                if(zCurrentPosition == -9999):
                    return -1
                if(zCurrentPosition < (self.ZAxisMinLimit+1) or zCurrentPosition > (self.ZAxisMaxLimit-1)):
                    self.strErrorMessage = "Z asix is exceed limit"
                    return -1
            return 0
        except:
            self.strErrorMessage = "MoveDecrement error"
            return -1

#********************************************************************************#
    # Set Motor Move Speed
    def SetSpeed(self,ofWhatAxis,Value):
        if(self.ser.isOpen() == False):
            self.strErrorMessage = "The serial port is not opened"
            return -1
        try:
            if (ofWhatAxis == self.X_axis):
                command = '%01#WDD0020000201'
            elif(ofWhatAxis == self.Y_axis):
                command = '%01#WDD0021000211'
            elif(ofWhatAxis == self.Z_axis):
                command = '%01#WDD0022000221'
            finalByte = self.__flipByte(Value)
            command = command + finalByte
            ret = self.__writeRead(command)
            if(ret == -1):
                self.strErrorMessage = "SetSpeed read command fail"
                return -1
            return ret
        except:
            self.strErrorMessage = "SetSpeed error"
            return -1
# ********************************************************************************#



# ********************************************************************************#
    # Get current motor move speed
    def GetSpeed(self,ofWhatAxis):
        if(self.ser.isOpen() == False):
            self.strErrorMessage = "The serial port is not opened"
            return -1
        try:
            command = ""
            if (ofWhatAxis == self.X_axis):
                command = '%01#RDD0020000200'
            elif(ofWhatAxis == self.Y_axis):
                command = '%01#RDD0021000210'
            elif(ofWhatAxis == self.Z_axis):
                command = '%01#RDD0022000220'
            bcc = self.__bccValue(command)
            command = command + bcc + '\r'
            command = command.upper()
            self.ser.write(command)

            #read data
            readString = self.ReadData(0.1)
            if("fail" in readString):
                self.strErrorMessage = "read data timeout"
                return -1
            value = self.__getValueOfByte(readString)
            return value
        except:
            self.strErrorMessage = "GetSpeed error"
            return  -1
# ********************************************************************************#




# ********************************************************************************************#
    # Get Limit of X / Y / Z axis
    def GetLimit(self,ofWhatAxis,ofWhatLimit):
        if(self.ser.isOpen() == False):
            self.strErrorMessage = "the serial port is not opened"
            return -9999
        try:
            # Get X-axis max / min limit
            if (ofWhatAxis == self.X_axis):
                if (ofWhatLimit == self.Max_limit):
                    command = '%01#RDD0062000621'
                elif (ofWhatLimit == self.Min_limit):
                    command = '%01#RDD0063000631'
                else:
                    self.strErrorMessage = "GetLimit input parameter is not correct"
                    return -9999
            # Get Y-axis max / min limit
            elif (ofWhatAxis == self.Y_axis):
                if (ofWhatLimit == self.Max_limit):
                    command = '%01#RDD0062200623'
                elif (ofWhatLimit == self.Min_limit):
                    command = '%01#RDD0063200633'
                else:
                    self.strErrorMessage = "GetLimit input parameter is not correct"
                    return -9999
            elif (ofWhatAxis == self.Z_axis):
                if (ofWhatLimit == self.Max_limit):
                    command = '%01#RDD0062400625'
                elif (ofWhatLimit == self.Min_limit):
                    command = '%01#RDD0063400635'
                else:
                    self.strErrorMessage = "GetLimit input parameter is not correct"
                    return -9999
            else:
                self.strErrorMessage = "GetLimit input parameter is not correct"
                return -9999

            #write data
            bcc = self.__bccValue(command)
            command = command + bcc + '\r'
            command = command.upper()
            self.ser.write(command)

            #read data
            readString = self.ReadData(0.1)
            if("fail" in readString):
                self.strErrorMessage = "read data timeout"
                return -9999
            else:
                value = self.__getValueOfByte(readString)
                return (value*10)
        except:
            self.strErrorMessage = "GetLimit error"
            return -9999
#********************************************************************************************#




# ********************************************************************************************#
    # Set Left / Right LED Color
    def SetLedLightColor(self,ofWhichLED,ofWhatColor):
        try:
            if(self.ser.isOpen() == False):
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
                    return -1 # Color Parameter Error
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
                    return -1 # Color Parameter Error
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
            if(ret != 0):
                self.strErrorMessage = "Red command fail"
                return -1
            return ret
        except:
            self.strErrorMessage = "SetLedLightColor error"
            return -1  # Color Parameter Error
# ********************************************************************************************#




 # ********************************************************************************************#
    # Read Sensors
    def GetSensorStatus(self,ofWhatSensor):
        if(self.ser.isOpen() == False):
            self.strErrorMessage =  "The serial port is not opened"
            return -1
        # X-axis Sensor
        if (ofWhatSensor == self.Sensor_X_Origin):
            command = '%01#RCSX0018'
        elif (ofWhatSensor == self.Sensor_X_Max):
            command = '%01#RCSX001A'
        elif (ofWhatSensor == self.Sensor_X_Min):
            command = '%01#RCSX0019'
        # Y-axis Sensor
        elif (ofWhatSensor == self.Sensor_Y_Origin):
            command = '%01#RCSX0015'
        elif (ofWhatSensor == self.Sensor_Y_Max):
            command = '%01#RCSX0017'
        elif (ofWhatSensor == self.Sensor_Y_Min):
            command = '%01#RCSX0016'
        # Z-axis Sensor
        elif (ofWhatSensor == self.Sensor_Z_Origin):
            command = '%01#RCSX001B'
        elif (ofWhatSensor == self.Sensor_Z_Max):
            command = '%01#RCSX001D'
        elif (ofWhatSensor == self.Sensor_Z_Min):
            command = '%01#RCSX001C'
        elif (ofWhatSensor == self.CylinderINSensor):
            command = '%01#RCSX0011'
        elif (ofWhatSensor == self.CylinderOUTSensor):
            command = '%01#RCSX0012'
        elif (ofWhatSensor == self.Sensor_Curtain):
            command = '%01#RCSX0010'
        elif (ofWhatSensor == self.FingerprintWorkSensor):
            command = '%01#RCSX000E'
        elif (ofWhatSensor == self.DUTLockSensor):
            command = '%01#RCSX000F'
        elif (ofWhatSensor == self.USBSensor):
            command = '%01#RCSR021B'
        elif (ofWhatSensor == self.DCSensor):
            command = '%01#RCSR021C'
        elif (ofWhatSensor == self.CheckDUT1Sensor):
            command = '%01#RCSX0304'
        elif (ofWhatSensor == self.CheckDUT2Sensor):
            command = '%01#RCSX0305'
        elif (ofWhatSensor == self.CheckDUT3Sensor):
            command = '%01#RCSX0306'
        elif (ofWhatSensor == self.CheckDUT4Sensor):
            command = '%01#RCSX0307'
        elif (ofWhatSensor == self.OSS1CheckSensor):
            command = '%01#RCSX0308'
        elif (ofWhatSensor == self.OSS2CheckSensor):
            command = '%01#RCSX0309'
        elif (ofWhatSensor == self.OSS3CheckSensor):
            command = '%01#RCSX030A'
        elif (ofWhatSensor == self.OSS4CheckSensor):
            command = '%01#RCSX030B'
        elif (ofWhatSensor == self.Sensor_TouchFinger):
            command = '%01#RCSX001E'
        elif (ofWhatSensor == self.Sensor_Calibrate):
            command = '%01#RCSX001F'
        elif (ofWhatSensor == self.USBALLSensor):
            command = '%01#RCSR0081'#ALL IN
        elif (ofWhatSensor == self.RUNPatternSensor):
            command = '%01#RCSR0001'
        else:
            self.strErrorMessage = "GetSensorStatus Input parameter error"
            return -1
        ret = self.__readONorOFF(command)
        ret = int(ret)
        if(ret == -1):
            self.strErrorMessage = "GetSensorStatus Read command fail"
            return -1
        return ret
# ********************************************************************************************#

    # ********************************************************************************************#
    # press two green buttons to trigger start, equals to click "Start" at Clifford
    # 1 --> two buttons pressed down, start triggered;
    # 0 --> two buttons don't triggered;
    def StartButtonsTriggered(self,action):
        try:
            if (action == self.StartButtonsTrigger):
                command = "%01#RCSR0610"
            ret = -1

            bcc = self.__bccValue(command)
            command = command + bcc + '\r'
            command = command.upper()
            self.ser.write(command)
            readString =  self.ReadData(0.1)
            # print "readString="+readString
            if("fail" in readString):
                self.strErrorMessage = "Command read time out"
                ret = -1
            readString = int(readString[6])
            if (readString == 1):
                ret = 1
            elif (readString == 0):
                ret = 0


            return ret 
        except:
            self.strErrorMessage = "Button status error"
            return -1

    # ********************************************************************************************#
    # Read Sensors
    def GetVer(self):
        if (self.ser.isOpen() == False):
            self.strErrorMessage = "The serial port is not opened"
            return -1
        #PLC Version
        PLCcommand = '%01#RDD0030800308'
        #Server version
        # Sercommand = '%01#RDD0035000351'
        PLcver = self.__readVer(PLCcommand)
        # Server = self.__readONorOFF(Sercommand)
        ver = 'PLCVer: ' + PLcver
        print (ver)
        PLcver = str(PLcver)
        if (PLcver.__len__() < 1):
            self.strErrorMessage = "Getversion Read command fail"
            return -1
        return ver

# ********************************************************************************************#

    # ********************************************************************************************#
    def SignalReset(self,timeout):
        try:
            mytimeCount = 0
            command = '%01#WCSR00841'
            bcc = self.__bccValue(command)
            command = command + bcc + '\r'
            ret = self.__writeRead(command)
            if(ret == 0):
                # wait for x-axis is ready
                time.sleep(self.myWaitTime)
                mytimeCount = 0
                command = "%01#RCSX0009"
                bcc = self.__bccValue(command)
                command = command + bcc + '\r'
                self.ser.write(command)
                time.sleep(0.2)
                string = self.ser.read_all()
                if int(string[6]) == 0:
                    self.strErrorMessage = "SignalReset action fail"
                    return -1
                while (self.GetHomeFinishState(self.XYZ_axis) == 1):
                    command = "%01#RCSX0009"
                    bcc = self.__bccValue(command)
                    command = command + bcc + '\r'
                    self.ser.write(command)
                    time.sleep(0.2)
                    string = self.ser.read_all()
                    if int(string[6]) == 0:
                        self.strErrorMessage = "SignalReset action fail"
                        return -1
                    if(mytimeCount > timeout):
                        self.strErrorMessage = "SignalReset time out"
                        return -1
                    time.sleep(0.5)
                    mytimeCount += self.myWaitTime

                command = '%01#WCSR00840'
                bcc = self.__bccValue(command)
                command = command + bcc + '\r'
                ret = self.__writeRead(command)
                if(ret == -1):
                    self.strErrorMessage = "SignalReset read error"
                    return -1
                return 0
                # mytimeCount = 0
                # while (self.GetmoveSignal(self.X_axis) == 1):
                #     if(mytimeCount > timeout):
                #         self.strErrorMessage = "Resrt time out"
                #         return -1
                #     time.sleep(self.myWaitTime)
                #     mytimeCount += self.myWaitTime
                # # wait for y-axis to ready
                # mytimeCount = 0
                # while (self.GetmoveSignal(self.Y_axis) == 1):
                #     if(mytimeCount > timeout):
                #         self.strErrorMessage = "Resrt time out"
                #         return -1
                #     time.sleep(self.myWaitTime)
                #     mytimeCount += self.myWaitTime
                # # wait for z-axis to ready
                # while (self.GetmoveSignal(self.Z_axis) == 1):
                #     if(mytimeCount > timeout):
                #         self.strErrorMessage = "Resrt time out"
                #         return -1
                #     time.sleep(self.myWaitTime)
                #     mytimeCount += self.myWaitTime
            else:
                self.strErrorMessage = "SignalReset write command fail"
                return -1
        except:
            self.strErrorMessage = "SignalReset error"
            return -1
        return 0

# ********************************************************************************************#




# ********************************************************************************************#
    def GetHomeFinishState(self,ofWhatAxis):
        if(self.ser.isOpen() == False):
            self.strErrorMessage =  "The serial port is not opened"
            return  -1
        try:
            if (ofWhatAxis == self.XYZ_axis):
                command = '%01#RCSR0104'
            elif(ofWhatAxis == self.X_axis):
                command = '%01#RCSR0100'
            elif(ofWhatAxis == self.Y_axis):
                command = '%01#RCSR0101'
            elif(ofWhatAxis == self.Z_axis):
                command = '%01#RCSR0102'

            bcc = self.__bccValue(command)
            command = command + bcc + '\r'
            command = command.upper()
            self.ser.write(command)
            readString =  self.ReadData(0.01)
            if("fail" in readString):
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


# ********************************************************************************************#
    def GetmoveSignal(self,ofWhatAxis):
        if(self.ser.isOpen() == False):
            self.strErrorMessage =  "The serial port is not opened"
            return  -1
        try:
            if (ofWhatAxis == self.XY_axis):
                command = '%01#RCSR0803'
            elif(ofWhatAxis == self.X_axis):
                command = '%01#RCSR0800'
            elif(ofWhatAxis == self.Y_axis):
                command = '%01#RCSR0801'
            elif(ofWhatAxis == self.Z_axis):
                command = '%01#RCSR0802'
            bcc = self.__bccValue(command)
            command = command + bcc + '\r'
            command = command.upper()
            self.ser.write(command)
            readString =  self.ReadData(0.01)
            if("fail" in readString or readString == 0):
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
            self.strErrorMessage = "GetmoveSignal error"
            return -1
# ********************************************************************************************#


# ********************************************************************************************#
    #create circle
    def CreateCircle(self,startx,starty,xStep,yStep,interval,circleNum,xMinLimit,xMaxLimit,yMinLimit,yMaxLimit):
        try:
            x = 0.0
            y = 0.0
            temp = 0.0
            upCenterx=0.0
            upCentery=0.0
            downCenterx=0.0
            downCentery=0.0
            lastx = startx
            lasty = starty
            newxStep = xStep
            newyStep = yStep


            listxPoint = []
            listyPoint = []
            for i in range(0,circleNum,1):
                xStep = (i+1)*newxStep
                yStep = (i+1)*newyStep
                startx = lastx
                starty = lasty
                if(i % 2 == 0):
                    if(i == 0):
                        upCenterx = startx
                        upCentery = starty - yStep
                    endy = upCentery - yStep
                    if(upCentery < 0 or endy < yMinLimit):
                        self.strErrorMessage = "coordinate transboundary up"
                        return -1
                    y = starty
                    while(y >= (endy-self.myTollerance)):
                        temp = 1.0 - math.pow((y-upCentery),2)/math.pow(yStep,2)
                        if(temp >= (0.0-self.myTollerance) and temp <= (0.0+self.myTollerance)):
                            x = upCenterx
                        else:
                            x = math.sqrt(temp*xStep*xStep) + upCenterx
                        listxPoint.append(x)
                        listyPoint.append(y)
                        y = y - interval
                    lastx = x;
                    lasty = y + interval
                else:
                    if(i == 1):
                        downCenterx = startx
                        downCentery = starty + yStep
                    endy = downCentery + yStep
                    if(endy > yMaxLimit):
                        self.strErrorMessage = "coordinate transboundary down"
                        return -1
                    y = starty
                    while (y <= (endy + self.myTollerance)):
                        temp = 1.0 - math.pow((y - downCentery), 2) / math.pow(yStep, 2)
                        if (temp >= (0.0 - self.myTollerance) and temp <= (0.0 + self.myTollerance)):
                            x = upCenterx
                        else:
                            x = math.sqrt(temp * xStep * xStep) + upCenterx
                            x = (x-downCenterx)*-1.0+downCenterx
                        listxPoint.append(x)
                        listyPoint.append(y)
                        y = y + interval
                    lastx = x;
                    lasty = y - interval

            print ('x=:')
            for i in range(0, len(listxPoint),1):
                print (listxPoint[i])
            print ('y=:')
            for i in range(0,len(listyPoint),1):
                print (listyPoint[i])
            listPoint = []
            strPoint = ""
            exeFolderPath = os.getcwd()
            exeFolderPath += "/motion.txt"
            output = open(exeFolderPath,'w')
            for i in range(0,len(listxPoint),1):
                if(listxPoint[i] < xMinLimit):
                    listxPoint[i] = xMinLimit
                if(listxPoint[i] > xMaxLimit):
                    listxPoint[i] = xMaxLimit

                if(listyPoint[i] < yMinLimit):
                    listyPoint[i] = yMinLimit
                if(listyPoint[i] > yMaxLimit):
                    listyPoint[i] = yMaxLimit
                strPoint = str(round(listyPoint[i],2)) + "," + str(round(listxPoint[i],2)) + "\n"
                listPoint.append(strPoint)
                output.write(strPoint)
            output.close()

        except:
            self.strErrorMessage = "CreateCircle error "
            return -1
        return 0

# ********************************************************************************************#


# ********************************************************************************************#
    #create rectangle
    def CreateRectangle(self,startx,starty,xStep,yStep,RectangleNum,xMinLimit,xMaxLimit,yMinLimit,yMaxLimit):
        try:
            x = 0.0
            y = 0.0
            xDirection = -1
            yDirection = 1
            Even = 1
            Odd = 1
            listxPoint = []
            listyPoint = []

            listxPoint.append(startx)
            listyPoint.append(starty)

            for i in range(0,RectangleNum,1):
                if(i % 2 == 0):
                    x = startx
                    y = starty + Odd * yDirection * yStep
                    yDirection = yDirection * -1
                    Odd  = Odd +1
                else:
                    x = startx + Even * xDirection * xStep
                    y = starty
                    Even = Even + 1
                    xDirection = xDirection * -1
                listxPoint.append(x)
                listyPoint.append(y)
                startx = x
                starty = y

            print ("x=:")
            for i in range(0,len(listxPoint),1):
                print (listxPoint[i])
            print ("y=:")
            for j in range(0,len(listyPoint),1):
                print (listyPoint[j])
            strPoint = ""
            exeFolderPath = os.getcwd()
            exeFolderPath += "/motion.txt"
            output = open(exeFolderPath,'w')
            listPoint = []
            # xMinLimit = 40
            # xMaxLimit = 170
            for i in range(0,len(listxPoint),1):
                if(listxPoint[i] < xMinLimit):
                    listxPoint[i] = xMinLimit
                if(listxPoint[i] > xMaxLimit):
                    listxPoint[i] = xMaxLimit

                if(listyPoint[i] < yMinLimit):
                    listyPoint[i] = yMinLimit
                if(listyPoint[i] > yMaxLimit):
                    listyPoint[i] = yMaxLimit
                strPoint = str(round(listyPoint[i],2)) + "," + str(round(listxPoint[i],2)) + "\n"
                listPoint.append(strPoint)
                output.write(strPoint)
            output.close()
        except:
            self.strErrorMessage = "Create pattern error"
            return -1
        return 0

# ********************************************************************************************#




 # ********************************************************************************************#
    #return error message to UI
    def GetErrorMessage(self):
        return self.strErrorMessage
# ********************************************************************************************#



# ********************************************************************************************#
    def RunPattern(self):
        try:
            ret = self.GetSensorStatus(self.RUNPatternSensor)
            if ret == 0:
                # tkMessageBox.showinfo("Error", "It is full mode, not runpattern!!")
                print ('It is full mode,please,do not runpattern')
                return
            exeFolderPath = os.getcwd()
            exeFolderPath += "/motion.txt"
            listXCoordinate = []
            listYCoordinate = []
            fileList = self.__getCoordinatesFromFile(exeFolderPath)
            for line in fileList:
                lineString = line.split(',')
                if(len(lineString) != 2):
                    self.strErrorMessage = "RunPattern format is not correct"
                    return -1
                listXCoordinate.append(float(lineString[1]))
                listYCoordinate.append(float(lineString[0]))
            for i in range(0, len(listXCoordinate), 1):
                err = self.SynchronousXY(listXCoordinate[i], listYCoordinate[i], 5)
                if (err != 0):
                    return -1
        except:
            self.strErrorMessage = "RunPattern error"
            return -1

# ********************************************************************************************#
    def Calibrate(self,ofWhichAxis, incrementOrDecrement):
        try:
            shouldCalibrate = 1
            LoopCounter = 0
            Coordinates = 0.0
            isSuccess = 0

            StepValue = 0.5
            err = self.SetStepValue(self.X_axis,StepValue)
            if(err == -1):
                return -1
            err = self.SetStepValue(self.Y_axis,StepValue)
            if(err == -1):
                return -1
            err = self.SetStepValue(self.Z_axis,StepValue)
            if(err == -1):
                return -1

            while (shouldCalibrate):
                err = self.GetSensorStatus(self.Sensor_Calibrate)
                if(err == -1):
                    return -1
                elif(err == 0):
                    if("increment" in incrementOrDecrement):
                        ret = self.MoveIncrement(ofWhichAxis)
                        if(ret == -1):
                            return -1
                    elif("decrement" in incrementOrDecrement):
                        ret = self.MoveDecrement(ofWhichAxis)
                        if(ret == -1):
                            return -1
                elif(err == 1):
                    LoopCounter = LoopCounter + 1
                    if (LoopCounter == 1):
                        StepValue = 0.1
                    elif (LoopCounter == 2):
                        StepValue = 0.01
                    elif (LoopCounter == 3):
                        ret = self.GetCurrentCoordinates(ofWhichAxis)
                        if(ret == -9999):
                            return -1
                        else:
                            return float(ret)

                    #add back step
                    if ("increment" in incrementOrDecrement):
                        ret = self.MoveDecrement(ofWhichAxis)
                        if(ret == -1):
                            return -1
                    elif ("decrement" in incrementOrDecrement):
                        ret = self.MoveIncrement(ofWhichAxis)
                        if(ret == -1):
                            return -1

                    err = self.SetStepValue(self.X_axis,StepValue)
                    if(err == -1):
                        return -1
                    err = self.SetStepValue(self.Y_axis,StepValue)
                    if(err == -1):
                        return -1
                    err = self.SetStepValue(self.Z_axis,StepValue)
                    if(err == -1):
                        return -1
        except:
            self.strErrorMessage = "Calibrate error"
            return -1

		
		
# ********************************************************************************************#
    def CalibrationPosition__(self,mode):
        try:
            ### Declare Variables #####
            Xval_1 = 0.0
            Xval_2 = 0.0
            Xval_Final = 0.0
            Yval_1 = 0.0
            Yval_2 = 0.0
            Yval_Final = 0.0
            Zvsl_Finsl = 0.0
            StepSpeed = 15

            #1:Reset fixture
            # err = self.SignalReset(10)
            # if(err != 0):
            #     return -1

            #1:Fingerprint down
            err = self.Set_CylindeFunction(self.Cylinder_DOWN)
            if(err == -1):
                return -1

            #2:Lock cylinder
            err = self.Set_CylindeFunction(self.Cylinder_LOCK)
            if(err == -1):
                return -1

            #3:Clynder in
            err = self.Set_CylindeFunction(self.Cylinder_IN)
            if(err == -1):
                return -1

            #4:Set speed
            err = self.SetSpeed(self.X_axis,StepSpeed)
            if(err == -1):
                return -1
            err = self.SetSpeed(self.Y_axis,StepSpeed)
            if(err == -1):
                return -1
            err = self.SetSpeed(self.Z_axis,StepSpeed)
            if(err == -1):
                return -1

            #read each test calibration initial position
            exeFolderPath = os.getcwd()
            if(mode == self.Phone_Mode_C1):
                exeFolderPath += "\\CalibrationInitialC1.txt"
            elif(mode == self.Phone_Mode_B1):
                exeFolderPath += "\\CalibrationInitialB1.txt"
            elif (mode == self.Phone_Mode_C1_Full_One):
                exeFolderPath += "\\CalibrationInitialFullC11.txt"
            elif (mode == self.Phone_Mode_C1_Full_Two):
                exeFolderPath += "\\CalibrationInitialFullC12.txt"
            elif (mode == self.Phone_Mode_B1_Full_One):
                exeFolderPath += "\\CalibrationInitialFullB11.txt"
            elif (mode == self.Phone_Mode_B1_Full_Two):
                exeFolderPath += "\\CalibrationInitialFullB12.txt"

            calibraionFile = open(exeFolderPath)
            alllines = calibraionFile.readlines()
            for line in alllines:
                strLine = line.strip()
                if ("ZIncrementx=" in strLine):
                    zAxisCalX = float(strLine[strLine.find("=") + 1:])
                elif ("ZIncrementy=" in strLine):
                    zAxisCalY = float(strLine[strLine.find("=") + 1:])

                elif ("XAxisCalIncrementX=" in strLine):
                    XAxisCalIncrementX = float(strLine[strLine.find("=") + 1:])
                elif ("XAxisCalIncrementY=" in strLine):
                    XAxisCalIncrementY = float(strLine[strLine.find("=") + 1:])

                elif ("XAxisCalDecrementX=" in strLine):
                    XAxisCalDecrementX = float(strLine[strLine.find("=") + 1:])
                elif ("XAxisCalDecrementY=" in strLine):
                    XAxisCalDecrementY = float(strLine[strLine.find("=") + 1:])

                elif ("YAxisCalIncrementX=" in strLine):
                    YAxisCalIncrementX = float(strLine[strLine.find("=") + 1:])
                elif ("YAxisCalIncrementY=" in strLine):
                    YAxisCalIncrementY = float(strLine[strLine.find("=") + 1:])

                elif ("YAxisCalDecrementX=" in strLine):
                    YAxisCalDecrementX = float(strLine[strLine.find("=") + 1:])
                elif ("YAxisCalDecrementY=" in strLine):
                    YAxisCalDecrementY = float(strLine[strLine.find("=") + 1:])


            # 3:Z-axis calibration
            zSafeDistance = 0
            err = self.MoveToCoordinates(self.Z_axis,zSafeDistance,10)
            if(err == -1):
                return -1
            else:
                #1:Move to calibration position
                err = self.MoveToCoordinates(self.X_axis,zAxisCalX,10)
                if (err == -1):
                    return -1
                err = self.MoveToCoordinates(self.Y_axis,zAxisCalY,10)
                if (err == -1):
                    return -1

                CalibrationBlockHeight = 0
                Zvsl_Finsl = self.Calibrate(self.Z_axis,"increment")
                Zvsl_Finsl = Zvsl_Finsl + CalibrationBlockHeight
                if(Zvsl_Finsl == -1):
                    print ("Z axis calibration error")
                    return -1
                else:
                    print ("Z axis calibration value=" + str(Zvsl_Finsl))

            #4:X-axis calibration  X1
            err = self.MoveToCoordinates(self.Z_axis,zSafeDistance,10)
            if(err == -1):
                return -1
            err = self.MoveToCoordinates(self.X_axis, XAxisCalIncrementX,10)
            if (err == -1):
                return -1
            err = self.MoveToCoordinates(self.Y_axis, XAxisCalIncrementY,10)
            if (err == -1):
                return -1
            Zvalue_temp = float(Zvsl_Finsl)
            Zvalue_temp = Zvalue_temp + 1.5
            err = self.MoveToCoordinates(self.Z_axis, Zvalue_temp, 10)
            if (err == -1):
                return -1
            else:
                Xval_1 = self.Calibrate(self.X_axis, 'increment')
                if (Xval_1 == -1):
                    print ("X_axis increment fail")
                    return -1
                else:
                    print ("X axis calibration value=" + str(Xval_1))


            # 4:X-axis calibration  X2
            err = self.MoveToCoordinates(self.Z_axis, zSafeDistance, 10)
            if (err == -1):
                return -1
            err = self.MoveToCoordinates(self.X_axis, XAxisCalDecrementX,10)
            if (err == -1):
                return -1
            err = self.MoveToCoordinates(self.Y_axis, XAxisCalDecrementY,10)
            if (err == -1):
                return -1
            err = self.MoveToCoordinates(self.Z_axis,Zvalue_temp,10)
            if(err == -1):
                return -1
            else:
                Xval_2 = self.Calibrate(self.X_axis, 'decrement')
                if(Xval_2 == -1):
                    print ("X_axis increment fail")
                    return -1
                else:
                    print ("X axis calibration value=" + str(Xval_2))
            Xval_Final = (Xval_1 + Xval_2) / 2
            print ("X calibrate result:" + str(Xval_Final))

            # 5:Y-axis calibration Y1
            err = self.MoveToCoordinates(self.Z_axis, zSafeDistance, 10)
            if (err == -1):
                return -1
            err = self.MoveToCoordinates(self.X_axis, YAxisCalIncrementX,10)
            if (err == -1):
                return -1
            err = self.MoveToCoordinates(self.Y_axis, YAxisCalIncrementY,10)
            if (err == -1):
                return -1
            err = self.MoveToCoordinates(self.Z_axis,Zvalue_temp,10)
            if(err == -1):
                return -1
            else:
                Yval_1 = self.Calibrate(self.Y_axis, 'increment')
                if(Yval_1 == -1):
                    print ("Y_axis increment fail")
                    return -1
                else:
                    print ("Y axis calibration value=" + str(Yval_1))

            # 5:Y-axis calibration Y2
            err = self.MoveToCoordinates(self.Z_axis, zSafeDistance, 10)
            if (err == -1):
                return -1
            err = self.MoveToCoordinates(self.X_axis, YAxisCalDecrementX,10)
            if (err == -1):
                return -1
            err = self.MoveToCoordinates(self.Y_axis, YAxisCalDecrementY,10)
            if (err == -1):
                return -1
            err = self.MoveToCoordinates(self.Z_axis, Zvalue_temp,10)
            if (err == -1):
                return -1
            else:
                Yval_2 = self.Calibrate(self.Y_axis, 'decrement')
                if (Yval_2 == -1):
                    print ("Y_axis increment fail")
                    return -1
                else:
                    print ("Y axis calibration value=" + str(Yval_2))
            Yval_Final = (Yval_1 + Yval_2) / 2
            print ("Y calibrate result:" + str(Yval_Final))
            Zvsl_Finsl = Zvsl_Finsl + 25.5

            #Save calibrtion file
            exeFolderPath = os.getcwd()
            if(mode == self.Phone_Mode_C1):
                exeFolderPath += "\\calibrationC1.txt"
            elif(mode == self.Phone_Mode_B1):
                exeFolderPath += "\\calibrationB1.txt"
            elif(mode == self.Phone_Mode_C1_Full_One):
                exeFolderPath += "\\calibrationFullC11.txt"
            elif(mode == self.Phone_Mode_C1_Full_Two):
                exeFolderPath += "\\calibrationFullC12.txt"
            elif(mode == self.Phone_Mode_B1_Full_One):
                exeFolderPath += "\\calibrationFullB11.txt"
            elif(mode == self.Phone_Mode_B1_Full_One):
                exeFolderPath += "\\calibrationFullB12.txt"

            output = open(exeFolderPath, 'w')
            output.write("X1=" + str(Xval_1) + "\n")
            output.write("X2=" + str(Xval_2) + "\n")
            output.write("X-Finial=" + str(Xval_Final) + "\n")
            output.write("Y1=" + str(Yval_1) + "\n")
            output.write("Y2=" + str(Yval_2) + "\n")
            output.write("Y-Finial=" + str(Yval_Final) + "\n")
            output.write("Z-Finial=" + str(Zvsl_Finsl) + "\n")

            err = self.MoveToCoordinates(self.Z_axis, zSafeDistance,10)
            if (err == -1):
                return -1
            err = self.MoveToCoordinates(self.X_axis, Xval_Final,10)
            if (err == -1):
                return -1
            err = self.MoveToCoordinates(self.Y_axis, Yval_Final,10)
            if (err == -1):
                return -1
        except:
            self.strErrorMessage = "CalibrationPosition error"
            return -1
		


 # ********************************************************************************************#
    def CalibrationPosition(self,product):
        try:
            ### Declare Variables #####
            Xval_1 = 0.0
            Xval_2 = 0.0
            Xval_Final = 0.0
            Yval_1 = 0.0
            Yval_2 = 0.0
            Yval_Final = 0.0
            Zvsl_Finsl = 0.0
            StepSpeed = 15

            #1:Reset fixture
            # err = self.SignalReset(10)
            # if(err != 0):
            #     return -1

            #1:Fingerprint down
            err = self.Set_CylindeFunction(self.Cylinder_DOWN)
            if(err == -1):
                return -1

            #2:Lock cylinder
            err = self.Set_CylindeFunction(self.Cylinder_LOCK)
            if(err == -1):
                return -1

            #3:Clynder in
            err = self.Set_CylindeFunction(self.Cylinder_IN)
            if(err == -1):
                return -1

            #4:Set speed
            err = self.SetSpeed(self.X_axis,StepSpeed)
            if(err == -1):
                return -1
            err = self.SetSpeed(self.Y_axis,StepSpeed)
            if(err == -1):
                return -1
            err = self.SetSpeed(self.Z_axis,StepSpeed)
            if(err == -1):
                return -1

            #read each test calibration initial position
            if product == 'B1':
                exeFolderPath = os.getcwd()
                exeFolderPath += "/B1_CalibrationInitial.txt"
            elif product == 'C1':
                exeFolderPath = os.getcwd()
                exeFolderPath += "/C1_CalibrationInitial.txt"

            calibraionFile = open(exeFolderPath)
            alllines = calibraionFile.readlines()
            for line in alllines:
                strLine = line.strip()
                if ("ZIncrementx=" in strLine):
                    zAxisCalX = float(strLine[strLine.find("=") + 1:])
                elif ("ZIncrementy=" in strLine):
                    zAxisCalY = float(strLine[strLine.find("=") + 1:])

                elif ("XAxisCalIncrementX=" in strLine):
                    XAxisCalIncrementX = float(strLine[strLine.find("=") + 1:])
                elif ("XAxisCalIncrementY=" in strLine):
                    XAxisCalIncrementY = float(strLine[strLine.find("=") + 1:])

                elif ("XAxisCalDecrementX=" in strLine):
                    XAxisCalDecrementX = float(strLine[strLine.find("=") + 1:])
                elif ("XAxisCalDecrementY=" in strLine):
                    XAxisCalDecrementY = float(strLine[strLine.find("=") + 1:])

                elif ("YAxisCalIncrementX=" in strLine):
                    YAxisCalIncrementX = float(strLine[strLine.find("=") + 1:])
                elif ("YAxisCalIncrementY=" in strLine):
                    YAxisCalIncrementY = float(strLine[strLine.find("=") + 1:])

                elif ("YAxisCalDecrementX=" in strLine):
                    YAxisCalDecrementX = float(strLine[strLine.find("=") + 1:])
                elif ("YAxisCalDecrementY=" in strLine):
                    YAxisCalDecrementY = float(strLine[strLine.find("=") + 1:])


            # 3:Z-axis calibration
            zSafeDistance = 0
            err = self.MoveToCoordinates(self.Z_axis,zSafeDistance,10)
            if(err == -1):
                return -1
            else:
                #1:Move to calibration position
                err = self.MoveToCoordinates(self.X_axis,zAxisCalX,10)
                if (err == -1):
                    return -1
                err = self.MoveToCoordinates(self.Y_axis,zAxisCalY,10)
                if (err == -1):
                    return -1

                CalibrationBlockHeight = 0
                Zvsl_Finsl = self.Calibrate(self.Z_axis,"increment")
                Zvsl_Finsl = Zvsl_Finsl + CalibrationBlockHeight
                if(Zvsl_Finsl == -1):
                    print ("Z axis calibration error")
                    return -1
                else:
                    print ("Z axis calibration value=" + str(Zvsl_Finsl))

            #4:X-axis calibration  X1
            err = self.MoveToCoordinates(self.Z_axis,zSafeDistance,10)
            if(err == -1):
                return -1
            err = self.MoveToCoordinates(self.X_axis, XAxisCalIncrementX,10)
            if (err == -1):
                return -1
            err = self.MoveToCoordinates(self.Y_axis, XAxisCalIncrementY,10)
            if (err == -1):
                return -1
            Zvalue_temp = float(Zvsl_Finsl)
            Zvalue_temp = Zvalue_temp + 1.5
            err = self.MoveToCoordinates(self.Z_axis, Zvalue_temp, 10)
            if (err == -1):
                return -1
            else:
                Xval_1 = self.Calibrate(self.X_axis, 'increment')
                if (Xval_1 == -1):
                    print ("X_axis increment fail")
                    return -1
                else:
                    print ("X axis calibration value=" + str(Xval_1))


            # 4:X-axis calibration  X2
            err = self.MoveToCoordinates(self.Z_axis, zSafeDistance, 10)
            if (err == -1):
                return -1
            err = self.MoveToCoordinates(self.X_axis, XAxisCalDecrementX,10)
            if (err == -1):
                return -1
            err = self.MoveToCoordinates(self.Y_axis, XAxisCalDecrementY,10)
            if (err == -1):
                return -1
            err = self.MoveToCoordinates(self.Z_axis,Zvalue_temp,10)
            if(err == -1):
                return -1
            else:
                Xval_2 = self.Calibrate(self.X_axis, 'decrement')
                if(Xval_2 == -1):
                    print ("X_axis increment fail")
                    return -1
                else:
                    print ("X axis calibration value=" + str(Xval_2))
            Xval_Final = (Xval_1 + Xval_2) / 2
            print ("X calibrate result:" + str(Xval_Final))

            # 5:Y-axis calibration Y1
            err = self.MoveToCoordinates(self.Z_axis, zSafeDistance, 10)
            if (err == -1):
                return -1
            err = self.MoveToCoordinates(self.X_axis, YAxisCalIncrementX,10)
            if (err == -1):
                return -1
            err = self.MoveToCoordinates(self.Y_axis, YAxisCalIncrementY,10)
            if (err == -1):
                return -1
            err = self.MoveToCoordinates(self.Z_axis,Zvalue_temp,10)
            if(err == -1):
                return -1
            else:
                Yval_1 = self.Calibrate(self.Y_axis, 'increment')
                if(Yval_1 == -1):
                    print ("Y_axis increment fail")
                    return -1
                else:
                    print ("Y axis calibration value=" + str(Yval_1))

            # 5:Y-axis calibration Y2
            err = self.MoveToCoordinates(self.Z_axis, zSafeDistance, 10)
            if (err == -1):
                return -1
            err = self.MoveToCoordinates(self.X_axis, YAxisCalDecrementX,10)
            if (err == -1):
                return -1
            err = self.MoveToCoordinates(self.Y_axis, YAxisCalDecrementY,10)
            if (err == -1):
                return -1
            err = self.MoveToCoordinates(self.Z_axis, Zvalue_temp,10)
            if (err == -1):
                return -1
            else:
                Yval_2 = self.Calibrate(self.Y_axis, 'decrement')
                if (Yval_2 == -1):
                    print ("Y_axis increment fail")
                    return -1
                else:
                    print ("Y axis calibration value=" + str(Yval_2))
            Yval_Final = (Yval_1 + Yval_2) / 2
            print ("Y calibrate result:" + str(Yval_Final))
            Zvsl_Finsl = Zvsl_Finsl + 5.5
            #Save calibrtion file
            if product == 'B1':
                exeFolderPath = os.getcwd()
                exeFolderPath += "/B1_calibration.txt"
            elif product == 'C1':
                exeFolderPath = os.getcwd()
                exeFolderPath += "/C1_calibration.txt"


            output = open(exeFolderPath, 'w')
            output.write("X1=" + str(Xval_1) + "\n")
            output.write("X2=" + str(Xval_2) + "\n")
            output.write("X-Finial=" + str(Xval_Final) + "\n")
            output.write("Y1=" + str(Yval_1) + "\n")
            output.write("Y2=" + str(Yval_2) + "\n")
            output.write("Y-Finial=" + str(Yval_Final) + "\n")
            output.write("Z-Finial=" + str(Zvsl_Finsl) + "\n")
            output.close()

            err = self.MoveToCoordinates(self.Z_axis, zSafeDistance,10)
            if (err == -1):
                return -1
            err = self.MoveToCoordinates(self.X_axis, Xval_Final,10)
            if (err == -1):
                return -1
            err = self.MoveToCoordinates(self.Y_axis, Yval_Final,10)
            if (err == -1):
                return -1

        except:
            self.strErrorMessage = "CalibrationPosition error"
            return -1

    # ********************************************************************************************#
    def DUTLcokOrOpen(self,index,state):
        if (self.ser.isOpen() == False):
            self.strErrorMessage = "The serial port is not opened"
            return -1
        try:
            if (index == self.DUT1):
                if(state == self.DUT_LOCK):
                    command = "%01#WCSR01121"
                elif(state == self.DUT_OPEN):
                    command = "%01#WCSR01120"
            elif (index == self.DUT2):
                if(state == self.DUT_LOCK):
                    command = "%01#WCSR01141"
                elif(state == self.DUT_OPEN):
                    command = "%01#WCSR01140"
            elif (index == self.DUT3):
                if(state == self.DUT_LOCK):
                    command = "%01#WCSR01161"
                elif(state == self.DUT_OPEN):
                    command = "%01#WCSR01160"
            elif (index == self.DUT4):
                if(state == self.DUT_LOCK):
                    command = "%01#WCSR01181"
                elif(state == self.DUT_OPEN):
                    command = "%01#WCSR01180"
            elif(index == self.DUTALL):
                if(state == self.DUT_LOCK):
                    command = "%01#WCSR00801"
                elif(state == self.DUT_OPEN):
                    command = "%01#WCSR00800"

            ret = self.__writeRead(command)
            if(ret != 0):
                self.strErrorMessage = "DUTLcokOrOpen Red command fail"
                return -1
            else:
                if (index == self.DUT1):
                    sensor = self.USB1Sensor
                elif (index == self.DUT2):
                    sensor = self.USB2Sensor
                elif (index == self.DUT3):
                    sensor = self.USB3Sensor
                elif (index == self.DUT4):
                    sensor = self.USB4Sensor
                elif (index == self.DUTALL):
                    sensor = self.USBALLSensor

                if (state == self.DUT_LOCK):
                    exceptValue = 1
                elif(state == self.DUT_OPEN):
                    exceptValue = 0

                if(self.bDisableUSBSensor == False):
                    timeout = 3
                    myTimeout = 0
                    while(1):
                        ret = self.GetSensorStatus(sensor)
                        if(exceptValue == ret):
                            break
                        elif(ret == -1):
                            self.strErrorMessage = "DUTLcokOrOpen read error"
                            return -1
                        elif(myTimeout > timeout):
                            self.strErrorMessage = "DUTLcokOrOpen time out"
                            return -1
                        time.sleep(0.1)
                        myTimeout = myTimeout + 0.1
                return 0
        except:
            self.strErrorMessage = "DUTLcokOrOpen error"
            return -1


    # ********************************************************************************************#
    def Set_DM_5V_ONOFF(self,OnOrOff):
        if(self.ser.isOpen() == False):
            self.strErrorMessage =  "The serial port is not opened"
            return  -1
        try:
            print ("Set_DM_5V_ONOFF")
            if(OnOrOff == self.Set_DM_5V_ON):
                command = "%01#WCSR00881"
            elif(OnOrOff == self.Set_DM_5V_OFF):
                command = "%01#WCSR00880"
            ret = self.__writeRead(command)
            if (ret != 0):
                self.strErrorMessage = "Set_DM_5V_ONOFF Red command fail"
                return -1
            return 0
        except:
            self.strErrorMessage = "Set_DM_5V_ONOFF error"
            return -1

    # ********************************************************************************************#
    def Set_CylindeFunction(self,action):
        if(self.ser.isOpen() == False):
            self.strErrorMessage =  "The serial port is not opened"
            return  -1
        try:
            #set
            if (action == self.Cylinder_IN):
                command = "%01#WCSR00771"
            elif (action == self.Cylinder_OUT):
                command = "%01#WCSR00791"
            elif (action == self.Cylinder_UP):
                command = "%01#WCSR00781"
            elif (action == self.Cylinder_DOWN):
                command = "%01#WCSR00780"
            elif (action == self.Cylinder_LOCK):
                command = "%01#WCSR01101"
            elif (action == self.Cylinder_OPEN):
                command = "%01#WCSR01100"

            ret = self.__writeRead(command)
            if (ret != 0):
                self.strErrorMessage = "Set_CylindeFunction Read command fail"
                return -1



            #get
            if(action == self.Cylinder_IN):
                command = "%01#RCSX0011"
                exceptRet = 1
            elif(action == self.Cylinder_OUT):
                command = "%01#RCSX0012"
                exceptRet = 1
            elif(action == self.Cylinder_UP):
                command = "%01#RCSX000E"
                exceptRet = 1
            elif(action == self.Cylinder_DOWN):
                command = "%01#RCSX000F"
                exceptRet = 1
            elif (action == self.Cylinder_LOCK):
                command = "%01#RCSX0308"
                exceptRet = 1
            elif (action == self.Cylinder_OPEN):
                command = "%01#RCSX0308"
                exceptRet = 0

            timeOut = 5
            myTimeCount = 0
            command = "%01#RCSX0009"
            bcc = self.__bccValue(command)
            command = command + bcc + '\r'
            self.ser.write(command)
            time.sleep(0.2)
            string = self.ser.read_all()
            if int(string[6]) == 0:
                self.strErrorMessage = "SignalReset action fail"
                return -1
            while(myTimeCount < timeOut):
                command = "%01#RCSX0009"
                bcc = self.__bccValue(command)
                command = command + bcc + '\r'
                self.ser.write(command)
                time.sleep(0.2)
                string = self.ser.read_all()
                if int(string[6]) == 0:
                    self.strErrorMessage = "SignalReset action fail"
                    return -1
                ret = self.__readONorOFF(command)
                ret = int(ret)
                if(ret == -1):
                    self.strErrorMessage = "Set_CylindeFunction error"
                    return -1
                elif(ret != exceptRet):
                    time.sleep(0.2)
                    myTimeCount += 0.2
                elif(ret == exceptRet):
                    break
            if(myTimeCount >= timeOut):
                self.strErrorMessage = "Set_CylindeFunction time out"
                return -1

            if(action == self.Cylinder_IN or action == self.Cylinder_OUT):
                if (action == self.Cylinder_IN):
                    command = "%01#WCSR00770"
                elif (action == self.Cylinder_OUT):
                    command = "%01#WCSR00790"
                ret = self.__writeRead(command)
                if (ret != 0):
                    self.strErrorMessage = "Set_CylindeFunction Read command fail"
                    return -1
            return 0
        except:
            self.strErrorMessage = "Set_CylindeFunction error"
            return -1

#***********************************************************************************************#


    def Set_CylindeFunctionPack2(self,action):
        if(self.ser.isOpen() == False):
            self.strErrorMessage =  "The serial port is not opened"
            return  -1
        try:
            #set
            if (action == self.Cylinder_IN):
                command = "%01#WCSR00771"
            elif (action == self.Cylinder_OUT):
                command = "%01#WCSR00791"
            elif (action == self.Cylinder_UP):
                command = "%01#WCSR00781"
            elif (action == self.Cylinder_DOWN):
                command = "%01#WCSR00780"
            elif (action == self.Cylinder_LOCK):
                command = "%01#WCSR01271"
            elif (action == self.Cylinder_OPEN):
                command = "%01#WCSR01270"

            ret = self.__writeRead(command)
            if (ret != 0):
                self.strErrorMessage = "Set_CylindeFunction Read command fail"
                return -1



            #get
            if(action == self.Cylinder_IN):
                command = "%01#RCSX0011"
                exceptRet = 1
            elif(action == self.Cylinder_OUT):
                command = "%01#RCSX0012"
                exceptRet = 1
            elif(action == self.Cylinder_UP):
                command = "%01#RCSX000E"
                exceptRet = 1
            elif(action == self.Cylinder_DOWN):
                command = "%01#RCSX000F"
                exceptRet = 1
            elif (action == self.Cylinder_LOCK):
                command = "%01#RCSX0309"
                exceptRet = 1
            elif (action == self.Cylinder_OPEN):
                command = "%01#RCSX0309"
                exceptRet = 0

            timeOut = 5
            myTimeCount = 0
            while(myTimeCount < timeOut):
                ret = self.__readONorOFF(command)
                ret = int(ret)
                if(ret == -1):
                    self.strErrorMessage = "Set_CylindeFunction error"
                    return -1
                elif(ret != exceptRet):
                    time.sleep(0.2)
                    myTimeCount += 0.2
                elif(ret == exceptRet):
                    break
            if(myTimeCount >= timeOut):
                self.strErrorMessage = "Set_CylindeFunction time out"
                return -1

            if(action == self.Cylinder_IN or action == self.Cylinder_OUT):
                if (action == self.Cylinder_IN):
                    command = "%01#WCSR00770"
                elif (action == self.Cylinder_OUT):
                    command = "%01#WCSR00790"
                ret = self.__writeRead(command)
                if (ret != 0):
                    self.strErrorMessage = "Set_CylindeFunction Read command fail"
                    return -1
            return 0
        except:
            self.strErrorMessage = "Set_CylindeFunction error"
            return -1


    def Set_CylindeFunctionPack3(self,action):
        if(self.ser.isOpen() == False):
            self.strErrorMessage =  "The serial port is not opened"
            return  -1
        try:
            #set
            if (action == self.Cylinder_IN):
                command = "%01#WCSR00771"
            elif (action == self.Cylinder_OUT):
                command = "%01#WCSR00791"
            elif (action == self.Cylinder_UP):
                command = "%01#WCSR00781"
            elif (action == self.Cylinder_DOWN):
                command = "%01#WCSR00780"
            elif (action == self.Cylinder_LOCK):
                command = "%01#WCSR01281"
            elif (action == self.Cylinder_OPEN):
                command = "%01#WCSR01280"

            ret = self.__writeRead(command)
            if (ret != 0):
                self.strErrorMessage = "Set_CylindeFunction Read command fail"
                return -1



            #get
            if(action == self.Cylinder_IN):
                command = "%01#RCSX0011"
                exceptRet = 1
            elif(action == self.Cylinder_OUT):
                command = "%01#RCSX0012"
                exceptRet = 1
            elif(action == self.Cylinder_UP):
                command = "%01#RCSX000E"
                exceptRet = 1
            elif(action == self.Cylinder_DOWN):
                command = "%01#RCSX000F"
                exceptRet = 1
            elif (action == self.Cylinder_LOCK):
                command = "%01#RCSX030A"
                exceptRet = 1
            elif (action == self.Cylinder_OPEN):
                command = "%01#RCSX030A"
                exceptRet = 0

            timeOut = 5
            myTimeCount = 0
            while(myTimeCount < timeOut):
                ret = self.__readONorOFF(command)
                ret = int(ret)
                if(ret == -1):
                    self.strErrorMessage = "Set_CylindeFunction error"
                    return -1
                elif(ret != exceptRet):
                    time.sleep(0.2)
                    myTimeCount += 0.2
                elif(ret == exceptRet):
                    break
            if(myTimeCount >= timeOut):
                self.strErrorMessage = "Set_CylindeFunction time out"
                return -1

            if(action == self.Cylinder_IN or action == self.Cylinder_OUT):
                if (action == self.Cylinder_IN):
                    command = "%01#WCSR00770"
                elif (action == self.Cylinder_OUT):
                    command = "%01#WCSR00790"
                ret = self.__writeRead(command)
                if (ret != 0):
                    self.strErrorMessage = "Set_CylindeFunction Read command fail"
                    return -1
            return 0
        except:
            self.strErrorMessage = "Set_CylindeFunction error"
            return -1


    def Set_CylindeFunctionPack4(self,action):
        if(self.ser.isOpen() == False):
            self.strErrorMessage =  "The serial port is not opened"
            return  -1
        try:
            #set
            if (action == self.Cylinder_IN):
                command = "%01#WCSR00771"
            elif (action == self.Cylinder_OUT):
                command = "%01#WCSR00791"
            elif (action == self.Cylinder_UP):
                command = "%01#WCSR00781"
            elif (action == self.Cylinder_DOWN):
                command = "%01#WCSR00780"
            elif (action == self.Cylinder_LOCK):
                command = "%01#WCSR01291"
            elif (action == self.Cylinder_OPEN):
                command = "%01#WCSR01290"

            ret = self.__writeRead(command)
            if (ret != 0):
                self.strErrorMessage = "Set_CylindeFunction Read command fail"
                return -1



            #get
            if(action == self.Cylinder_IN):
                command = "%01#RCSX0011"
                exceptRet = 1
            elif(action == self.Cylinder_OUT):
                command = "%01#RCSX0012"
                exceptRet = 1
            elif(action == self.Cylinder_UP):
                command = "%01#RCSX000E"
                exceptRet = 1
            elif(action == self.Cylinder_DOWN):
                command = "%01#RCSX000F"
                exceptRet = 1
            elif (action == self.Cylinder_LOCK):
                command = "%01#RCSX030B"
                exceptRet = 1
            elif (action == self.Cylinder_OPEN):
                command = "%01#RCSX030B"
                exceptRet = 0

            timeOut = 5
            myTimeCount = 0
            while(myTimeCount < timeOut):
                ret = self.__readONorOFF(command)
                ret = int(ret)
                if(ret == -1):
                    self.strErrorMessage = "Set_CylindeFunction error"
                    return -1
                elif(ret != exceptRet):
                    time.sleep(0.2)
                    myTimeCount += 0.2
                elif(ret == exceptRet):
                    break
            if(myTimeCount >= timeOut):
                self.strErrorMessage = "Set_CylindeFunction time out"
                return -1

            if(action == self.Cylinder_IN or action == self.Cylinder_OUT):
                if (action == self.Cylinder_IN):
                    command = "%01#WCSR00770"
                elif (action == self.Cylinder_OUT):
                    command = "%01#WCSR00790"
                ret = self.__writeRead(command)
                if (ret != 0):
                    self.strErrorMessage = "Set_CylindeFunction Read command fail"
                    return -1
            return 0
        except:
            self.strErrorMessage = "Set_CylindeFunction error"
            return -1



    def Set_CylindeFunctionPack5(self,action):
        if(self.ser.isOpen() == False):
            self.strErrorMessage =  "The serial port is not opened"
            return  -1
        try:
            #set
            if (action == self.Cylinder_IN):
                command = "%01#WCSR00771"
            elif (action == self.Cylinder_OUT):
                command = "%01#WCSR00791"
            elif (action == self.Cylinder_UP):
                command = "%01#WCSR00781"
            elif (action == self.Cylinder_DOWN):
                command = "%01#WCSR00780"
            elif (action == self.Cylinder_LOCK):
                command = "%01#WCSR012A1"
            elif (action == self.Cylinder_OPEN):
                command = "%01#WCSR012A0"

            ret = self.__writeRead(command)
            if (ret != 0):
                self.strErrorMessage = "Set_CylindeFunction Read command fail"
                return -1



            #get
            if(action == self.Cylinder_IN):
                command = "%01#RCSX0011"
                exceptRet = 1
            elif(action == self.Cylinder_OUT):
                command = "%01#RCSX0012"
                exceptRet = 1
            elif(action == self.Cylinder_UP):
                command = "%01#RCSX000E"
                exceptRet = 1
            elif(action == self.Cylinder_DOWN):
                command = "%01#RCSX000F"
                exceptRet = 1
            elif (action == self.Cylinder_LOCK):
                command = "%01#RCSR0010"
                exceptRet = 1
            elif (action == self.Cylinder_OPEN):
                command = "%01#RCSR0010"
                exceptRet = 0

            timeOut = 5
            myTimeCount = 0
            while(myTimeCount < timeOut):
                ret = self.__readONorOFF(command)
                ret = int(ret)
                if(ret == -1):
                    self.strErrorMessage = "Set_CylindeFunction error"
                    return -1
                elif(ret != exceptRet):
                    time.sleep(0.2)
                    myTimeCount += 0.2
                elif(ret == exceptRet):
                    break
            if(myTimeCount >= timeOut):
                self.strErrorMessage = "Set_CylindeFunction time out"
                return -1

            if(action == self.Cylinder_IN or action == self.Cylinder_OUT):
                if (action == self.Cylinder_IN):
                    command = "%01#WCSR00770"
                elif (action == self.Cylinder_OUT):
                    command = "%01#WCSR00790"
                ret = self.__writeRead(command)
                if (ret != 0):
                    self.strErrorMessage = "Set_CylindeFunction Read command fail"
                    return -1
            return 0
        except:
            self.strErrorMessage = "Set_CylindeFunction error"
            return -1

    # ********************************************************************************************#
    def AlarmBuzzer(self,state):
        if (self.ser.isOpen() == False):
            self.strErrorMessage = "The serial port is not opened"
            return -1
        try:
            if(state == self.Alarm_On):
                command = "%01#WCSR00761"
            elif(state == self.Alarm_Off):
                command = "%01#WCSR00760"
            ret = self.__writeRead(command)
            if (ret != 0):
                self.strErrorMessage = "AlarmBuzzer Red command fail"
                return -1
            return 0
        except:
            self.strErrorMessage = "AlarmBuzzer error"
            return -1


    # ********************************************************************************************#
    def ReadAxisAlarm(self,ofWhichAxis):
        try:
            if(ofWhichAxis == self.X_axis):
                command = "%01#RCSX0006"
            elif(ofWhichAxis == self.Y_axis):
                command = "%01#RCSX0007"
            elif(ofWhichAxis == self.Z_axis):
                command = "%01#RCSX0008"
            else:
                self.strErrorMessage = "ReadAxisAlarm Input parameter error"
                return -1
            self.ser.write(command)
            readString = self.ReadData(0.1)
            #?????
        except:
            self.strErrorMessage = "ReadAxisAlarm error"
            return -1

    # ********************************************************************************************#
    def SetEStop(self,state):
        try:
            if(state == self.EStopOff):
                command = "%01#WCSR00990"
            elif(state == self.EStopOn):
                command = "%01#WCSR00991"
            else:
                self.strErrorMessage = "SetEStop Input parameter error"
                return -1
            self.ser.write(command)
            readString = self.ReadData(0.1)
        except:
            self.strErrorMessage = "SetEStop error"
            return -1


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
            print ("command = " + command)
            ret = self.__writeRead(command)
            if (ret != 0):
                self.strErrorMessage = "SetLight curtain command fail"
                return -1
            return 0
        except:
            self.strErrorMessage = "SetLight curtain error"
            return -1

    # ********************************************************************************************#
    def ResetTray(self,action):
        try:
            if (action == self.Cylinder_IN):
                command = "%01#WCSR00770"
            elif (action == self.Cylinder_OUT):
                command = "%01#WCSR00790"
            ret = self.__writeRead(command)
            if (ret != 0):



                self.strErrorMessage = "ResetTray Read command fail"
                return -1
        except:
            self.strErrorMessage = "ResetTray error"
            return -1

    # **************************** full test ****************************************************************#
    def BojayFulltest(self, product,pauseSec):
        try:
            # 1:Fingerprint down
            err = self.Set_CylindeFunction(self.Cylinder_DOWN)
            if (err == -1):
                return -1

            # 2:Z axis move to safety position
            ZaxisSafetyPosition = 0
            err = self.MoveToCoordinates(self.Z_axis, ZaxisSafetyPosition, 10)
            if (err == -1):
                return -1

            err = self.Set_CylindeFunction(self.Cylinder_LOCK)
            if (err == -1):
                return -1

            # 4:Tray in
            err = self.Set_CylindeFunction(self.Cylinder_IN)
            if (err == -1):
                err = self.ResetTray(self.Cylinder_IN)
                if (err == -1):
                    return -1
                return -1

            # 6:Set speed
            if (self.bFirstRunFunction == True):
                err = self.SetSpeed(self.X_axis, 50)
                if (err == -1):
                    return -1
                err = self.SetSpeed(self.Y_axis, 50)
                if (err == -1):
                    return -1
                err = self.SetSpeed(self.Z_axis, 50)
                if (err == -1):
                    return -1

            # xlocate = 100.0
            # ylocate = 45.0
            # zlocate = 0
            #
            # err = self.SynchronousXY(xlocate, ylocate, 5)
            # if (err == -1):
            #     return -1
            # err = self.MoveToCoordinates(self.Z_axis, zlocate, 10)
            # if (err == -1):
            #     return -1
            #
            # sleep(0.5)

            if product == 'B11':
                exeFolderPath = os.getcwd()
                exeFolderPath += "/B11_calibration.txt"
            elif product == 'B12':
                exeFolderPath = os.getcwd()
                exeFolderPath += "/B12_calibration.txt"
            elif product == 'C11':
                exeFolderPath = os.getcwd()
                exeFolderPath += "/C11_calibration.txt"
            elif product == 'C12':
                exeFolderPath = os.getcwd()
                exeFolderPath += "/C12_calibration.txt"

            # 8:Move to calibraton position
            calibraionFile = open(exeFolderPath)
            alllines = calibraionFile.readlines()
            for line in alllines:
                strLine = line.strip()
                if ("X-Finial=" in strLine):
                    self.XAxisCalibration = float(strLine[strLine.find("=") + 1:])
                elif ("Y-Finial=" in strLine):
                    self.YAxisCalibration = float(strLine[strLine.find("=") + 1:])
                elif ("Z-Finial=" in strLine):
                    self.ZAxisCalibration = float(strLine[strLine.find("=") + 1:])


            err = self.SynchronousXY(self.XAxisCalibration, self.YAxisCalibration, 5)
            if (err == -1):
                return -1
            err = self.MoveToCoordinates(self.Z_axis, self.ZAxisCalibration, 10)
            if (err == -1):
                return -1

            sleep(pauseSec)
            # 10 end of test
            # err = self.MoveToCoordinates(self.Z_axis, 0, 10)
            # if (err == -1):
            #     return -1
            # err = self.SynchronousXY(0, 0, 10)
            # if (err == -1):
            #     return -1
            return 0
        except:
            self.strErrorMessage = "Full test error"
            return -1


    # **************************** full test ****************************************************************#
    def BojayholeTest(self):
        try:
            # 1:Fingerprint down
            err = self.Set_CylindeFunction(self.Cylinder_DOWN)
            if (err == -1):
                return -1

            # 2:Z axis move to safety position
            ZaxisSafetyPosition = 0
            err = self.MoveToCoordinates(self.Z_axis, ZaxisSafetyPosition, 10)
            if (err == -1):
                return -1

            err = self.Set_CylindeFunction(self.Cylinder_LOCK)
            if (err == -1):
                return -1

            # 4:Tray in
            err = self.Set_CylindeFunction(self.Cylinder_IN)
            if (err == -1):
                err = self.ResetTray(self.Cylinder_IN)
                if (err == -1):
                    return -1
                return -1

            # 6:Set speed
            if (self.bFirstRunFunction == True):
                err = self.SetSpeed(self.X_axis, 50)
                if (err == -1):
                    return -1
                err = self.SetSpeed(self.Y_axis, 50)
                if (err == -1):
                    return -1
                err = self.SetSpeed(self.Z_axis, 50)
                if (err == -1):
                    return -1

            # xlocate = 100.0
            # ylocate = 45.0
            # zlocate = 0
            #
            # err = self.SynchronousXY(xlocate, ylocate, 5)
            # if (err == -1):
            #     return -1
            # err = self.MoveToCoordinates(self.Z_axis, zlocate, 10)
            # if (err == -1):
            #     return -1
            #
            # sleep(0.5)

            # if product == 'B11':
            #     exeFolderPath = os.getcwd()
            #     exeFolderPath += "/B11_calibration.txt"
            # elif product == 'B12':
            #     exeFolderPath = os.getcwd()
            #     exeFolderPath += "/B12_calibration.txt"
            # elif product == 'C11':
            #     exeFolderPath = os.getcwd()
            #     exeFolderPath += "/C11_calibration.txt"
            # elif product == 'C12':
            exeFolderPath = os.getcwd()
            exeFolderPath += "/holetest.txt"

            # 8:Move to calibraton position
            calibraionFile = open(exeFolderPath)
            alllines = calibraionFile.readlines()
            for line in alllines:
                strLine = line.strip()
                if ("X-Finial=" in strLine):
                    self.XAxisCalibration = float(strLine[strLine.find("=") + 1:])
                elif ("Y-Finial=" in strLine):
                    self.YAxisCalibration = float(strLine[strLine.find("=") + 1:])
                elif ("Z-Finial=" in strLine):
                    self.ZAxisCalibration = float(strLine[strLine.find("=") + 1:])


            err = self.SynchronousXY(self.XAxisCalibration, self.YAxisCalibration, 5)
            if (err == -1):
                return -1
            err = self.MoveToCoordinates(self.Z_axis, self.ZAxisCalibration, 10)
            if (err == -1):
                return -1

            sleep(1)
            # 10 end of test
            # err = self.MoveToCoordinates(self.Z_axis, 0, 10)
            # if (err == -1):
            #     return -1
            # err = self.SynchronousXY(0, 0, 10)
            # if (err == -1):
            #     return -1
            return 0
        except:
            self.strErrorMessage = "Full test error"
            return -1

    # ********************************************************************************************#

    # ********************************************************************************************#
    def BojayDutStartTest(self):
        try:
            if self.SignalReset(5) == -1:
                 return -1

            if (self.Set_CylindeFunction(self.Cylinder_IN) == -1):
                return -1
            originalPoints = [[94.88, 18.92, 17.7], [94.88, 52.92, 16.7], [94.88, 85.92, 17.7]]


            for j in range(0,10,1):
                if self.MoveToCoordinates(self.X_axis,99.88,5) == -1:
                    return -1
                if self.MoveToCoordinates(self.Y_axis,52.92,5) == -1:
                    return -1
                if self.MoveToCoordinates(self.Z_axis,18.7,5) == -1:
                    return -1

                pin2 = self.PushPinDown(self.Pin2)
                time.sleep(1)
                pin2 = self.LiftPinUp(self.Pin2)
                time.sleep(1)


                for i in range(0,3,1):
                    if self.MoveToCoordinates(self.Z_axis,10.0,5) == -1:
                        return -1

                    if self.MoveToCoordinates(self.X_axis,originalPoints[i][0],5) == -1:
                        return -1
                    if self.MoveToCoordinates(self.Y_axis,originalPoints[i][1],5) == -1:
                        return -1
                    if self.MoveToCoordinates(self.Z_axis,originalPoints[i][2],5) == -1:
                        return -1

                    pin1 = self.PushPinDown(self.Pin1)
                    time.sleep(1)
                    pin1 = self.LiftPinUp(self.Pin1)
                    time.sleep(1)
                if self.MoveToCoordinates(self.Z_axis, 12.0, 5) == -1:
                    return -1


            if (self.Set_CylindeFunction(self.Cylinder_IN) == -1):
                return -1
            if self.SignalReset(5) == -1:
                 return -1
        except :
            self.strErrorMessage = "Dut Start Test error"
            return -1

    # ********************************************************************************************#
    def BojayFFTEnd(self,DUT1,DUT2,DUT3,DUT4,DUTALL):
        try:
            #1:Fingerprint down
            err = self.Set_CylindeFunction(self.Cylinder_DOWN)
            if(err == -1):
                return -1
            #2:Z axis move to safety position
            ZaxisSafetyPosition = 0
            err = self.MoveToCoordinates(self.Z_axis,ZaxisSafetyPosition,5)
            if(err == -1):
                return -1

            #3:Open USB
            if(DUTALL == True):
                ret = self.DUTLcokOrOpen(self.DUTALL, self.DUT_OPEN)
                if (ret != 0):
                    return -1
            else:
                if(DUT1 == True):
                    ret = self.DUTLcokOrOpen(self.DUT1,self.DUT_OPEN)
                    if(ret != 0):
                        return -1
                if(DUT2 == True):
                    ret = self.DUTLcokOrOpen(self.DUT2,self.DUT_OPEN)
                    if(ret != 0):
                        return -1
                if(DUT3 == True):
                    ret = self.DUTLcokOrOpen(self.DUT3,self.DUT_OPEN)
                    if(ret != 0):
                        return -1
                if(DUT4 == True):
                    ret = self.DUTLcokOrOpen(self.DUT4,self.DUT_OPEN)
                    if(ret != 0):
                        return -1

            #4:Cylinder out
            err = self.Set_CylindeFunction(self.Cylinder_OUT)
            if(err == -1):
                err = self.ResetTray(self.Cylinder_OUT)
                if(err == -1):
                    return -1
                return -1

            # 5:Open lock
            err = self.Set_CylindeFunction(self.Cylinder_OPEN)
            if (err == -1):
                return -1
            return 0
        except:
            self.strErrorMessage = "BojayFFTEnd error"
            return -1

    # ********************************************************************************************#
    def GetAllAxisLimit(self):
        try:
            ret = self.GetLimit(self.Z_axis, self.Max_limit)
            if (ret == -9999):
                return -1
            else:
                self.ZAxisMaxLimit = float(ret)
            ret = self.GetLimit(self.Z_axis, self.Min_limit)
            if (ret == -9999):
                return -1
            else:
                self.ZAxisMinLimit = float(ret)

            ret = self.GetLimit(self.X_axis, self.Max_limit)
            if (ret == -9999):
                return -1
            else:
                self.XAxisMaxLimit = float(ret)
            ret = self.GetLimit(self.X_axis, self.Min_limit)
            if (ret == -9999):
                return -1
            else:
                self.XAxisMinLimit = float(ret)
            ret = self.GetLimit(self.Y_axis, self.Max_limit)
            if (ret == -9999):
                return -1
            else:
                self.YAxisMaxLimit = float(ret)
            ret = self.GetLimit(self.Y_axis, self.Min_limit)
            if (ret == -9999):
                return -1
            else:
                self.YAxisMinLimit = float(ret)
        except:
            return -1


    # ********************************************************************************************#
    def SetPLCLimit(self,ofWhatAxis,ofWhatLimit,value):
        try:
            # Set X-axis max / min limit
            if (ofWhatAxis == self.X_axis):
                if (ofWhatLimit == self.Max_limit):
                    command = '%01#WDD0210002101'
                elif (ofWhatLimit == self.Min_limit):
                    command = '%01#WDD0210402105'
                else:
                    self.strErrorMessage = "SetPLCLimit input parameter is not correct"
                    return -1
            # Set Y-axis max / min limit
            elif (ofWhatAxis == self.Y_axis):
                if (ofWhatLimit == self.Max_limit):
                    command = '%01#WDD0210802109'
                elif (ofWhatLimit == self.Min_limit):
                    command = '%01#WDD0211202113'
                else:
                    self.strErrorMessage = "SetPLCLimit input parameter is not correct"
                    return -1
            # Set Z-axis max / min limit
            elif (ofWhatAxis == self.Z_axis):
                if (ofWhatLimit == self.Max_limit):
                    command = '%01#WDD0211602117'
                elif (ofWhatLimit == self.Min_limit):
                    command = '%01#WDD0212002121'
                else:
                    self.strErrorMessage = "SetPLCLimit input parameter is not correct"
                    return -1
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

            finalByte = self.__flipByte(value)
            command = command + finalByte
            ret = self.__writeRead(command)
            return 0
        except:
            self.strErrorMessage = "SetPLCLimit error"
            return -1

    # ********************************************************************************************#
    def LoadLimitTXT(self):
        try:
            strPath = os.getcwd() + "/Limit.txt"
            readTxt = open(strPath,"r")
            allLines = readTxt.readlines()
            lineTemp = ""
            for line in allLines:
                index = line.find("=")
                if "ZAxisX1Limit" in line:
                    value = float(line[index,line.__le__()].strip())
                    ret = self.SetPLCLimit(self.ZAxisX1Limit,self.Min_limit,value)
                elif "ZAxisX2Limit" in line:
                    value = float(line[index,line.__le__()].strip())
                    ret = self.SetPLCLimit(self.ZAxisX2Limit,self.Min_limit,value)
                elif "ZAxisY1Limit" in line:
                    value = float(line[index,line.__le__()].strip())
                    ret = self.SetPLCLimit(self.ZAxisY1Limit,self.Min_limit,value)
                elif "ZAxisY2Limit" in line:
                    value = float(line[index,line.__le__()].strip())
                    ret = self.SetPLCLimit(self.ZAxisY2Limit,self.Min_limit,value)
                elif "ZAxisY3Limit" in line:
                    value = float(line[index,line.__le__()].strip())
                    ret = self.SetPLCLimit(self.ZAxisY3Limit,self.Min_limit,value)
                elif "ZAxisY4Limit" in line:
                    value = float(line[index,line.__le__()].strip())
                    ret = self.SetPLCLimit(self.ZAxisY4Limit,self.Min_limit,value)
                elif "XAxisMaxLimit" in line:
                    value = float(line[index,line.__le__()].strip())
                    ret = self.SetPLCLimit(self.X_axis,self.Max_limit,value)
                elif "XAxisMinLimit" in line:
                    value = float(line[index,line.__le__()].strip())
                    ret = self.SetPLCLimit(self.X_axis,self.Min_limit,value)
                elif "YAxisMaxLimit" in line:
                    value = float(line[index,line.__le__()].strip())
                    ret = self.SetPLCLimit(self.Y_axis,self.Max_limit,value)
                elif "YAxisMinLimit" in line:
                    value = float(line[index,line.__le__()].strip())
                    ret = self.SetPLCLimit(self.Y_axis,self.Min_limit,value)
                elif "ZAxisMaxLimit" in line:
                    value = float(line[index,line.__le__()].strip())
                    ret = self.SetPLCLimit(self.Z_axis,self.Max_limit,value)
                elif "ZAxisMinLimit" in line:
                    value = float(line[index,line.__le__()].strip())
                    ret = self.SetPLCLimit(self.Z_axis,self.Min_limit,value)
            readTxt.close()
        except:
            self.strErrorMessage = "LoadLimitTXT error"
            return -1

    # ********************************************************************************************#
    def SaveLimitTXT(self,ofKeyWords,strvalue):
        try:
            strPath = os.getcwd() + "/Limit.txt"
            #read data first
            ReadTxt = open(strPath,"r")
            allLines = ReadTxt.readlines()
            myList = []
            for line in allLines:
                if ofKeyWords in line:
                    line = ofKeyWords + " = " +  strvalue + "\r\n"
                myList.append(line)
            ReadTxt.close()
            os.remove(strPath)

            #Write
            WriteTxt = open(strPath, "w")
            for i in range(0,len(myList),1):
                WriteTxt.write(myList[i])
            WriteTxt.close()
        except:
            self.strErrorMessage = "LoadLimitTXT error"
            return -1

#********************************************************************************#
    def PlugInPowerSource(self):
        if(self.ser.isOpen() == False):
            self.strErrorMessage = "The serial port is not opened"
            return -1
        try:
            command = '%01#WCSR02071'
            ret = self.__writeRead(command)
            if(ret == -1):
                self.strErrorMessage = "PlugInPowerSource command fail"
                return -1
            return ret
        except:
            self.strErrorMessage = "PlugInPowerSource error"
            return -1
# ********************************************************************************#

#********************************************************************************#
    def PullOutPowerSource(self):
        if(self.ser.isOpen() == False):
            self.strErrorMessage = "The serial port is not opened"
            return -1
        try:
            command = '%01#WCSR02070'
            ret = self.__writeRead(command)
            if(ret == -1):
                self.strErrorMessage = "PullOutPowerSource command fail"
                return -1
            return ret
        except:
            self.strErrorMessage = "PullOutPowerSource error"
            return -1

# ********************************************************************************#

# ********************************************************************************#
    def USBLockandUnlock(self, state,timeout=2):
        if (self.ser.isOpen() == False):
            self.strErrorMessage = "The serial port is not opened"
            return -1
        try:
            if (state == self.USBLock):
                command = "%01#WCSR00891"
                confirm = 0
            elif (state == self.USBUnlock):
                command = "%01#WCSR00890"
                confirm = 1
            ret = self.__writeRead(command)
            if (ret == -1):
                self.strErrorMessage = "PushPinDown command fail"
                return -1
            mytimeCount = 0
            command = "%01#RCSX0009"
            bcc = self.__bccValue(command)
            command = command + bcc + '\r'
            self.ser.write(command)
            time.sleep(0.2)
            string = self.ser.read_all()
            if int(string[6]) == 0:
                self.strErrorMessage = "USBLockandUnlock action fail"
                return -1
            while True:
                command = "%01#RCSX0009"
                bcc = self.__bccValue(command)
                command = command + bcc + '\r'
                self.ser.write(command)
                time.sleep(0.2)
                string = self.ser.read_all()
                if int(string[6]) == 0:
                    self.strErrorMessage = "USBLockandUnlock action fail"
                    return -1
                if (mytimeCount > timeout):
                    self.strErrorMessage = " GetUSBSensor time out"
                    return -1
                if self.GetSensorStatus(self.USBSensor) == confirm:
                    break
                time.sleep(self.myWaitTime)
                mytimeCount += self.myWaitTime
            return ret
        except:
            self.strErrorMessage = "PushPinDown error"
            return -1

# ********************************************************************************#

# ********************************************************************************#
    def DCLockandUnlock(self, state, timeout=2):
        if (self.ser.isOpen() == False):
            self.strErrorMessage = "The serial port is not opened"
            return -1
        try:
            if (state == self.DCLock):
                command = "%01#WCSR00881"
                confirm = 1
            elif (state == self.DCUnlock):
                command = "%01#WCSR00880"
                confirm = 0
            ret = self.__writeRead(command)
            if (ret == -1):
                self.strErrorMessage = "PushPinDown command fail"
                return -1
            mytimeCount = 0
            command = "%01#RCSX0009"
            bcc = self.__bccValue(command)
            command = command + bcc + '\r'
            self.ser.write(command)
            time.sleep(0.2)
            string = self.ser.read_all()
            if int(string[6]) == 0:
                self.strErrorMessage = "DCLockandUnlock action fail"
                return -1
            while True:
                command = "%01#RCSX0009"
                bcc = self.__bccValue(command)
                command = command + bcc + '\r'
                self.ser.write(command)
                time.sleep(0.2)
                string = self.ser.read_all()
                if int(string[6]) == 0:
                    self.strErrorMessage = "DCLockandUnlock action fail"
                    return -1
                if (mytimeCount > timeout):
                    self.strErrorMessage = " GetDCSensor time out"
                    return -1
                if self.GetSensorStatus(self.DCSensor) == confirm:
                    break
                time.sleep(self.myWaitTime)
                mytimeCount += self.myWaitTime
            return ret
        except Exception,e:
            self.strErrorMessage = "PushPinDown error"
            return -1



# ********************************************************************************#

#********************************************************************************#
    def PushPinDown(self, pinIndex):
        if(self.ser.isOpen() == False):
            self.strErrorMessage = "The serial port is not opened"
            return -1
        try:
            if (pinIndex == self.Pin1):
                command = "%01#WCSR01611"
            elif (pinIndex == self.Pin2):
                command = "%01#WCSR01601"
            elif (pinIndex == self.Pin3):
                command = "%01#WCSR01621"
            ret = self.__writeRead(command)
            if(ret == -1):
                self.strErrorMessage = "PushPinDown command fail"
                return -1
            return ret
        except:
            self.strErrorMessage = "PushPinDown error"
            return -1
# ********************************************************************************#

#********************************************************************************#
    def LiftPinUp(self, pinIndex):
        if(self.ser.isOpen() == False):
            self.strErrorMessage = "The serial port is not opened"
            return -1
        try:
            if (pinIndex == self.Pin1):
                command = "%01#WCSR01610"
            elif (pinIndex == self.Pin2):
                command = "%01#WCSR01600"
            elif (pinIndex == self.Pin3):
                command = "%01#WCSR01620"
            ret = self.__writeRead(command)
            if(ret == -1):
                self.strErrorMessage = "LiftPinUp command fail"
                return -1
            return ret
        except:
            self.strErrorMessage = "LiftPinUp error"
            return -1
# ********************************************************************************#

#********************************************************************************#
    def EnablePowerSource(self, enable):
        if(self.ser.isOpen() == False):
            self.strErrorMessage = "The serial port is not opened"
            return -1
        try:
            if (enable):
                command = "%01#WCSR02071"
            else:
                command = "%01#WCSR02070"
            ret = self.__writeRead(command)
            if(ret == -1):
                self.strErrorMessage = "EnablePowerSource command fail"
                return -1
            return ret
        except:
            self.strErrorMessage = "EnablePowerSource error"
            return -1
# ********************************************************************************#

#********************************************************************************#
    def CheckPowerSourcePosition(self):
        if(self.ser.isOpen() == False):
            self.strErrorMessage = "The serial port is not opened"
            return -1
        try:
            command = "%01#WCSR02071"
            ret = self.__writeRead(command)
            if(ret == -1):
                self.strErrorMessage = "LiftPinUp command fail"
                return -1
            return ret
        except:
            self.strErrorMessage = "LiftPinUp error"
            return -1
# ********************************************************************************#

 # ********************************************************************************************#
    def CalibratePositionOfV71(self, point):
        try:
             ### Declare Variables #####
            if (self.SignalReset(10) == -1):
                 return -1
            time.sleep(1)

            fastSpeed = 10
            step = 0.12
            isTouched = False
            calPoints = []
            # originalPoints = [[25,65],[85,65],[55,15],[55,105]]
            originalPoints = [[81, 54], [120, 54], [100, -6], [100, 114]]
            axises = [self.X_axis,self.X_axis,self.Y_axis,self.Y_axis,self.Z_axis]
            
            #Clynder in
            if(self.Set_CylindeFunction(self.Cylinder_IN) == -1):
                return -1


            #Set fast speed 
            if(self.SetSpeed(self.X_axis,fastSpeed) == -1):
                return -1
            if(self.SetSpeed(self.Y_axis,fastSpeed) == -1):
                return -1

            for i in range(0,4):
                #Move to original position
                if(self.MoveToCoordinates(self.X_axis, originalPoints[i][0], 5) == -1):
                    return -1
                time.sleep(1)
                if(self.MoveToCoordinates(self.Y_axis, originalPoints[i][1], 5) == -1):
                    return -1
                time.sleep(2)
                #Push Z axis down
                if(self.MoveToCoordinates(self.Z_axis, 9, 5) == -1):
                    return -1
                time.sleep(1)
            
                while(not isTouched):
                    if(self.SetStepValue(axises[i],step) == -1):
                        return -1

                    if(i%2 == 0):
                        if(self.MoveIncrement(axises[i]) == -1):
                            return -1
                    else:
                        if(self.MoveDecrement(axises[i]) == -1):
                            return -1

                    time.sleep(0.5)

                    if(self.GetSensorStatus(self.Sensor_Calibrate) == 1):
                        break



                xPosition = float(self.GetCurrentCoordinates(self.X_axis))
                yPosition = float(self.GetCurrentCoordinates(self.Y_axis))
                calPoints.append([xPosition, yPosition])
                print (xPosition,yPosition)

                #Leave block
                if(self.MoveToCoordinates(self.X_axis, originalPoints[i][0], 5) == -1):
                    return -1
                time.sleep(1)
                if(self.MoveToCoordinates(self.Y_axis, originalPoints[i][1], 5) == -1):
                    return -1
                time.sleep(1)
                #Lift Z axis up
                if(self.MoveToCoordinates(self.Z_axis, 0, 5) == -1):
                    return -1
                time.sleep(1)


            #calibretiom Z_Axis
            if (self.MoveToCoordinates(self.X_axis,(calPoints[0][0] + calPoints[1][0])/2.0,5)) == -1:
                 return -1
            if (self.MoveToCoordinates(self.Y_axis, (calPoints[2][1] + calPoints[3][1])/2.0, 5)) == -1:
                 return -1
            if (self.MoveToCoordinates(self.Z_axis, 0, 5)) == -1:
                 return -1
            time.sleep(1)
            while (not isTouched):
                if (self.SetStepValue(axises[4], step) == -1):
                     return -1
                time.sleep(0.5)
                print("have set step value")
                if (self.MoveIncrement(axises[4]) == -1):
                     return -1
                time.sleep(0.5)

                if (self.GetSensorStatus(self.Sensor_Calibrate) == 1):
                     break

            zPosition = float(self.GetCurrentCoordinates(self.Z_axis))


            #Move to original position
            if (self.MoveToCoordinates(self.Z_axis, 0, 5) == -1):
                return -1

            if(self.MoveToCoordinates(self.X_axis, 0, 5) == -1):
                return -1
            time.sleep(1)
            if(self.MoveToCoordinates(self.Y_axis, 0, 5) == -1):
                return -1
            time.sleep(3)

            #Clynder out
            if(self.Set_CylindeFunction(self.Cylinder_OUT) == -1):
                return -1

            point.append((calPoints[0][0] + calPoints[1][0])/2.0)
            point.append((calPoints[2][1] + calPoints[3][1])/2.0)
            point.append(zPosition)
            filepath = os.getcwd()
            filepath += "/CenterPoint.txt"
            with open(filepath, 'w') as output:
                output.write("Center Point = " + str(point) + "\n")
                output.write("4 Cal Points = " + str(calPoints))
                output.close()
            return 0
        except:
            self.strErrorMessage = "CalibrationPosition error"
            return -1

# ********************************************************************************************#

#********************************************************************************#
    def BurningTestOfV71(self, count):
        try:
            centerPoint = []
            
            filepath = os.getcwd()
            filepath += "/CenterPoint.txt"
            with open(filepath, 'r') as input:
                read = input.readline()
                index = read.index('=')
                centerPoint = literal_eval(read[index + 1 :].strip())
                input.close()

            if(self.Set_CylindeFunction(self.Cylinder_IN) == -1):
                return -1

            for i in range(0,count):
                if(self.MoveToCoordinates(self.X_axis, centerPoint[0], 5) == -1):
                    return -1
                time.sleep(0.5)
                if(self.MoveToCoordinates(self.Y_axis, centerPoint[1], 5) == -1):
                    return -1
                time.sleep(0.5)
                if(self.MoveToCoordinates(self.Z_axis, 15, 5) == -1):
                    return -1
                time.sleep(0.5)
                if(self.PushPinDown(self.Pin1) == -1):
                    return -1
                time.sleep(0.5)
                if(self.PushPinDown(self.Pin2) == -1):
                    return -1
                time.sleep(0.5)
                if(self.PushPinDown(self.Pin3) == -1):
                    return -1
                time.sleep(0.5)
                if(self.LiftPinUp(self.Pin1) == -1):
                    return -1
                time.sleep(0.5)
                if(self.LiftPinUp(self.Pin2) == -1):
                    return -1
                time.sleep(0.5)
                if(self.LiftPinUp(self.Pin3) == -1):
                    return -1
                time.sleep(0.5)
                if(self.MoveToCoordinates(self.Z_axis, 0, 5) == -1):
                    return -1
                time.sleep(0.5)
                if(self.MoveToCoordinates(self.X_axis, 0, 5) == -1):
                    return -1
                time.sleep(0.5)
                if(self.MoveToCoordinates(self.Y_axis, 0, 5) == -1):
                    return -1
                time.sleep(0.5)

            if(self.Set_CylindeFunction(self.Cylinder_OUT) == -1):
                return -1

            return 0            
        except:
            self.strErrorMessage = "BurningTestOfV71 error"
            return -1
# ********************************************************************************#

#sensor funtion
#**********************************************************************************#
    def OpenSensorPort(self, serialName=""):
        try:
            port_list = list(serial.tools.list_ports.comports())
            for i in range(0,len(port_list),1):
                print (port_list[i])
            for i in range(0, len(port_list), 1):
                    print (port_list[i].device)
                    self.LigentSerialPort = serial.Serial(port=port_list[i].device,
                                                          baudrate=19200,
                                                          bytesize=8,
                                                          parity='N',
                                                          stopbits=2,
                                                          timeout=0.05)
                    if self.LigentSerialPort.is_open:
                        err = self.AutoChooseLigentCom()
                        if err != 0:
                            self.LigentSerialPort.close()
                        else:
                            self.LigentSerialPortName = port_list[i].device
                            return 0
            print ("open plc serial success")
            return -1
        except:
            self.strErrorMessage = "open sensor port except fail"

    # *****************************************************************************#
    def AutoChooseLigentCom(self):
        try:
            self.LigentSerialPort.write(binascii.unhexlify(self.command_line1))
            time.sleep(0.2)
            ret = binascii.hexlify(self.LigentSerialPort.read(9))
            print (ret)
            if (ret[0:6] == "010304" and ret.__len__() == 18):
                return 0
            else:
                return -1
        except Exception as e:
            self.strErrorMessage = "AutoChooseSensorCom except fail " + "{0}".format(e)
            return -1
    # *****************************************************************************#

    # *****************************************************************************#
    # get l240t one line value
    def GetLigentOneLinePressure(self, command):
        if (self.LigentSerialPort.is_open == False):
            self.strErrorMessage = "The serial port is not opened when GetLigentOneLinePressure write command %s" % command
            return -1
        try:
            for i in range(1,6,1):
                OneLine = self.LigentSerialPort.write(binascii.unhexlify(command))
                time.sleep(0.01*i)
                OriginalValue = binascii.hexlify(self.LigentSerialPort.read(9))
                if (OriginalValue[0:6] == "010304" and len(OriginalValue) == 18):
                    OneLineValue = OriginalValue[6:14]
                    err = int ( OneLineValue, 16 )
                    if (err > 2147483648):
                        err = long ( err )
                        err = err ^ 4294967295
                        err = err + 1
                        err = "-" + str ( err )
                        return round(float(err)/1000.0 ,3)
                    else:
                        err = str ( err )
                        return round(float(err)/1000.0,3)
                else:
                    continue
            return -1
        except Exception as e:
            self.strErrorMessage = "GetLigentOneLinePressure write command %s fail" % command + "{0}".format(e)
            return -1
    # ********************************************************************************#

# ********************************************************************************#
    # get l240t all lines value
    def GetLigentPressure(self, command):
        if (self.LigentSerialPort.is_open == False):
            self.strErrorMessage = "The serial port is not opened when GetLigentPressure write command %s" % command
            return -1
        try:
            for delay in range(1,6,1):
                allLine = self.LigentSerialPort.write ( binascii.unhexlify ( command ) )
                time.sleep ( 0.01*delay )
                allValue = binascii.hexlify ( self.LigentSerialPort.read(21) )
                # print allValue
                if allValue[0:6] == "010310" and len(allValue) == 42:
                    GetReceiveValue_1 = allValue[6:14]
                    GetReceiveValue_1 = int ( GetReceiveValue_1, 16 )

                    GetReceiveValue_2 = allValue[14:22]
                    GetReceiveValue_2 = int ( GetReceiveValue_2, 16 )

                    GetReceiveValue_3 = allValue[22:30]
                    GetReceiveValue_3 = int ( GetReceiveValue_3, 16 )

                    GetReceiveValue_4 = allValue[30:38]
                    GetReceiveValue_4 = int ( GetReceiveValue_4, 16 )

                    list_all = []
                    list_all = [GetReceiveValue_1, GetReceiveValue_2, GetReceiveValue_3, GetReceiveValue_4]
                    for i in range ( 0, 4, 1 ):
                        if (list_all[i] > 2147483648):
                            list_all[i] = long ( list_all[i] )
                            list_all[i] = list_all[i] ^ 4294967295
                            list_all[i] = list_all[i] + 1
                            list_all[i] = round(float("-" + str(list_all[i]))/10000.0,3)
                        else:
                            list_all[i] = round(float(str(list_all[i]))/10000.0,3)
                    return list_all
                # deal except condition
                elif "010310" in allValue and len(allValue) == 42:
                    print (allValue)
                    allValue = allValue.strip().split("010310")
                    allValue = "010310" + allValue[1] + allValue[0]

                    GetReceiveValue_1 = allValue[6:14]
                    GetReceiveValue_1 = int ( GetReceiveValue_1, 16 )

                    GetReceiveValue_2 = allValue[14:22]
                    GetReceiveValue_2 = int ( GetReceiveValue_2, 16 )

                    GetReceiveValue_3 = allValue[22:30]
                    GetReceiveValue_3 = int ( GetReceiveValue_3, 16 )

                    GetReceiveValue_4 = allValue[30:38]
                    GetReceiveValue_4 = int ( GetReceiveValue_4, 16 )

                    list_all = []
                    list_all = [GetReceiveValue_1, GetReceiveValue_2, GetReceiveValue_3, GetReceiveValue_4]
                    for i in range ( 0, 4, 1 ):
                        if (list_all[i] > 2147483648):
                            list_all[i] = long ( list_all[i] )
                            list_all[i] = list_all[i] ^ 4294967295
                            list_all[i] = list_all[i] + 1
                            list_all[i] = round(float("-" + str(list_all[i]))/10000.0,3)
                        else:
                            list_all[i] = round(float(str(list_all[i]))/10000.0,3)
                    return list_all
                else:
                    continue
            return -1
        except Exception as e:
            self.strErrorMessage = "GetLigentPressure write command %s fail" % command + "{0}".format ( e )
            return -1
    # ********************************************************************************#

    # ********************************************************************************#
    # set ligent to zero
    def SetLigentToZero(self, command):
        if (self.LigentSerialPort.isOpen() == False):
            self.strErrorMessage = "The serial port is not opened when CleanAllLines write command %s" % command
            return -1
        try:
            CleanCommand = self.LigentSerialPort.write(binascii.unhexlify(command))
            time.sleep(0.5)
            # if self.LigentSerialPort.is_open == True:
            #     self.LigentSerialPort.close()
            # port_list = list(serial.tools.list_ports.comports())
            # for i in range(0, len(port_list), 1):
            #     if port_list[i].device != self.ser:
            #         print port_list[i].device
            #         self.LigentSerialPort = serial.Serial(port=port_list[i].device,
            #                                               baudrate=19200,
            #                                               bytesize=8,
            #                                               parity='N',
            #                                               stopbits=2,
            #                                               timeout=0.05)
            #         if self.LigentSerialPort.is_open:
            #             err = self.AutoChooseLigentCom()
            #             if err != 0:
            #                 self.LigentSerialPort.close()
            #             else:
            #                 self.LigentSerialPortName = port_list[i].device
            #                 break
            return 0
        except Exception as e:
            self.strErrorMessage = "CleanAllLines write command %s fail" % command + "{0}".format(e)
            return -1
    # ********************************************************************************#

    def CloseSensorPort(self):
        try:

            if self.LigentSerialPort.is_open:
                self.LigentSerialPort.close()
            return 0
        except Exception as e:
            self.strErrorMessage = "CloseSerial except fail " + "{0}".format(e)
            return -1
    # ********************************************************************#





