'''
For B50 keyboard : PLC motion control
Bojay tony_dong@zhbojay.com
Version:V1.0 2018/11/20 update
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
        self.MoveForwardStep_xAxis = "%01#WCSR00201"
        self.MoveBackwardStep_xAxis = "%01#WCSR00211"
        self.MoveForwardStep_yAxis = "%01#WCSR00241"
        self.MoveBackwardStep_yAxis = "%01#WCSR00251"
        self.MoveForwardStep_zAxis = "%01#WCSR00281"
        self.MoveBackwardStep_zAxis = "%01#WCSR00291"
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
        #Set move distance
        self.SetDistane_xAxis = "%01#WDD0020200203"
        self.SetDistane_yAxis = "%01#WDD0021200213"
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
        #self.SingleMoveFinish_xyzAxis = "%01#RCSR0059"
        self.SingleHomeFinish_xAxis = "%01#RCSR0100"
        self.SingleHomeFinish_yAxis = "%01#RCSR0101"
        self.SingleHomeFinish_zAxis = "%01#RCSR0102"
        self.SingleHomeFinish_xyzAxis = "%01#RCSR0104"


        #Get Limit
        self.GetMaxLimit_xAxis = "%01#RDD0062000621"
        self.GetMaxLimit_yAxis = "%01#RDD0062200623"
        self.GetMaxLimit_zAxis = "%01#RDD0062400625"
        self.GetMinLimit_xAxis = "%01#RDD0063000631"
        self.GetMinLimit_yAxis = "%01#RDD0063200633"
        self.GetMinLimit_zAxis = "%01#RDD0063400635"

        #Set Limit
        self.SetMaxLimit_xAxis = "%01#WDD0210002101"
        self.SetMinLimit_xAxis = "%01#WDD0210402105"
        self.SetMaxLimit_yAxis = "%01#WDD0210802109"
        self.SetMinLimit_yAxis = "%01#WDD0211202113"
        self.SetMaxLimit_zAxis = "%01#WDD0211602117"
        self.SetMinLimit_zAxis = "%01#WDD0212002121"


        #reset
        self.ResetCommand_ON ="%01#WCSR00841"
        self.ResetCommand_OFF ="%01#WCSR00840"


        #Sensor
        self.CylinderSensorIn = "%01#RCSX0011"
        self.CylinderSensorOut = "%01#RCSX0012"
        self.CalibrateSensor = "%01#RCSX001F"
        self.threeSensor = "%01#RCSR0010"

        #Cylinder
        self.TrayCylinderOut_ON = "%01#WCSR02061"
        self.TrayCylinderIn_ON = "%01#WCSR02041"
        self.TrayCylinderOut_OFF = "%01#WCSR02060"
        self.TrayCylinderIn_OFF = "%01#WCSR02040"

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
        self.Out = 8
        self.In = 9

        self.CylinderSensorIn = 10
        self.CylinderSensorOut = 11
        self.CalibrateSensor = 12

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

    # ********************************************************************#
    #Open the PLC port
    def OpenSerial(self,serialName=""):
        try:
            port_list = list(serial.tools.list_ports.comports())
            if len(port_list) < 0:
                self.strErrorMessage = "There is no serial port"
                return -1

            # for i in range(0,len(port_list),1):
            #     print port_list[i].device
                #if "usbserial" in port_list[i].device:
            self.myPLCSerialPort = serial.Serial(port=serialName,
                                             timeout=1,
                                             baudrate=115200,
                                             parity=serial.PARITY_ODD)
            #self.myPLCSerialPort.close()
            if self.myPLCSerialPort.is_open:
                err = self.AutoChooseCom()
                if err != 0:
                    self.myPLCSerialPort.close()
                else:
                    return 0
            else:
                self.strErrorMessage = "OpenSerial did not open"
                return -1

            self.strErrorMessage = "OpenSerial:did not find suitable serial port"
            return -1
        except:
            self.strErrorMessage = "OpenSerial except fail"
            return -1

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
            if len(readStr) > 0:
                print readStr
                return 0
            return -1
        except:
            self.strErrorMessage = "AutoChooseCom except fail"
            return -1
    # ********************************************************************#



    # ********************************************************************#
    #Close the PLC port
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
    #Get current coordinate
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
    #Moving to specified Coordinates per Axis
    def MoveToCoordinates(self,ofWhatAxis,Value,timeout=10):
        try:
            finalByte = self.__flipByte(Value)
            if ofWhatAxis == self.Axis_x:
                command = myBojayPLCCommandClass.SetDistane_xAxis + finalByte
                MoveCommand = myBojayPLCCommandClass.XMove
                moveFinishCommand = myBojayPLCCommandClass.SingleMoveFinish_xAxis
            elif ofWhatAxis == self.Axis_y:
                command = myBojayPLCCommandClass.SetDistane_yAxis + finalByte
                MoveCommand = myBojayPLCCommandClass.YMove
                moveFinishCommand = myBojayPLCCommandClass.SingleMoveFinish_yAxis
            elif ofWhatAxis == self.Axis_z:
                command = myBojayPLCCommandClass.SetDistane_zAxis + finalByte
                MoveCommand = myBojayPLCCommandClass.ZMove
                moveFinishCommand = myBojayPLCCommandClass.SingleMoveFinish_zAxis
            ret = self.__writeRead(command)
            if ret != 0:
                self.strErrorMessage = "MoveToCoordinates write distance fail"
                return -1

            ret = self.__writeRead(MoveCommand)
            if ret != 0:
                self.strErrorMessage = "MoveToCoordinates move fail"
                return -1

            mytimeCount = 0
            while (self.GetmoveSignal(ofWhatAxis) == 1):
                time.sleep(0.005)
                mytimeCount = mytimeCount + 0.005
            if mytimeCount >= timeout:
                self.strErrorMessage = "MoveToCoordinates time out"
                return -1
            else:
                return 0
        except:
            self.strErrorMessage = "MoveToCoordinates except fail"
            return -1
    # ********************************************************************#



    # ********************************************************************#
    #x and y move
    def SynchronousXY(self,xValue,yValue,timeout=10):
        try:
            #return 0
            finalByte = self.__flipByte(xValue)
            command = myBojayPLCCommandClass.SetDistane_xAxis + finalByte
            ret = self.__writeRead(command)
            if(ret != 0):
                self.strErrorMessage =  "SynchronousXY x fail"
                return -1
            finalByte = self.__flipByte(yValue)
            command = myBojayPLCCommandClass.SetDistane_yAxis + finalByte
            ret = self.__writeRead(command)
            if(ret != 0):
                self.strErrorMessage = "SynchronousXY y fail"
                return -1
            bcc = self.__bccValue(myBojayPLCCommandClass.XYMove)
            command = myBojayPLCCommandClass.XYMove + bcc + '\r'
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
    # Set Increment / Decrement Value
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
            self.ser.write(command)
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
    def MoveStep(self, ofWhatAxis,timeout=10):
        try:
            if (ofWhatAxis == self.Axis_x):
                command = myBojayPLCCommandClass.MoveForwardStep_xAxis
            elif(ofWhatAxis == self.Axis_y):
                command = myBojayPLCCommandClass.MoveForwardStep_yAxis
            elif(ofWhatAxis == self.Axis_z):
                command = myBojayPLCCommandClass.MoveForwardStep_zAxis

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





    # ********************************************************************#
    # Set speed
    def SetSpeed(self, ofWhatAxis, Value):
        try:
            if ofWhatAxis < self.Axis_xy:
                if ofWhatAxis == self.Axis_x:
                    command = myBojayPLCCommandClass.SetSpeed_xAxis
                elif ofWhatAxis == self.Axis_y:
                    command = myBojayPLCCommandClass.SetSpeed_yAxis
                elif ofWhatAxis == self.Axis_z:
                    command = myBojayPLCCommandClass.SetSpeed_zAxis

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
                        command = myBojayPLCCommandClass.SetSpeed_xAxis
                    elif i == 1:
                        command = myBojayPLCCommandClass.SetSpeed_yAxis
                    elif i == 2:
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
    # Get speed
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
    # Set Limit of X / Y / Z axis
    def SetLimit(self, ofWhatAxis,ofWhatLimit,Limit):
        try:
            if ofWhatAxis == self.Axis_x:
                if ofWhatLimit == self.MaxLimit:
                    command = myBojayPLCCommandClass.SetMaxLimit_xAxis
                elif ofWhatAxis == self.MinLimit:
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
            if ret == 0:
                return 0
            else:
                return -1
        except:
            self.strErrorMessage = "SetLimit except fail"
            return -1
    # ********************************************************************#

    # ********************************************************************#
    # Get Limit of X / Y / Z axis
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
    #will finish this latter
    def GetSensorStatus(self, ofWhatSensor):
        try:
            if ofWhatSensor == self.CylinderSensorIn:
                command = myBojayPLCCommandClass.CylinderSensorIn
            elif ofWhatSensor == self.CylinderSensorOut:
                command = myBojayPLCCommandClass.CylinderSensorOut
            elif ofWhatSensor == self.CalibrateSensor:
                command = myBojayPLCCommandClass.CalibrateSensor


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
    #will finish this latter
    def StartButtonsTriggered(self, action):
        pass
    # ********************************************************************#



    # ********************************************************************#
    def SignalReset(self,timeout=10):
        try:
            mytimeCount = 0
            command = myBojayPLCCommandClass.ResetCommand_ON
            bcc = self.__bccValue(command)
            command = command + bcc + '\r'
            ret = self.__writeRead(command)
            if ret != 0:
                self.strErrorMessage = "SignalReset fail"
                return -1

            mytimeCount = 0
            while (self.GetHomeFinishState(self.Axis_xyz) == 1):
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
            return
        except:
            self.strErrorMessage = "SignalReset except fail"
            return -1
    # ********************************************************************#


    # ********************************************************************#
    #check the single of moveing axis
    def GetmoveSignal(self, ofWhatAxis):
        try:
            if ofWhatAxis == self.Axis_x:
                command = myBojayPLCCommandClass.SingleMoveFinish_xAxis
            elif ofWhatAxis ==self.Axis_y:
                command = myBojayPLCCommandClass.SingleMoveFinish_yAxis
            elif ofWhatAxis ==self.Axis_z:
                command = myBojayPLCCommandClass.SingleMoveFinish_zAxis
            elif ofWhatAxis ==self.Axis_xy:
                command = myBojayPLCCommandClass.SingleMoveFinish_xyAxis
            elif ofWhatAxis ==self.Axis_xyz:
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
    def Set_CylinderFunction(self, direction,timeout=10):
        try:
            if direction == self.Out:
                #threeSensorCommand = myBojayPLCCommandClass.threeSensor
                command = myBojayPLCCommandClass.TrayCylinderOut_ON
                sensorCommand = self.CylinderSensorOut
                commandOff = myBojayPLCCommandClass.TrayCylinderOut_OFF
                bNeedOff = 1
            elif direction == self.In:
                threeSensorCommand = myBojayPLCCommandClass.threeSensor
                command = myBojayPLCCommandClass.TrayCylinderIn_ON
                sensorCommand = self.CylinderSensorIn
                commandOff = myBojayPLCCommandClass.TrayCylinderIn_OFF
                bNeedOff = 1

                ret = self.__readONorOFF(threeSensorCommand)
                ret = int(ret)
                if ret != 1:
                    self.strErrorMessage = "GetSensorStatus fail"
                    return -1


            ret = self.__writeRead(command)
            if (ret != 0):
                self.strErrorMessage = "Set_CylinderFunction write command fail"
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
            if(bNeedOff == 1):
                ret = self.__writeRead(commandOff)
                if (ret != 0):
                    self.strErrorMessage = "Set_CylinderFunction write command fail"
                    return -1
                else:
                    return 0
        except:
            self.strErrorMessage = "Set_CylindeFunction except fail"
            return -1
    # ********************************************************************#

    # ********************************************************************#
    def LoadCalbrationInitialFile(self):
        try:
            #1:Get initial calibration coordinate
            calInitialFile = os.getcwd() + "//CalibrationInitial.txt"
            if not os.path.exists(calInitialFile):
                self.strErrorMessage = "CalibrationInitial.txt does not exist"
                return -1
            with open(calInitialFile,"r") as reader:
                for line in reader.readlines():
                    index = line.find("=")
                    if index < 0:
                        continue
                    line = line.strip().strip('\n')
                    if "ZIncrementX" in line:
                        self.ZIncrementx = float(line[index+1:])
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
    def CalibrationMove(self,ofWhatAxis,direction):
        try:
            ret = self.SetStepValue(ofWhatAxis,0.5*direction)
            if ret != 0:
                return -1

            calStep = 0
            while True:
                ret = self.GetSensorStatus(self.CalibrateSensor)
                if ret == -1:
                    return -1
                elif ret == 0:
                    ret = self.MoveStep()
                elif ret == 1:
                    ret = self.SetStepValue(ofWhatAxis, step * direction*-1)
                    if ret != 0:
                        return -1
                    calStep = calStep + 1
                    if calStep == 1:
                        step = 0.1
                    elif calStep == 2:
                        step = 0.01
                    else:
                        break
                    ret = self.SetStepValue(ofWhatAxis,step*direction)
                    if ret != 0:
                        return -1
            return 0
        except:
            self.strErrorMessage = "CalibrationMove except fail"
            return -1

    # ********************************************************************#
    def Calibrate(self,ofWhichAxis, incrementOrDecrement):
        try:
            shouldCalibrate = 1
            LoopCounter = 0
            Coordinates = 0.0
            isSuccess = 0
            if ("increment" in incrementOrDecrement):
                StepValue = 0.05
            if ("decrement" in incrementOrDecrement):
                StepValue = -0.05
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
                        ret = self.GetCurrentCoordinate(ofWhichAxis)
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
    def Calibration(self,*args,**kwargs):
        try:
            self.SetUpx = kwargs["Upx"]
            self.SetUpy = kwargs["Upy"]
            self.SetLeftx = kwargs["Leftx"]
            self.SetLefty = kwargs["Lefty"]
            self.SetDownx = kwargs["Downx"]
            self.SetDowny = kwargs["Downy"]
            self.SetRightx = kwargs["Rightx"]
            self.SetRighty = kwargs["Righty"]
            self.SetZx = kwargs["Zx"]
            self.SetZy = kwargs["Zy"]
            self.offset = kwargs["offset"]

            #1:Load cal initial file
            ret = self.LoadCalbrationInitialFile()
            if ret != 0:
                return -1

            #2:z axis move
            ret = self.MoveToCoordinates(self.Axis_z,31)
            if ret != 0:
                return -1

            #3:set speed
            ret = self.SetSpeed(self.Axis_xyz,6)
            if ret != 0:
                return -1

            #4:calibrate z axis
            print self.ZIncrementx,self.ZIncrementy
            ret = self.SynchronousXY(self.ZIncrementx,self.ZIncrementy)
            if ret != 0:
                return -1
            CalibrationBlockHeight = self.offset
            Zvsl_Finsl = self.Calibrate(self.Axis_z, "increment")
            Zvsl_Finsl = Zvsl_Finsl + CalibrationBlockHeight
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
            ret = self.MoveToCoordinates(self.Axis_z, 38)
            if ret != 0:
                return -1
            Xvsl_Dec = self.Calibrate(self.Axis_x, "increment")
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
            ret = self.MoveToCoordinates(self.Axis_z, 38)
            if ret != 0:
                return -1
            Xvsl_Inc = self.Calibrate(self.Axis_x, "decrement")
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
            ret = self.MoveToCoordinates(self.Axis_z, 38)
            if ret != 0:
                return -1
            Yvsl_Dec = self.Calibrate(self.Axis_y, "increment")
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
            ret = self.MoveToCoordinates(self.Axis_z, 38)
            if ret != 0:
                return -1
            Yvsl_Inc = self.Calibrate(self.Axis_y, "decrement")
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





    # **************************************************************#
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
    # Write and Read Command
    def __writeRead(self, command):
        try:
            bcc = self.__bccValue(command)
            command = command + bcc + '\r'
            command = command.upper()
            self.myPLCSerialPort.write(command)
            readString = self.ReadData(0.05)
            if (readString[3] == '$'):
                return 0
            else:
                return -1
        except:
            return -1
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