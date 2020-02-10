'''
For C2F2-Oslo : PLC motion control
Bojay tony_dong@zhbojay.com
Version:V1.6 2019/2/12 update
'''

import os
import serial
import serial.tools.list_ports
import binascii
import struct
import time

class BojayPLCCommandClass:
    def __init__(self):

        self.ReadPLCVersion = "%01#RDD0030000302"
        # Step move
        self.MoveStep_xAxis = "%01#WCSR00201"
        self.MoveStep_yAxis = "%01#WCSR00241"
        self.MoveStep_zAxis = "%01#WCSR00281"
        #Step set
        self.SetStep_xAxis = "%01#WDD0100001001"
        self.SetStep_yAxis = "%01#WDD0100801009"
        self.SetStep_zAxis = "%01#WDD0101601017"
        #Step get
        self.GetStep_xAxis = "%01#RDD0060000601"
        self.GetStep_yAxis = "%01#RDD0060200603"
        self.GetStep_zAxis = "%01#RDD0060400605"
        #Set speed
        self.SetSpeed_xAxis = "%01#WDD0020000201"
        self.SetSpeed_yAxis = "%01#WDD0021000211"
        self.SetSpeed_zAxis = "%01#WDD0022000221"
        #Get speed
        self.GetSpeed_xAxis = "%01#RDD0020000201"
        self.GetSpeed_yAxis = "%01#RDD0021000211"
        self.GetSpeed_zAxis = "%01#RDD0022000221"
        #Set x&y rotation angle and z move distance
        self.SetAngle_xAxis = "%01#WDD0020200203"
        self.SetAngle_yAxis = "%01#WDD0021200213"
        self.SetDistane_zAxis = "%01#WDD0022200223"
        #Move x&y&z
        self.XYMove = "%01#WCSR002F1"
        self.XYZMove = "%01#WCSR002B1"
        self.XMove = "%01#WCSR002C1"
        self.YMove = "%01#WCSR002D1"
        self.ZMove = "%01#WCSR002E1"
        #Get x&y&z
        self.GetCoordiante_xAxis = "%01#RDD0014600147"
        self.GetCoordiante_yAxis = "%01#RDD0015000151"
        self.GetCoordiante_zAxis = "%01#RDD0015400155"
        #Single of moving axis
        self.SingleMoveFinish_xAxis = "%01#RCSR0800"
        self.SingleMoveFinish_yAxis = "%01#RCSR0801"
        self.SingleMoveFinish_zAxis = "%01#RCSR0802"
        self.SingleMoveFinish_xyAxis = "%01#RCSR0803"
        self.SingleMoveFinish_xyzAxis = "%01#RCSR0059"
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
        #set offset PlC
        self.SetHome_xAxis = "%01#WCSR05301"
        self.SetHome_yAxis = "%01#WCSR05311"
        self.SetHome_zAxis = "%01#WCSR05321"
        #reset
        self.ResetCommand_ON ="%01#WCSR00841"
        self.ResetCommand_OFF ="%01#WCSR01040"
        #Sensor
        self.XAisHomeSensor = "%01#RCSX0018"
        self.YAisHomeSensor = "%01#RCSX0015"
        self.ZAisHomeSensor = "%01#RCSX001B"
        self.Check_DUT_Sensor = "%01#RCSX000E"
        #Set E-Stop
        self.SetESTOP_ON = "%01#WCSR00991"
        self.SetESTOP_OFF = "%01#WCSR00990"
        #Set Brake
        self.SetBrakeON = "%01#WCSR40020"
        self.SetBrakeOFF = "%01#WCSR40021"
        #Set Door Sensor state
        self.DoorSensorOFF = "%01#WCSR40011"
        self.DoorSensorON = "%01#WCSR40010"



myBojayPLCCommandClass = BojayPLCCommandClass()


#*****************************************************************************#
class GOEControlClass:
    def __init__(self):
        self.myPLCSerialPort = None
        self.strErrorMessage = ""

        self.Axis_x = 1
        self.Axis_y = 2
        self.Axis_z = 3
        self.Axis_xy = 4
        self.Axis_xyz = 5
        self.MaxLimit = 6
        self.MinLimit = 7
        self.XAxisHomeSensor = 8
        self.YAxisHomeSensor = 9
        self.ZAxisHomeSensor = 10
        self.Check_DUT_Sensor = 11
        self.EStopOff = 12
        self.EStopOn = 13
        self.Sensor_X_Max = 14
        self.Sensor_X_Min = 15
        self.Sensor_X_Origin = 16
        self.Sensor_Y_Max = 17
        self.Sensor_Y_Min = 18
        self.Sensor_Y_Origin = 19
        self.Sensor_Z_Max = 20
        self.Sensor_Z_Min = 21
        self.Sensor_Z_Origin = 22
        self.BrakeON = 23
        self.BrakeOFF = 24
        self.DoorSensorON = 25
        self.DoorSensorOFF = 26

    # ********************************************************************#
    #Open the PLC port
    def OpenSerial(self,serialName=""):
        try:
            port_list = list(serial.tools.list_ports.comports())
            if len(port_list) < 0:
                self.strErrorMessage = "There is no serial port"
                return -1
            if len(serialName) < 1:
                for i in range(0,len(port_list),1):
                    print port_list[i].device
                    self.myPLCSerialPort = serial.Serial(port=port_list[i].device,
                                                 timeout=0.01,
                                                 baudrate=115200,
                                                 parity=serial.PARITY_ODD)
                    if self.myPLCSerialPort.is_open:
                        err = self.AutoChooseCom()
                        if err != 0:
                            self.myPLCSerialPort.close()
                        else:
                            return 0
                self.strErrorMessage = "Did not find suitable serial port"
                return -1
            else:
                self.myPLCSerialPort = serial.Serial(port=serialName,
                                                     timeout=0.01,
                                                     baudrate=115200,
                                                     parity=serial.PARITY_ODD)
                return 0
        except:
            self.strErrorMessage = "OpenSerial except fail"
            print self.strErrorMessage
            return -1

    # ********************************************************************#

    # ********************************************************************#
    def AutoChooseCom(self):
        try:
            bcc = self.__bccValue("%01#RDD0015400155")
            command = "%01#RDD0015400155" + bcc + '\r'
            command = command.upper()
            ret = self.myPLCSerialPort.write(command)
            print ret
            time.sleep(0.5)
            readString = self.myPLCSerialPort.read_all()
            if len(readString) > 0:
                print readString
                return 0
            return -1
        except:
            self.strErrorMessage = "AutoChooseCom except fail"
            return -1
    # ********************************************************************#

    # ********************************************************************#
    def CloseSerial(self):
        try:
            if self.myPLCSerialPort.is_open:
                self.myPLCSerialPort.close()
            return 0
        except:
            self.strErrorMessage = "CloseSerial except fail"
            return -1
    # ********************************************************************#

    # ********************************************************************#
    def GetCurrentCoordinate(self,ofWhatAxis):
        try:
            if (ofWhatAxis == self.Axis_x):
                command = myBojayPLCCommandClass.GetCoordiante_xAxis
            elif (ofWhatAxis == self.Axis_y):
                command = myBojayPLCCommandClass.GetCoordiante_yAxis
            elif (ofWhatAxis == self.Axis_z):
                command = myBojayPLCCommandClass.GetCoordiante_zAxis

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
    def MoveToCoordinates(self,ofWhatAxis,Value,timeout=10):
        try:
            finalByte = self.__flipByte(Value)
            #start to move
            if ofWhatAxis == self.Axis_x:
                command = myBojayPLCCommandClass.SetAngle_xAxis + finalByte
                MoveCommand = myBojayPLCCommandClass.XMove
            elif ofWhatAxis == self.Axis_y:
                command = myBojayPLCCommandClass.SetAngle_yAxis + finalByte
                MoveCommand = myBojayPLCCommandClass.YMove
            elif ofWhatAxis == self.Axis_z:
                command = myBojayPLCCommandClass.SetDistane_zAxis + finalByte
                MoveCommand = myBojayPLCCommandClass.ZMove
            ret = self.__writeRead(command)
            if ret != 0:
                self.strErrorMessage = "MoveToCoordinates write distance fail"
                print "MoveToCoordinates write distance fail"
                return -1

            ret = self.__writeRead(MoveCommand)
            if ret != 0:
                self.strErrorMessage = "MoveToCoordinates move fail"
                print "MoveToCoordinates move fail"
                return -1

            mytimeCount = 0
            while (self.GetmoveSignal(ofWhatAxis) == 1):
                time.sleep(0.005)
                mytimeCount = mytimeCount + 0.005
            if mytimeCount >= timeout:
                self.strErrorMessage = "MoveToCoordinates time out"
                print "MoveToCoordinates time out"
                return -1
            time.sleep(0.05)
            current_value = self.GetCurrentCoordinate(ofWhatAxis)
            print current_value
            if (Value == current_value):
                return 0
            else:
                return -1
        except:
            self.strErrorMessage = "MoveToCoordinates except fail"
            return -1
    # ********************************************************************#

    # ********************************************************************#
    def SetStepValue(self, ofWhatAxis, Value):
        try:
            finalByte = self.__flipByte(Value)
            if ofWhatAxis == self.Axis_x:
                command = myBojayPLCCommandClass.SetStep_xAxis + finalByte
            elif ofWhatAxis == self.Axis_y:
                command = myBojayPLCCommandClass.SetStep_yAxis + finalByte
            elif ofWhatAxis == self.Axis_z:
                command = myBojayPLCCommandClass.SetStep_zAxis + finalByte
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
                command = myBojayPLCCommandClass.GetStep_xAxis
            elif(ofWhatAxis == self.Axis_y):
                command = myBojayPLCCommandClass.GetStep_yAxis
            elif(ofWhatAxis == self.Axis_z):
                command = myBojayPLCCommandClass.GetStep_zAxis
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
            return value
        except:
            self.strErrorMessage = "GetStepValue except fail"
            return -1
    # ********************************************************************#

    # ********************************************************************#
    def MoveStep(self, ofWhatAxis, value, timeout=10):
        try:
            # set step
            ret = self.SetStepValue(ofWhatAxis, value)
            if ret != 0:
                return -1

            #start to move
            if (ofWhatAxis == self.Axis_x):
                command = myBojayPLCCommandClass.MoveStep_xAxis
            elif (ofWhatAxis == self.Axis_y):
                command = myBojayPLCCommandClass.MoveStep_yAxis
            elif (ofWhatAxis == self.Axis_z):
                command = myBojayPLCCommandClass.MoveStep_zAxis
            time.sleep(0.2)

            ret = self.__writeRead(command)
            if (ret == -1):
                self.strErrorMessage = "MoveStep fail"
                return -1
            #wait finsh
            mytimeCount = 0
            while (self.GetmoveSignal(ofWhatAxis) == 1):
                time.sleep(0.1)
                mytimeCount = mytimeCount + 0.1
                if mytimeCount >= timeout:
                    self.strErrorMessage = "MoveStep time out"
                    return -1
            return 0
        except:
            self.strErrorMessage = "Move step except fail"
            return -1
    # ********************************************************************#

    # ********************************************************************#
    def SetSpeed(self, ofWhatAxis, Value):
        try:
            if ofWhatAxis == self.Axis_x:
                if Value >= 500:
                    Value = 500
                if Value <= 2:
                    Value = 2
                command = myBojayPLCCommandClass.SetSpeed_xAxis
            elif ofWhatAxis == self.Axis_y:
                if Value >= 500:
                    Value = 500
                if Value <= 2:
                    Value = 2
                command = myBojayPLCCommandClass.SetSpeed_yAxis
            elif ofWhatAxis == self.Axis_z:
                if Value >= 250:
                    Value = 250
                if Value <= 2:
                    Value = 2
                command = myBojayPLCCommandClass.SetSpeed_zAxis

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

    # ********************************************************************#
    def GetSpeed(self, ofWhatAxis):
        try:
            if ofWhatAxis == self.Axis_x:
                command = myBojayPLCCommandClass.GetSpeed_xAxis
            elif ofWhatAxis == self.Axis_y:
                command = myBojayPLCCommandClass.GetSpeed_yAxis
            elif ofWhatAxis == self.Axis_z:
                command = myBojayPLCCommandClass.GetSpeed_zAxis
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

    # ********************************************************************#
    def SetLimit(self,ofWhatLimit,ofWhatAxis,Limit):
        try:
            if ofWhatAxis == self.Axis_x:
                if ofWhatLimit == self.MaxLimit:
                    command = myBojayPLCCommandClass.SetMaxLimit_xAxis
                elif ofWhatLimit == self.MinLimit:
                    command = myBojayPLCCommandClass.SetMinLimit_xAxis
            elif ofWhatAxis == self.Axis_y:
                if ofWhatLimit == self.MaxLimit:
                    command = myBojayPLCCommandClass.SetMaxLimit_yAxis
                elif ofWhatLimit == self.MinLimit:
                    command = myBojayPLCCommandClass.SetMinLimit_yAxis
            elif ofWhatAxis == self.Axis_z:
                if ofWhatLimit == self.MaxLimit:
                    command = myBojayPLCCommandClass.SetMaxLimit_zAxis
                elif ofWhatLimit == self.MinLimit:
                    command = myBojayPLCCommandClass.SetMinLimit_zAxis
            finalByte = self.__flipByte(Limit)
            command = command + finalByte
            ret = self.__writeRead(command)
            if ret != 0:
                self.strErrorMessage = "SetLimit:set Limit fail"
                return -1
            return 0
        except:
            self.strErrorMessage = "SetLimit except fail"
            return -1
    # ********************************************************************#

    # ********************************************************************#
    def GetLimit(self, ofWhatAxis, ofWhatLimit):
        try:
            if ofWhatAxis == self.Axis_x:
                if ofWhatLimit == self.MaxLimit:
                    command = myBojayPLCCommandClass.GetMaxLimit_xAxis
                elif ofWhatLimit == self.MinLimit:
                    command = myBojayPLCCommandClass.GetMinLimit_xAxis
            elif ofWhatAxis == self.Axis_y:
                if ofWhatLimit == self.MaxLimit:
                    command = myBojayPLCCommandClass.GetMaxLimit_yAxis
                elif ofWhatLimit == self.MinLimit:
                    command = myBojayPLCCommandClass.GetMinLimit_yAxis
            elif ofWhatAxis == self.Axis_z:
                if ofWhatLimit == self.MaxLimit:
                    command = myBojayPLCCommandClass.GetMaxLimit_zAxis
                elif ofWhatLimit == self.MinLimit:
                    command = myBojayPLCCommandClass.GetMinLimit_zAxis

            #write data
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

    # ********************************************************************#
    def SignalReset(self,timeout=30):
        try:
            command = myBojayPLCCommandClass.ResetCommand_ON
            bcc = self.__bccValue(command)
            command = command + bcc + '\r'
            ret = self.__writeRead(command)
            if ret != 0:
                self.strErrorMessage = "SignalReset fail"
                return -1

            mytimeCount = 0
            while(self.GetHomeFinishState(self.Axis_xyz) == 1):
                if (mytimeCount > timeout):
                    self.strErrorMessage = "SignalReset Resrt time out"
                    return -1
                time.sleep(0.5)
                mytimeCount = mytimeCount + 0.5
            if mytimeCount > timeout:
                self.strErrorMessage = "SignalReset out"
                return -1

            command = myBojayPLCCommandClass.ResetCommand_OFF
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

    # ********************************************************************#
    def GetHomeFinishState(self, ofWhatAxis):
        try:
            if ofWhatAxis == self.Axis_x:
                command = myBojayPLCCommandClass.SingleHomeFinish_xAxis
            elif ofWhatAxis == self.Axis_y:
                command = myBojayPLCCommandClass.SingleHomeFinish_yAxis
            elif ofWhatAxis == self.Axis_z:
                command = myBojayPLCCommandClass.SingleHomeFinish_zAxis
            elif ofWhatAxis == self.Axis_xyz:
                command = myBojayPLCCommandClass.SingleHomeFinish_xyzAxis

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

    # ********************************************************************#
    def GetmoveSignal(self, ofWhatAxis):
        try:
            if ofWhatAxis == self.Axis_x:
                command = myBojayPLCCommandClass.SingleMoveFinish_xAxis
            elif ofWhatAxis == self.Axis_y:
                command = myBojayPLCCommandClass.SingleMoveFinish_yAxis
            elif ofWhatAxis == self.Axis_z:
                command = myBojayPLCCommandClass.SingleMoveFinish_zAxis
            elif ofWhatAxis == self.Axis_xy:
                command = myBojayPLCCommandClass.SingleMoveFinish_xyAxis
            elif ofWhatAxis == self.Axis_xyz:
                command = myBojayPLCCommandClass.SingleMoveFinish_xyzAxis

            bcc = self.__bccValue(command)
            command = command + bcc + '\r'
            command = command.upper()
            self.myPLCSerialPort.write(command)
            readString = self.ReadData(0.01)
            if ("fail" in readString or readString == 0):
                self.strErrorMessage = "GetmoveSignal read time out"
                return -1
            else:
                iread = int(readString[6])
                return iread
        except:
            self.strErrorMessage = "GetmoveSignal except fail"
            return -1
    # ********************************************************************#

    # ********************************************************************#
    def SetEStop(self, state):
        try:
            if state == self.EStopOff:
                command = myBojayPLCCommandClass.SetESTOP_OFF
            elif state == self.EStopOn:
                command = myBojayPLCCommandClass.SetESTOP_ON
            else:
                self.strErrorMessage = "SetEStop Input parameter error"
                return -1
            readString = self.__writeRead(command)
            return readString
        except:
            self.strErrorMessage = "SetEStop error"
            return -1

    # ********************************************************************#

    # ********************************************************************#
    def GetErrorMessage(self):
        return self.strErrorMessage

    # ********************************************************************#

    # ********************************************************************#
    def SetHomePLC(self, ofWhatAxis):
        try:
            if ofWhatAxis == self.Axis_x:
                command = myBojayPLCCommandClass.SetHome_xAxis
            elif ofWhatAxis == self.Axis_y:
                command = myBojayPLCCommandClass.SetHome_yAxis
            elif ofWhatAxis == self.Axis_z:
                command = myBojayPLCCommandClass.SetHome_zAxis
            ret = self.__writeRead(command)
            if ret != 0:
                self.strErrorMessage = "OffHome fail"
                return -1
            return 0
        except:
            self.strErrorMessage = "OffHome except fail"
            return -1
    # ********************************************************************#

    # ********************************************************************#
    def Brake(self,status):
        try:
            if status == self.BrakeOFF:
                command = myBojayPLCCommandClass.SetBrakeOFF
            elif status == self.BrakeON:
                command = myBojayPLCCommandClass.SetBrakeON
            else:
                self.strErrorMessage = "Set Brake Input parameter error"
                return -1
            readString = self.__writeRead(command)
            return readString
        except:
            self.strErrorMessage = "Set Brake error"
            return -1

    # ********************************************************************#

    # ********************************************************************#
    def GetSensorStatus(self, ofWhatSensor):
        if (self.myPLCSerialPort.isOpen() == False):
            self.strErrorMessage = "The serial port is not opened"
            return -1
        # X-axis Sensor
        if (ofWhatSensor == self.Sensor_X_Max):
            command = '%01#RCSX0015'
        elif (ofWhatSensor == self.Sensor_X_Min):
            command = '%01#RCSX0014'
        # Y-axis Sensor
        elif (ofWhatSensor == self.Sensor_Y_Origin):
            command = '%01#RCSX0011'
        # Z-axis Sensor
        elif (ofWhatSensor == self.Sensor_Z_Max):
            command = '%01#RCSX0017'
        elif (ofWhatSensor == self.Sensor_Z_Min):
            command = '%01#RCSX0016'
        else:
            self.strErrorMessage = "GetSensorStatus Input parameter error"
            return -1
        ret = self.__readONorOFF(command)
        ret = int(ret)
        if (ret == -1):
            self.strErrorMessage = "GetSensorStatus Read command fail"
            return -1
        return ret

    # ********************************************************************#

    # ********************************************************************#
    def SetDoorSensor(self,status):
        try:
            if status == self.DoorSensorOFF:
                command = myBojayPLCCommandClass.DoorSensorOFF
            elif status == self.DoorSensorON:
                command = myBojayPLCCommandClass.DoorSensorON
            else:
                self.strErrorMessage = "Set Brake Input parameter error"
                return -1
            readString = self.__writeRead(command)
            return readString
        except:
            self.strErrorMessage = "Set Brake error"
            return -1
    # ********************************************************************#
    def GetDoorSensor(self):
        command = '%01#RCSX0000'
        ret = self.__readONorOFF(command)
        ret = int(ret)
        if (ret == -1):
            self.strErrorMessage = "GetDoorSensorStatus Read command fail"
            return -1
        return ret

    # ********************************************************************#
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
    def ReadData(self, timeDelay):
        try:
            for i in range(0, 1, 5):
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
