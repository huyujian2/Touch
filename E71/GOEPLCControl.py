'''
Version 1.03 2019/09/17 update
author tony_dong@zhbojay.com
add USBEableOrDisable && DUTLockOrUnlock && PowerEnableOrDisable
interpreter python3 || python2

'''
import time
import serial
import serial.tools.list_ports
import io
import struct
import sys,os
import binascii
import datetime
import math
import platform

Interpreter = platform.python_version()[0]
print(Interpreter)


class BojayPLCCommandClass:

    ReadPLCVersion = '%01#RDD0030000302'

    # Step move
    MoveStep_xAxis = '%01#WCSR00201'
    MoveStep_yAxis = '%01#WCSR00241'
    MoveStep_zAxis = '%01#WCSR00281'

    # Step set
    SetStep_xAxis = '%01#WDD0100001001'
    SetStep_yAxis = '%01#WDD0100801009'
    SetStep_zAxis = '%01#WDD0101601017'

    # Step get
    GetStep_xAxis = '%01#RDD006000060054'
    GetStep_yAxis = '%01#RDD006020060254'
    GetStep_zAxis = '%01#RDD006040060454'

    # Set speed
    SetSpeed_xAxis = '%01#WDD0020000201'
    SetSpeed_yAxis = '%01#WDD0021000211'
    SetSpeed_zAxis = '%01#WDD0022000221'

    # Get speed
    GetSpeed_xAxis = '%01#RDD0020000201'
    GetSpeed_yAxis = '%01#RDD0021000211'
    GetSpeed_zAxis = '%01#RDD0022000221'

    # Set move distance
    SetDistance_xAxis = '%01#WDD0020200203'
    SetDistance_yAxis = '%01#WDD0021200213'
    SetDistance_zAxis = '%01#WDD0022200223'

    # Move x&y&z
    XYMove = '%01#WCSR002F1'
    # XYZMove = "%01#WCSR002B1"
    XMove = '%01#WCSR002C1'
    YMove = '%01#WCSR002D1'
    ZMove = '%01#WCSR002E1'

    # Get x&y&z
    GetCoordiante_xAxis = '%01#RDD0014600147'
    GetCoordiante_yAxis = '%01#RDD0015000151'
    GetCoordiante_zAxis = '%01#RDD0015400155'

    # Single of moving axis
    SingleMoveFinish_xAxis = '%01#RCSR0052'
    SingleMoveFinish_yAxis = '%01#RCSR0054'
    SingleMoveFinish_zAxis = '%01#RCSR0056'
    SingleMoveFinish_xyAxis = '%01#RCSR005C'
    # SingleMoveFinish_xyzAxis = '%01#RCSR0059'
    SingleHomeFinish_xAxis = '%01#RCSR0100'
    SingleHomeFinish_yAxis = '%01#RCSR0101'
    SingleHomeFinish_zAxis = '%01#RCSR0102'
    SingleHomeFinish_xyzAxis = '%01#RCSR0104'

    # Get Limit
    GetMaxLimit_xAxis = '%01#RDD0062000621'
    GetMaxLimit_yAxis = '%01#RDD0062200623'
    GetMaxLimit_zAxis = '%01#RDD0062400625'
    GetMinLimit_xAxis = '%01#RDD0063000631'
    GetMinLimit_yAxis = '%01#RDD0063200633'
    GetMinLimit_zAxis = '%01#RDD0063400635'

    # Set Limit
    SetMaxLimit_xAxis = '%01#WDD0210002101'
    SetMinLimit_xAxis = '%01#WDD0210402105'
    SetMaxLimit_yAxis = '%01#WDD0210802109'
    SetMinLimit_yAxis = '%01#WDD0211202113'
    SetMaxLimit_zAxis = '%01#WDD0211602117'
    SetMinLimit_zAxis = '%01#WDD0212002121'

    # reset
    ResetCommand_ON = '%01#WCSR00841'
    ResetCommand_OFF = '%01#WCSR00840'

    # Sensor axis
    XAisHomeSensor = '%01#RCSX0018'
    XAxisLLSensor = '%01#RCSX0019'
    XAxisHLSensor = '%01#RCSX001A'

    YAisHomeSensor = '%01#RCSX0015'
    YAxisLLSensor = '%01#RCSX0016'
    YAxisHLSensor = '%01#RCSX0017'

    ZAisHomeSensor = '%01#RCSX001B'
    ZAxisLLSensor = '%01#RCSX001C'
    ZAxisHLSensor = '%01#RCSX001D'

    CylinderInSensor = '%01#RCSX0011'
    CylinderOutSensor = '%01#RCSX0012'

    CurtainSensor = '%01#RCSX0010'
    CalibrationSensor = '%01#RCSX001F'

    # E71
    EnableUSB1 = '%01#WCSR01221'
    EnableUSB2 = "%01#WCSR01421"
    EnableUSB_all = '%01#WCSR01291'
    DisableUSB1 = '%01#WCSR01220'
    DisableUSB2 = "%01#WCSR01420"
    DisableUSB_all = '%01#WCSR01290'
    USB1Sensor = "%01#RCSX0302"
    USB2Sensor = "%01#RCSX0303"

    EnablePower1 = '%01#WCSR01201'
    EnablePower2 = '%01#WCSR01401'
    EnablePower_all = '%01#WCSR01271'
    DisablePower1 = '%01#WCSR01200'
    DisablePower2 = '%01#WCSR01400'
    DisablePower_all = '%01#WCSR01270'
    Power1Sensor = "%01#RCSX0300"
    Power2Sensor = "%01#RCSX0301"

    LockDUT1 = '%01#WCSR01241'
    LockDUT2 = "%01#WCSR01441"
    LockDUT_all = '%01#WCSR012B1'
    UnlockDUT1 = '%01#WCSR01240'
    UnlockDUT2 = "%01#WCSR01440"
    UnlockDUT_all = '%01#WCSR012B0'
    DUT1Sensor = '%01#RCSX0304'
    DUT2Sensor = "%01#RCSX0305"
    DUT3Sensor = '%01#RCSX0306'
    DUT4Sensor = "%01#RCSX0307"

myBojayPLCCommandClass = BojayPLCCommandClass()


class GOEControlClass:
    # E71
    USBDisable = 0
    USBEnable = 1
    PowerEnable = 2
    PowerDisable = 3
    DUTLock = 4
    DUTUnlock = 5

    USB1 = 6
    USB2 = 7
    USB_all = 8
    Power1 = 9
    Power2 = 10
    Power_all = 11
    DUT1 = 12
    DUT2 = 13
    DUT_all = 14

    # E45
    X_axis = 100
    Y_axis = 200
    Z_axis = 300
    XY_axis = 400
    XYZ_axis = 401

    # DUT1 = 500
    # DUT2 = 501
    # DUT3 = 502
    # DUT4 = 503

    # Set_DM_5V_ON = 504
    # Set_DM_5V_OFF = 505
    # DUT_LOCK = 506
    # DUT_OPEN= 507

    Cylinder_IN = 508
    Cylinder_OUT = 509

    EStopOn = 510
    EStopOff = 511

    # Cylinder_UP = 512
    # Cylinder_DOWN = 513
    # Cylinder_LOCK = 514
    # Cylinder_OPEN = 515

    Alarm_On = 516
    Alarm_Off = 517
    # DUTALL = 518


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

    # USBLeft_ON = 5101
    # USBLeft_OFF = 5100
    # USBRight_ON = 5201
    # USBRight_OFF = 5200

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
    # Sensor_RightHolder_In = 6500
    # Sensor_RightHolder_Out = 6510

    Sensor_LeftDUT = 6600
    Sensor_RightDUT = 6700

    Sensor_Curtain = 6800

    Sensor_Calibrate = 6900 # %01#RCSX001F
    Sensor_TouchFinger = 7000 # %01#RCSX001E

    SerialPortOpen = False

    myTollerance = 0.0000001
    myWaitTime = 0.1
    strErrorMessage ="ok"

    #add new sensor
    CylinderINSensor = 7001
    CylinderOUTSensor = 7002
    # FingerprintWorkSensor = 7004
    # DUTLockSensor = 7005
    # USB1Sensor = 7006
    # USB2Sensor = 7007
    # USB3Sensor = 7008
    # USB4Sensor = 7009
    CheckDUT1Sensor = 7010
    CheckDUT2Sensor = 7011
    # CheckDUT3Sensor = 7012
    # CheckDUT4Sensor = 7013
    # OSS1CheckSensor = 7014
    # OSS2CheckSensor = 7015
    # OSS3CheckSensor = 7016
    # OSS4CheckSensor = 7017
    # USBALLSensor = 7018

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

    SensorOn = 1
    SensorOFF = 2
    # ********************************************************************************#

    # ********************************************************************************#
    # for E71
    def DUTSensorOnorOFF(self,state,ofWhatDUT):
        try:
            if ofWhatDUT == self.DUT2:
                if state == self.SensorOn:
                    command = "%01#WCSR00110"
                elif state == self.SensorOFF:
                    command = "%01#WCSR00111"
            elif ofWhatDUT == self.DUT1:
                if state == self.SensorOn:
                    command = "%01#WCSR00100"
                elif state == self.SensorOFF:
                    command = "%01#WCSR00101"
            err = self.__writeRead(command)
            if err != 0:
                return -1
            return 0
        except Exception as e:
            return -1


    def USBEableOrDisable(self,state,OfWhatUSB=8):
        try:
            if state == self.USBEnable:
                if OfWhatUSB == self.USB1:
                    command = myBojayPLCCommandClass.EnableUSB1 #'%01#WCSR01221'
                elif OfWhatUSB == self.USB2:
                    command = myBojayPLCCommandClass.EnableUSB2 #"01#WCSR01421"
                elif OfWhatUSB == self.USB_all:
                    command = myBojayPLCCommandClass.EnableUSB_all
                exceptValue = 1
            elif state == self.USBDisable:
                if OfWhatUSB == self.USB1:
                    command = myBojayPLCCommandClass.DisableUSB1 #'%01#WCSR01231'
                elif OfWhatUSB == self.USB2:
                    command = myBojayPLCCommandClass.DisableUSB2 #"01#WCSR01431"
                elif OfWhatUSB == self.USB_all:
                    command = myBojayPLCCommandClass.DisableUSB_all
                exceptValue = 0

            if OfWhatUSB == self.USB1:
                sensor = myBojayPLCCommandClass.USB1Sensor #"%01#RCSX0302"
            elif OfWhatUSB == self.USB2:
                sensor = myBojayPLCCommandClass.USB2Sensor #"%01#RCSX0303"

            ret = self.__writeRead(command)
            if ret != 0:
                return -1
            Timeout = 3
            mytimeout = 0
            while mytimeout < Timeout:
                if OfWhatUSB == self.USB_all:
                    ret1 = self.__readONorOFF(myBojayPLCCommandClass.USB1Sensor)
                    ret2 = self.__readONorOFF(myBojayPLCCommandClass.USB2Sensor)
                    if ret1 == exceptValue and ret2 == exceptValue:
                        return 0
                    elif ret1 == -1 or ret2 == -1:
                        self.strErrorMessage = "USBEableOrDisable read sensor error"
                        return -1
                    else:
                        time.sleep(0.1)
                        mytimeout = mytimeout + 0.1
                        continue
                elif OfWhatUSB != self.USB_all:
                    ret = self.__readONorOFF(sensor)
                    if ret == exceptValue:
                        return 0
                    elif ret == -1:
                        self.strErrorMessage = "USBEableOrDisable read sensor error"
                        return -1
                    else:
                        time.sleep(0.1)
                        mytimeout = mytimeout + 0.1
                        continue
            if mytimeout >= Timeout:
                self.strErrorMessage = "USBEableOrDisable timeout"
                return -1
            return 0
        except Exception as e:
            self.strErrorMessage = 'USBEableOrDisable except %s' % e
            return -1
    # ********************************************************************************#

    # ********************************************************************************#
    def DUTLockOrUnlock(self,state,OfWhatDUT=14):
        try:
            if state == self.DUTLock:
                if OfWhatDUT == self.DUT1:
                    command = myBojayPLCCommandClass.LockDUT1 #'%01#WCSR01241'
                elif OfWhatDUT == self.DUT2:
                    command = myBojayPLCCommandClass.LockDUT2 #"%01#WCSR01441"
                elif OfWhatDUT == self.DUT_all:
                    command = myBojayPLCCommandClass.LockDUT_all
                exceptValue = 1

            elif state == self.DUTUnlock:
                if OfWhatDUT == self.DUT1:
                    command = myBojayPLCCommandClass.UnlockDUT1 #'%01#WCSR01251'
                elif OfWhatDUT == self.DUT2:
                    command = myBojayPLCCommandClass.UnlockDUT2 #"%01#WCSR01451"
                elif OfWhatDUT == self.DUT_all:
                    command = myBojayPLCCommandClass.UnlockDUT_all
                exceptValue = 0

            if OfWhatDUT == self.DUT1:
                sensor1 = myBojayPLCCommandClass.DUT1Sensor #'%01#RCSX0308'
                sensor2 = myBojayPLCCommandClass.DUT3Sensor
            elif OfWhatDUT == self.DUT2:
                sensor1 = myBojayPLCCommandClass.DUT2Sensor #"%01#RCSX0309"
                sensor2 = myBojayPLCCommandClass.DUT4Sensor
                
            ret = self.__writeRead(command)
            if ret != 0:
                return -1
            Timeout = 3
            mytimeout = 0
            while mytimeout < Timeout:
                if OfWhatDUT == self.DUT_all:
                    ret1 = self.__readONorOFF(myBojayPLCCommandClass.DUT1Sensor)
                    ret2 = self.__readONorOFF(myBojayPLCCommandClass.DUT2Sensor)
                    ret3 = self.__readONorOFF(myBojayPLCCommandClass.DUT3Sensor)
                    ret4 = self.__readONorOFF(myBojayPLCCommandClass.DUT4Sensor)
                    if (ret1 == exceptValue and ret2 == exceptValue) and (ret3 == exceptValue and ret4 == exceptValue):
                        return 0
                    elif (ret1 == -1 or ret2 == -1) or (ret3 == -1 or ret4 == -1):
                        self.strErrorMessage = "DUTLockOrUnlock read sensor error"
                        return -1
                    else:
                        time.sleep(0.1)
                        mytimeout = mytimeout + 0.1
                        continue
                elif OfWhatDUT != self.DUT_all:
                    ret1 = self.__readONorOFF(sensor1)
                    ret2 = self.__readONorOFF(sensor2)
                    if ret1 == exceptValue and ret2 == exceptValue:
                        return 0
                    elif ret1 == -1 or ret2 == -1:
                        self.strErrorMessage = "DUTLockOrUnlock read sensor error"
                        return -1
                    else:
                        time.sleep(0.1)
                        mytimeout = mytimeout + 0.1
                        continue
            if mytimeout >= Timeout:
                self.strErrorMessage = "DUTLockOrUnlock timeout"
                return -1
            return 0
        except Exception as e:
            self.strErrorMessage = 'DUTLockOrUnlock except %s' % e
            return -1
    # ********************************************************************************#

    # ********************************************************************************#
    def PowerEnableOrDisable(self,state,OfWhatPower=11):
        try:
            if state == self.PowerEnable:
                if OfWhatPower == self.Power1:
                    command = myBojayPLCCommandClass.EnablePower1 #'%01#WCSR01201'
                elif OfWhatPower == self.Power2:
                    command = myBojayPLCCommandClass.EnablePower2 #'%01#WCSR01401'
                elif OfWhatPower == self.Power_all:
                    command = myBojayPLCCommandClass.EnablePower_all
                exceptValue = 1
            elif state == self.PowerDisable:
                if OfWhatPower == self.Power1:
                    command = myBojayPLCCommandClass.DisablePower1 #'%01#WCSR01211'
                elif OfWhatPower == self.Power2:
                    command = myBojayPLCCommandClass.DisablePower2 #'%01#WCSR01411'
                elif OfWhatPower == self.Power_all:
                    command = myBojayPLCCommandClass.DisablePower_all
                exceptValue = 0

            if OfWhatPower == self.Power1:
                sensor = myBojayPLCCommandClass.Power1Sensor #"%01#RCSX0300"
            elif OfWhatPower == self.Power2:
                sensor = myBojayPLCCommandClass.Power2Sensor #"%01#RCSX0301"

            ret = self.__writeRead(command)
            if ret != 0:
                return -1
            Timeout = 3
            mytimeout = 0
            while mytimeout < Timeout:
                if OfWhatPower == self.Power_all:
                    ret1 = self.__readONorOFF(myBojayPLCCommandClass.Power1Sensor)
                    ret2 = self.__readONorOFF(myBojayPLCCommandClass.Power2Sensor)
                    if ret1 == exceptValue and ret2 == exceptValue:
                        return 0
                    elif ret1 == -1 or ret2 == -1:
                        self.strErrorMessage = "PowerEnableOrDisable read sensor error"
                        return -1
                    else:
                        time.sleep(0.1)
                        mytimeout = mytimeout + 0.1
                        continue
                elif OfWhatPower != self.Power_all:
                    ret = self.__readONorOFF(sensor)
                    if ret == exceptValue:
                        return 0
                    elif ret == -1:
                        self.strErrorMessage = "PowerEnableOrDisable read sensor error"
                        return -1
                    else:
                        time.sleep(0.1)
                        mytimeout = mytimeout + 0.1
                        continue
            if mytimeout >= Timeout:
                self.strErrorMessage = "PowerEnableOrDisable timeout"
                return -1
            return 0
        except Exception as e:
            self.strErrorMessage = 'PowerEnableOrDisable except %s' % e
            return -1
    # ********************************************************************************#

    # ********************************************************************************#
    def SetLimit(self,ofWhatAxis,ofWhatLimit,value):
        try:
            # Set X-axis max / min limit
            if (ofWhatAxis == self.X_axis):
                if (ofWhatLimit == self.Max_limit):
                    command = myBojayPLCCommandClass.SetMaxLimit_xAxis #'%01#WDD0210002101'
                elif (ofWhatLimit == self.Min_limit):
                    command = myBojayPLCCommandClass.SetMinLimit_xAxis #'%01#WDD0210402105'
                else:
                    self.strErrorMessage = "SetPLCLimit input parameter is not correct"
                    return -1
            # Set Y-axis max / min limit
            elif (ofWhatAxis == self.Y_axis):
                if (ofWhatLimit == self.Max_limit):
                    command = myBojayPLCCommandClass.SetMaxLimit_yAxis #'%01#WDD0210802109'
                elif (ofWhatLimit == self.Min_limit):
                    command = myBojayPLCCommandClass.SetMinLimit_yAxis #'%01#WDD0211202113'
                else:
                    self.strErrorMessage = "SetPLCLimit input parameter is not correct"
                    return -1
            # Set Z-axis max / min limit
            elif (ofWhatAxis == self.Z_axis):
                if (ofWhatLimit == self.Max_limit):
                    command = myBojayPLCCommandClass.SetMaxLimit_zAxis #'%01#WDD0211602117'
                elif (ofWhatLimit == self.Min_limit):
                    command = myBojayPLCCommandClass.SetMinLimit_zAxis #'%01#WDD0212002121'
                else:
                    self.strErrorMessage = "SetPLCLimit input parameter is not correct"
                    return -1

            finalByte = self.__flipByte(value)
            command = command + finalByte
            ret = self.__writeRead(command)
            if ret != 0:
                self.strErrorMessage = 'SetLimit fail'
                return -1
            return 0
        except:
            self.strErrorMessage = "SetPLCLimit except"
            return -1
    # ********************************************************************************#

    # ********************************************************************************#
    def DrawCicleFlag(self,state):
        self.bDrawCircle = state
    # ********************************************************************************#

    # ********************************************************************************#
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
                # elif(i == 12):
                #     command = "%01#WCSR00780"#Set Cylinder2 Down
                #     strMessage = "Set Cylinder2 Down error"
                # elif(i == 13):
                #     command = "%01#WCSR01100"#DUT Lock
                #     strMessage = "DUT Lock error"
                # elif(i == 14):
                #     command = "%01#WCSR01120"#DUT USB 1
                #     strMessage = "DUT USB 1 error"
                # elif (i == 15):
                #     command = "%01#WCSR01140"#DUT USB 2
                #     strMessage = "DUT USB 2 error"
                # elif (i == 16):
                #     command = "%01#WCSR01160"#DUT USB 3
                #     strMessage = "DUT USB 3 error"
                # elif (i == 17):
                #     command = "%01#WCSR01180"#DUT USB 4
                #     strMessage = "DUT USB 4 error"
                elif (i == 18):
                    command = "%01#WCSR00850"#Set Red OFF DUT1
                    strMessage = "Set Red OFF DUT1 error"
                elif (i == 19):
                    command = "%01#WCSR00860"#Set Yellow OFF DUT1
                    strMessage = "Set Yellow OFF DUT1 error"
                elif (i == 20):
                    command = "%01#WCSR00870"#Set Green OFF DUT1
                    strMessage = "Set Green OFF DUT1 error"
                # elif (i == 21):
                #     command = "%01#WCSR008A0"#Set Red OFF DUT2
                #     strMessage = "Set Red OFF DUT2 error"
                # elif (i == 22):
                #     command = "%01#WCSR008B0"#Set Yellow OFF DUT2
                #     strMessage = "Set Yellow OFF DUT2 error"
                # elif (i == 23):
                #     command = "%01#WCSR008C0"#Set Green OFF DUT2
                #     strMessage = "Set Green OFF DUT2 error"
                # elif (i == 24):
                #     command = "%01#WCSR01200"#Set Red OFF DUT3
                #     strMessage = "Set Red OFF DUT3 error"
                # elif (i == 25):
                #     command = "%01#WCSR01210"#Set Yellow OFF DUT3
                #     strMessage = "Set Yellow OFF DUT3 error"
                # elif (i == 26):
                #     command = "%01#WCSR01220"#Set Green OFF DUT3
                #     strMessage = "Set Green OFF DUT3 error"
                # elif (i == 27):
                #     command = "%01#WCSR01230"#Set Red OFF DUT4
                #     strMessage = "Set Red OFF DUT4 error"
                # elif (i == 28):
                #     command = "%01#WCSR01240"#Set Yellow OFF DUT4
                #     strMessage = "Set Yellow OFF DUT4 error"
                # elif (i == 29):
                #     command = "%01#WCSR01250"#Set Green OFF DUT4
                #     strMessage = "Set Green OFF DUT4 error"
                elif (i == 30):
                    command = "%01#WCSR00990"#Set E-STOP OFF
                    strMessage = "Set E-STOP OFF error"
                # elif (i == 31):
                #     command = "%01#WCSR00800"#4 USB OPEN ALL
                #     strMessage = "4 USB OPEN ALL error"
                elif (i == 32):
                    command = "%01#WCSR00320"#4 USB OPEN ALL
                    strMessage = "Draw circle address error"


                bcc = self.__bccValue(command)
                command = command + bcc + '\r'
                command = command.upper()
                if Interpreter == '3':
                    command = command.encode('utf-8')
                self.ser.write(command)
                time.sleep(0.01)
                readString = self.ReadData(0.1)
                if (readString[3] != '$'):
                    return -1
            return 0
        except Exception as e:
            print(e)
            self.strErrorMessage =  "RestFunction fail"
            return -1
    # ********************************************************************************#

    # ********************************************************************************#
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
            self.strErrorMessage = 'DotFunction except'
            return -1
    # ********************************************************************************#

    # ********************************************************************************#
    #read data
    def ReadData(self,timeDelay):
        bReadData = False
        for i in range(0, 5, 1):
            time.sleep(timeDelay)
            readString = self.ser.readline()
            if(len(readString) > 1):
                if Interpreter == '3':
                    return readString.decode()
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
        if Interpreter == '3':
            return bcc.decode()
        return bcc

    # Write and Read Command
    def __writeRead(self, command):
        try:
            bcc = self.__bccValue(command)
            command = command + bcc + '\r'
            command = command.upper()
            if Interpreter == '3':
                command = command.encode('utf-8')
            self.ser.write(command)
            readString = self.ReadData(0.1)
            if (readString[3] == '$'):
                return 0
            else:
                return -1
        except Exception as e:
            return -1

    # flip Byte Function
    def __flipByte(self, code):
        code = float(code)
        code = int(code * 5000.0 / 5.0)
        X = binascii.hexlify(struct.pack('>i', code))

        byte1 = X[0:2]
        byte2 = X[2:4]
        byte3 = X[4:6]
        byte4 = X[6:8]
        finalbyte = byte4 + byte3 + byte2 + byte1
        finalbyte = finalbyte.upper()
        if Interpreter == '3':
            return finalbyte.decode()
        return finalbyte

    # __getValueOfByte function
    def __getValueOfByte(self,ByteString):
        try:
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
        except Exception as e:
            self.strErrorMessage  = '__getValueOfByte except %s' % e
            return -1

    #__readONorOFF function
    def __readONorOFF(self,command):
        bcc = self.__bccValue(command)
        command = command + bcc + '\r'
        command = command.upper()
        if Interpreter == '3':
            command = command.encode('utf-8')
        self.ser.write(command)
        readString = self.ReadData(0.1)#self.ser.readline()
        if("fail" in readString):
            return -1
        readState = readString[6]
        return int(readState)

    # __getCoordinatesFromFile function
    def __getCoordinatesFromFile(self,FilePath):
        FinalSplitLine = []
        with open(FilePath) as f:
            for line in f:
                splitline = line.rstrip().split('\r')
                FinalSplitLine = FinalSplitLine + splitline
            f.close()
            return FinalSplitLine

    # __readONorOFF function
    def __readVer(self, command):
        bcc = self.__bccValue(command)
        command = command + bcc + '\r'
        command = command.upper()
        self.ser.write(command.encode('utf-8'))
        readString = self.ReadData(0.1)  # self.ser.readline()
        if ("fail" in readString):
            return -1
        readState1 = readString[6:8]
        readState2 = readString[8:10]
        if Interpreter == '3':
            readState1 = readState1.decode()
            readState2 = readState2.decode()
        s1 = (binascii.a2b_hex(readState1))
        s2 = (binascii.a2b_hex(readState2))
        # ver = s1 + '.' + s2
        ver = 'Ver2.2'
        return ver

    def ReadVer(self):
        return self.__readVer(myBojayPLCCommandClass.ReadPLCVersion)

    # printHello function
    def printHello(self):
        print('Hello')
    # ********************************************************************************#

    # ********************************************************************************#
    #ChooseCOM function
    def ChooseCOM(self,serialName):
        try:
            self.ser = serial.Serial(port=serialName,
                                    timeout=0.01,
                                    baudrate=115200,
                                    parity=serial.PARITY_ODD)
            self.ser.close()
            self.ser.open()
            if(self.ser.is_open):
                command = '%01#RDD0015400155'
                bcc = self.__bccValue(command)
                command = command + bcc + '\r'
                command = command.upper()
                if Interpreter == '3':
                    command = command.encode('utf-8')
                self.ser.write(command)
                readStr = self.ReadData(0.1)
                if("fail" in readStr):
                    self.strErrorMessage = "ChooseCOM read command fail"
                    return -1
                else:
                    err = self.GetAllAxisLimit()
                    if(err == -1):
                        return -1
                    # err = self.RestAllFunction()
                    # if(err == -1):
                    #     return -1
                    return 0
            else:
                return 1
        except:
            self.strErrorMessage =  "ChooseCOM fail"
            return -1
    # ********************************************************************************#

    # ********************************************************************************#
    # Open Serial
    def OpenSerial(self):
        try:
            port_list = list(serial.tools.list_ports.comports())
            if(len(port_list) < 1):
                self.strErrorMessage = "fail:There is no serial port"
                return -1
            bFindSerialPort = False;
            for i in range(0, len(port_list)):
                err =  self.ChooseCOM(port_list[i].device)
                if(err == 0):
                    bFindSerialPort = True
                    return 0
                else:
                    self.ser.close()
                    continue
            if(bFindSerialPort == False):
                self.strErrorMessage = "There is no suitable port"
                return -1
        except:
            self.strErrorMessage =  "Open serial port fail"
            return -1
        return 0
    # ********************************************************************************#

    # ********************************************************************************#
    # Close Serial
    def CloseSerial(self):
        try:
            if(self.ser.is_open == True):
                self.ser.close()
            return 0
        except:
            self.strErrorMessage =   "CloseSerial fail"
            return -1
    # ********************************************************************************#

    # ********************************************************************************#
    # Read current X / Y / Z coordinates X:100 Y:
    def GetCurrentCoordinates(self,ofWhatAxis):
        if(self.ser.isOpen() == False):
            self.strErrorMessage = "the serial port is not opened"
            return -9999
        try:
            if (ofWhatAxis == self.X_axis):
                command = myBojayPLCCommandClass.GetCoordiante_xAxis #'%01#RDD0014600147'
            elif(ofWhatAxis == self.Y_axis):
                command = myBojayPLCCommandClass.GetCoordiante_yAxis #'%01#RDD0015000151'
            elif(ofWhatAxis == self.Z_axis):
                command = myBojayPLCCommandClass.GetCoordiante_zAxis #'%01#RDD0015400155'
            bcc = self.__bccValue(command)
            command = command + bcc + '\r'
            command = command.upper()
            if Interpreter == '3':
                command = command.encode('utf-8')
            self.ser.write(command)

            # read data
            bGetDataFromPLC = False
            readString =  self.ReadData(0.1)
            if ("fail" in readString):
                self.strErrorMessage = "GetCurrentCoordinates timeout"
                return -9999
            else:
                value = self.__getValueOfByte(readString)
                return round((value*10),2)
        except:
            self.strErrorMessage = "GetCurrentCoordinates error"
            return -9999
    # ********************************************************************************#

    # ********************************************************************************#
    # Moving to specified Coordinates per Axis
    def MoveToCoordinates(self,ofWhatAxis,Value,timeout=10):
        if(self.ser.isOpen() == False):
            self.strErrorMessage =  "The serial port is not opened"
            return -1
        # Move X-Axis
        if (ofWhatAxis == self.X_axis):
            if (Value < self.XAxisMinLimit):
                Value = self.XAxisMinLimit
            if(Value > self.XAxisMaxLimit):
                Value = self.XAxisMaxLimit

            command = myBojayPLCCommandClass.SetDistance_xAxis #'%01#WDD0020200203'
            finalByte = self.__flipByte(Value)
            command = command + finalByte
            ret = self.__writeRead(command)
            if (ret == 0):
                moveCommand = myBojayPLCCommandClass.XMove #'%01#WCSR002C1'
                ret = self.__writeRead(moveCommand)
                if(ret == 0):
                    mytimeCount = 0
                    while (self.GetmoveSignal(self.X_axis) == 1):
                        if (mytimeCount > timeout):
                            self.strErrorMessage = "MoveToCoordinates read command timeout"
                            return -1
                        time.sleep(0.005)
                        mytimeCount += 0.005

                    moveCommand = '%01#WCSR002C0'
                    ret = self.__writeRead(moveCommand)
                    print(self.GetmoveSignal(self.X_axis))
                    return 0
                else:
                    self.strErrorMessage = "MoveToCoordinates write command fail"
                    return -1
            else:
                self.strErrorMessage = "MoveToCoordinates write command fail"
                return -1

        # Move Y-Axis
        elif (ofWhatAxis == self.Y_axis):
            if (Value < self.YAxisMinLimit):
                Value = self.YAxisMinLimit
            if(Value > self.YAxisMaxLimit):
                Value = self.YAxisMaxLimit
            command = myBojayPLCCommandClass.SetDistance_yAxis #'%01#WDD0021200213'
            finalByte = self.__flipByte(Value)
            command = command + finalByte
            ret = self.__writeRead(command)
            if (ret == 0):
                moveCommand = myBojayPLCCommandClass.YMove #'%01#WCSR002D1'
                ret = self.__writeRead(moveCommand)
                if(ret == 0):
                    mytimeCount = 0
                    while (self.GetmoveSignal(self.Y_axis) == 1):
                        if (mytimeCount > timeout):
                            self.strErrorMessage = "MoveToCoordinates read command timeout"
                            return -1
                        time.sleep(0.005)
                        mytimeCount += 0.005

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
            if (Value < self.ZAxisMinLimit):
                Value = self.ZAxisMinLimit
            if(Value > self.ZAxisMaxLimit):
                Value = self.ZAxisMaxLimit
            command = myBojayPLCCommandClass.SetDistance_zAxis #'%01#WDD0022200223'
            finalByte = self.__flipByte(Value)
            command = command + finalByte
            ret = self.__writeRead(command)
            if (ret == 0):
                moveCommand = myBojayPLCCommandClass.ZMove #'%01#WCSR002E1'
                ret = self.__writeRead(moveCommand)
                if(ret == 0):
                    mytimeCount = 0
                    while (self.GetmoveSignal(self.Z_axis) == 1):
                        if (mytimeCount > timeout):
                            self.strErrorMessage = "MoveToCoordinates read command timeout"
                            return -1
                        time.sleep(0.005)
                        mytimeCount += 0.005

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
            self.strErrorMessage = "MoveToCoordinates input parameter error"
            return -1
    # ********************************************************************************#

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

            command = myBojayPLCCommandClass.SetDistance_xAxis #'%01#WDD0020200203'
            finalByte = self.__flipByte(xValue)
            command = command + finalByte
            ret = self.__writeRead(command)
            if(ret != 0):
                self.strErrorMessage =  "SynchronousXY %01#WDD0020200203 fail"
                return -1
            command = myBojayPLCCommandClass.SetDistance_yAxis #'%01#WDD0021200213'
            finalByte = self.__flipByte(yValue)
            command = command + finalByte
            ret = self.__writeRead(command)
            if(ret != 0):
                self.strErrorMessage = "SynchronousXY %01#WDD0021200213 fail"
                return -1

            if(self.bDrawCircle == True):
                command = '%01#WCSR00321'
            else:
                command = myBojayPLCCommandClass.XYMove #'%01#WCSR002F1'
            # bcc = self.__bccValue(command)
            # command = command + bcc + '\r'
            # command = command.upper()
            # command = command.encode('utf-8')
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
        except Exception as e:
            self.strErrorMessage = "SynchronousXY fail %s" % e
            return -1
    # ********************************************************************************#

    # ********************************************************************************#
    # Set Increment / Decrement Value
    def SetStepValue(self,ofWhatAxis,Value):
        if(self.ser.isOpen() == False):
            self.strErrorMessage = "the serial port is not opened"
            return -1
        try:
            if (ofWhatAxis == self.X_axis):
                command = myBojayPLCCommandClass.SetStep_xAxis #'%01#WDD0100001001'
            elif(ofWhatAxis == self.Y_axis):
                command = myBojayPLCCommandClass.SetStep_yAxis #'%01#WDD0100801009'
            elif(ofWhatAxis == self.Z_axis):
                command = myBojayPLCCommandClass.SetStep_zAxis #'%01#WDD0101601017'
            finalByte = self.__flipByte(Value)
            command = command + finalByte
            ret = self.__writeRead(command)
            if(ret == -1):
                self.strErrorMessage = "SetStepValue write command fail"
                return -1
            return ret
        except Exception as e:
            self.strErrorMessage = "SetStepValue except %s" % e
            return -1
    # ********************************************************************************#

    # ********************************************************************************#
    def GetStepValue(self, ofWhatAxis):
        try:
            if (ofWhatAxis == self.X_axis):
                command = myBojayPLCCommandClass.GetStep_xAxis #"%01#RDD006000060054"
            elif(ofWhatAxis == self.Y_axis):
                command = myBojayPLCCommandClass.GetStep_yAxis #"%01#RDD006020060254"
            elif(ofWhatAxis == self.Z_axis):
                command = myBojayPLCCommandClass.GetStep_zAxis #"%01#RDD006040060454"
            bcc = self.__bccValue(command)
            command = command + bcc + '\r'
            command = command.upper()
            if Interpreter == '3':
                command = command.encode('utf-8')
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

    # ********************************************************************************#
    # Move Increment
    def MoveIncrement(self,ofWhatAxis):
        if(self.ser.isOpen() == False):
            self.strErrorMessage =  "The serial port is not open"
            return -1
        try:
            if (ofWhatAxis == self.X_axis):
                command = myBojayPLCCommandClass.MoveStep_xAxis #'%01#WCSR00201'
            elif(ofWhatAxis == self.Y_axis):
                command = myBojayPLCCommandClass.MoveStep_yAxis #'%01#WCSR00241'
            elif(ofWhatAxis == self.Z_axis):
                command = myBojayPLCCommandClass.MoveStep_zAxis #'%01#WCSR00281'
            ret = self.__writeRead(command)
            if(ret == -1):
                self.strErrorMessage = "MoveIncrement write command error"
                return -1
            timeout = 10
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
                        self.strErrorMessage = "MoveIncrement time out"
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
                        self.strErrorMessage = "MoveIncrement time out"
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
        except Exception as e:
            self.strErrorMessage = "MoveIncrement except %s" % e
            return -1
    # ********************************************************************************#

    # ********************************************************************************#
    # Move decrement
    def MoveDecrement(self,ofWhatAxis):
        if(self.ser.isOpen() == False):
            self.strErrorMessage = "the serial port is not open"
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
                self.strErrorMessage = "MoveDecrement write command error"
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
        except Exception as e:
            self.strErrorMessage = "MoveDecrement except %s" % e
            return -1
    # ********************************************************************************#

    # ********************************************************************************#
    # Set Motor Move Speed
    def SetSpeed(self,ofWhatAxis,Value):
        if(self.ser.isOpen() == False):
            self.strErrorMessage = "The serial port is not open"
            return -1
        try:
            if (ofWhatAxis == self.X_axis):
                command = myBojayPLCCommandClass.SetSpeed_xAxis #'%01#WDD0020000201'
            elif(ofWhatAxis == self.Y_axis):
                command = myBojayPLCCommandClass.SetSpeed_yAxis #'%01#WDD0021000211'
            elif(ofWhatAxis == self.Z_axis):
                command = myBojayPLCCommandClass.SetSpeed_zAxis #'%01#WDD0022000221'
            finalByte = self.__flipByte(Value)
            command = command + finalByte
            ret = self.__writeRead(command)
            if(ret == -1):
                self.strErrorMessage = "SetSpeed read command fail"
                return -1
            return 0
        except Exception as e:
            self.strErrorMessage = "SetSpeed except %s" % e
            return -1
    # ********************************************************************************#

    # ********************************************************************************#
    # Get current motor move speed
    def GetSpeed(self,ofWhatAxis):
        if(self.ser.isOpen() == False):
            self.strErrorMessage = "The serial port is not open"
            return -1
        try:
            if (ofWhatAxis == self.X_axis):
                command = myBojayPLCCommandClass.GetSpeed_xAxis #'%01#RDD0020000201'
            elif(ofWhatAxis == self.Y_axis):
                command = myBojayPLCCommandClass.GetSpeed_yAxis #'%01#RDD0021000211'
            elif(ofWhatAxis == self.Z_axis):
                command = myBojayPLCCommandClass.GetSpeed_zAxis #'%01#RDD0022000221'
            bcc = self.__bccValue(command)
            command = command + bcc + '\r'
            command = command.upper()
            if Interpreter == '3':
                command = command.encode('utf-8')
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
    # ********************************************************************************************#

    # ********************************************************************************************#
    # Get Limit of X / Y / Z axis
    def GetLimit(self,ofWhatAxis,ofWhatLimit):
        if(self.ser.isOpen() == False):
            self.strErrorMessage = "the serial port is not open"
            return -9999
        try:
            # Get X-axis max / min limit
            if (ofWhatAxis == self.X_axis):
                if (ofWhatLimit == self.Max_limit):
                    command = myBojayPLCCommandClass.GetMaxLimit_xAxis #'%01#RDD0062000621'
                elif (ofWhatLimit == self.Min_limit):
                    command = myBojayPLCCommandClass.GetMinLimit_xAxis #'%01#RDD0063000631'
                else:
                    self.strErrorMessage = "GetLimit input parameter is not correct"
                    return -9999
            # Get Y-axis max / min limit
            elif (ofWhatAxis == self.Y_axis):
                if (ofWhatLimit == self.Max_limit):
                    command = myBojayPLCCommandClass.GetMaxLimit_yAxis #'%01#RDD0062200623'
                elif (ofWhatLimit == self.Min_limit):
                    command = myBojayPLCCommandClass.GetMinLimit_yAxis #'%01#RDD0063200633'
                else:
                    self.strErrorMessage = "GetLimit input parameter is not correct"
                    return -9999
            elif (ofWhatAxis == self.Z_axis):
                if (ofWhatLimit == self.Max_limit):
                    command = myBojayPLCCommandClass.GetMaxLimit_zAxis #'%01#RDD0062400625'
                elif (ofWhatLimit == self.Min_limit):
                    command = myBojayPLCCommandClass.GetMinLimit_zAxis #'%01#RDD0063400635'
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
            if Interpreter == '3':
                command = command.encode('utf-8')
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
    # ********************************************************************************************#

    # ********************************************************************************************#
    # Set Left / Right LED Color
    def SetLedLightColor(self,ofWhichLED,ofWhatColor):
        try:
            if(self.ser.isOpen() == False):
                self.strErrorMessage = "The serial port is not open"
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
            elif (ofWhichLED == self.DUT2):
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
            # # Set DUT3 Color
            # if (ofWhichLED == self.DUT3):
            #     # LEFT LED RED Color
            #     if (ofWhatColor == self.Red_OFF):
            #         command = '%01#WCSR01200'
            #     elif (ofWhatColor == self.Red_ON):
            #         command = '%01#WCSR01201'
            #     # LEFT LED Yellow Color
            #     elif (ofWhatColor == self.Yellow_OFF):
            #         command = '%01#WCSR01210'
            #     elif (ofWhatColor == self.Yellow_ON):
            #         command = '%01#WCSR01211'
            #     # LEFT LED Green Color
            #     elif (ofWhatColor == self.Green_OFF):
            #         command = '%01#WCSR01220'
            #     elif (ofWhatColor == self.Green_ON):
            #         command = '%01#WCSR01221'
            #     else:
            #         self.strErrorMessage = "Input parameter error"
            #         return -1  # Color Parameter Error
            #
            # # Set DUT4 Color
            # if (ofWhichLED == self.DUT4):
            #     # LEFT LED RED Color
            #     if (ofWhatColor == self.Red_OFF):
            #         command = '%01#WCSR01230'
            #     elif (ofWhatColor == self.Red_ON):
            #         command = '%01#WCSR01231'
            #     # LEFT LED Yellow Color
            #     elif (ofWhatColor == self.Yellow_OFF):
            #         command = '%01#WCSR01240'
            #     elif (ofWhatColor == self.Yellow_ON):
            #         command = '%01#WCSR01241'
            #     # LEFT LED Green Color
            #     elif (ofWhatColor == self.Green_OFF):
            #         command = '%01#WCSR01250'
            #     elif (ofWhatColor == self.Green_ON):
            #         command = '%01#WCSR01251'
            #     else:
            #         self.strErrorMessage = "Input parameter error"
            #         return -1  # Color Parameter Error

            ret = self.__writeRead(command)
            if(ret != 0):
                self.strErrorMessage = "SetLedLightColor write command fail"
                return -1
            return 0
        except Exception as e:
            self.strErrorMessage = "SetLedLightColor except %s" % e
            return -1  # Color Parameter Error
    # ********************************************************************************************#

    # ********************************************************************************************#
    # Read Sensors
    def GetSensorStatus(self,ofWhatSensor):
        if(self.ser.isOpen() == False):
            self.strErrorMessage =  "The serial port is not open"
            return -1
        # X-axis Sensor
        if (ofWhatSensor == self.Sensor_X_Origin):
            command = myBojayPLCCommandClass.XAisHomeSensor #'%01#RCSX0018'
        elif (ofWhatSensor == self.Sensor_X_Max):
            command = myBojayPLCCommandClass.XAxisHLSensor #'%01#RCSX001A'
        elif (ofWhatSensor == self.Sensor_X_Min):
            command = myBojayPLCCommandClass.XAxisLLSensor #'%01#RCSX0019'
        # Y-axis Sensor
        elif (ofWhatSensor == self.Sensor_Y_Origin):
            command = myBojayPLCCommandClass.YAisHomeSensor #'%01#RCSX0015'
        elif (ofWhatSensor == self.Sensor_Y_Max):
            command = myBojayPLCCommandClass.YAxisHLSensor #'%01#RCSX0017'
        elif (ofWhatSensor == self.Sensor_Y_Min):
            command = myBojayPLCCommandClass.YAxisLLSensor #'%01#RCSX0016'
        # Z-axis Sensor
        elif (ofWhatSensor == self.Sensor_Z_Origin):
            command = myBojayPLCCommandClass.ZAisHomeSensor #'%01#RCSX001B'
        elif (ofWhatSensor == self.Sensor_Z_Max):
            command = myBojayPLCCommandClass.ZAxisHLSensor #'%01#RCSX001D'
        elif (ofWhatSensor == self.Sensor_Z_Min):
            command = myBojayPLCCommandClass.ZAxisLLSensor #'%01#RCSX001C'
        # Other
        elif (ofWhatSensor == self.CylinderINSensor):
            command = myBojayPLCCommandClass.CylinderInSensor #'%01#RCSX0011'
        elif (ofWhatSensor == self.CylinderOUTSensor):
            command = myBojayPLCCommandClass.CylinderOutSensor #'%01#RCSX0012'
        elif (ofWhatSensor == self.Sensor_Curtain):
            command = myBojayPLCCommandClass.CurtainSensor #'%01#RCSX0010'
        elif (ofWhatSensor == self.Sensor_Calibrate):
            command = myBojayPLCCommandClass.CalibrationSensor #'%01#RCSX001F'
        elif (ofWhatSensor == self.CheckDUT1Sensor):
            command = '%01#RCSX000F'
        elif (ofWhatSensor == self.CheckDUT2Sensor):
            command = '%01#RCSX000E'
        elif (ofWhatSensor == self.Sensor_TouchFinger):
            command = '%01#RCSX001E'
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
    def SignalReset(self,timeout=15):
        try:
            mytimeCount = 0
            command = myBojayPLCCommandClass.ResetCommand_ON #'%01#WCSR00841'
            bcc = self.__bccValue(command)
            command = command + bcc + '\r'
            ret = self.__writeRead(command)
            if(ret == 0):
                # wait for x-axis is ready
                time.sleep(self.myWaitTime)
                mytimeCount = 0
                while (self.GetHomeFinishState(self.XYZ_axis) == 1):
                    if(mytimeCount > timeout):
                        break
                    time.sleep(0.5)
                    mytimeCount += self.myWaitTime
                command = myBojayPLCCommandClass.ResetCommand_OFF  # '%01#WCSR00840'
                bcc = self.__bccValue(command)
                command = command + bcc + '\r'
                ret = self.__writeRead(command)
                if (ret == -1):
                    self.strErrorMessage = "SignalReset read error"
                    return -1
                if(mytimeCount > timeout):
                    self.strErrorMessage = "SignalReset Reset time out"
                    return -1
                return 0
            else:
                self.strErrorMessage = "SignalReset write command fail"
                return -1
        except Exception as e:
            self.strErrorMessage = "SignalReset except %s" % e
            return -1
    # ********************************************************************************************#

    # ********************************************************************************************#
    def GetHomeFinishState(self,ofWhatAxis):
        if(self.ser.isOpen() == False):
            self.strErrorMessage =  "The serial port is not opened"
            return  -1
        try:
            if (ofWhatAxis == self.XYZ_axis):
                command = myBojayPLCCommandClass.SingleHomeFinish_xyzAxis #'%01#RCSR0104'
            elif(ofWhatAxis == self.X_axis):
                command = myBojayPLCCommandClass.SingleHomeFinish_xAxis #'%01#RCSR0100'
            elif(ofWhatAxis == self.Y_axis):
                command = myBojayPLCCommandClass.SingleHomeFinish_yAxis #'%01#RCSR0101'
            elif(ofWhatAxis == self.Z_axis):
                command = myBojayPLCCommandClass.SingleHomeFinish_zAxis #'%01#RCSR0102'

            bcc = self.__bccValue(command)
            command = command + bcc + '\r'
            command = command.upper()
            if Interpreter == '3':
                command = command.encode('utf-8')
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

    # ********************************************************************************************#
    def GetmoveSignal(self,ofWhatAxis):
        if(self.ser.isOpen() == False):
            self.strErrorMessage =  "The serial port is not opened"
            return  -1
        try:
            if (ofWhatAxis == self.XY_axis):
                command = myBojayPLCCommandClass.SingleMoveFinish_xyAxis #'%01#RCSR005C'
            elif(ofWhatAxis == self.X_axis):
                command = myBojayPLCCommandClass.SingleMoveFinish_xAxis #'%01#RCSR0052'
            elif(ofWhatAxis == self.Y_axis):
                command = myBojayPLCCommandClass.SingleMoveFinish_yAxis #'%01#RCSR0054'
            elif(ofWhatAxis == self.Z_axis):
                command = myBojayPLCCommandClass.SingleMoveFinish_zAxis #'%01#RCSR0056'
            bcc = self.__bccValue(command)
            command = command + bcc + '\r'
            command = command.upper()
            if Interpreter == '3':
                command = command.encode('utf-8')
            self.ser.write(command)
            readString =  self.ReadData(0.1)
            if("fail" in readString):
                self.strErrorMessage = "GetmoveSignal read time out"
                return -1
            readString = int(readString[6])
            if (readString == 1):
                return 0
            elif (readString == 0):
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

            listPoint = []
            strPoint = ""
            exeFolderPath = os.getcwd()
            exeFolderPath += "\\motion.txt"
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
            return 0

        except:
            self.strErrorMessage = "CreateCircle except"
            return -1
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
            strPoint = ""
            exeFolderPath = os.getcwd()
            exeFolderPath += "\\motion.txt"
            output = open(exeFolderPath,'w')
            listPoint = []
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
            self.strErrorMessage = "Create pattern except"
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
            exeFolderPath = os.getcwd()
            exeFolderPath += "\\motion.txt"
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
                time.sleep(0.2)
            return 0
        except:
            self.strErrorMessage = "RunPattern error"
            return -1
    # ********************************************************************************#

    # ********************************************************************************#
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
                    # back
                    if("increment" in incrementOrDecrement):
                        err = self.SetStepValue(ofWhichAxis, -3*StepValue)
                        if (err == -1):
                            return -1
                        ret = self.MoveIncrement(ofWhichAxis)
                        if(ret == -1):
                            return -1
                    elif("decrement" in incrementOrDecrement):
                        err = self.SetStepValue(ofWhichAxis, -3*StepValue)
                        if (err == -1):
                            return -1
                        ret = self.MoveDecrement(ofWhichAxis)
                        if(ret == -1):
                            return -1

                    LoopCounter = LoopCounter + 1
                    if (LoopCounter == 1):
                        StepValue = 0.1
                    elif (LoopCounter == 2):
                        StepValue = 0.02
                    elif (LoopCounter == 3):
                        CalPosition = self.GetCurrentCoordinates(ofWhichAxis)
                        if(CalPosition == -9999):
                            return -1
                        else:
                            # back
                            if ("increment" in incrementOrDecrement):
                                err = self.SetStepValue(ofWhichAxis, -3 * StepValue)
                                if (err == -1):
                                    return -1
                                ret = self.MoveIncrement(ofWhichAxis)
                                if (ret == -1):
                                    return -1
                            elif ("decrement" in incrementOrDecrement):
                                err = self.SetStepValue(ofWhichAxis, -3 * StepValue)
                                if (err == -1):
                                    return -1
                                ret = self.MoveDecrement(ofWhichAxis)
                                if (ret == -1):
                                    return -1
                            return round(float(CalPosition),2)
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
    # ********************************************************************************#

    # ********************************************************************************#
    def CalibrationPosition(self,offset):
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
            exeFolderPath += "\\CalibrationInitial.txt"
            calibraionFile = open(exeFolderPath)
            alllines = calibraionFile.readlines()
            for line in alllines:
                strLine = line.strip()
                if ("ZIncrementX=" in strLine):
                    zAxisCalX = float(strLine[strLine.find("=") + 1:])
                elif ("ZIncrementY=" in strLine):
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
                    print("Z axis calibration error")
                    return -1
                else:
                    print("Z axis calibration value=" + str(Zvsl_Finsl))

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
            Zvalue_temp = Zvalue_temp + 5.0
            err = self.MoveToCoordinates(self.Z_axis, Zvalue_temp, 10)
            if (err == -1):
                return -1
            else:
                Xval_1 = self.Calibrate(self.X_axis, 'increment')
                if (Xval_1 == -1):
                    print("X_axis increment fail")
                    return -1
                else:
                    print("X axis calibration value=" + str(Xval_1))


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
                    print("X_axis increment fail")
                    return -1
                else:
                    print("X axis calibration value=" + str(Xval_2))
            Xval_Final = (Xval_1 + Xval_2) / 2
            print("X calibrate result:" + str(Xval_Final))

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
                    print("Y_axis increment fail")
                    return -1
                else:
                    print("Y axis calibration value=" + str(Yval_1))

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
                    print("Y_axis increment fail")
                    return -1
                else:
                    print("Y axis calibration value=" + str(Yval_2))
            Yval_Final = (Yval_1 + Yval_2) / 2
            print("Y calibrate result:" + str(Yval_Final))


            #Save calibrtion file
            Zvsl_Finsl = Zvsl_Finsl + offset
            exeFolderPath = os.getcwd()
            exeFolderPath += "\\calibration.txt"
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
            return 0
        except:
            self.strErrorMessage = "CalibrationPosition error"
            return -1
    # ********************************************************************************************#

    # ********************************************************************************************#
    def Set_CylindeFunction(self,action):
        if(self.ser.isOpen() == False):
            self.strErrorMessage =  "The serial port is not opened"
            return  -1
        try:
            if (action == self.Cylinder_IN):
                command = "%01#WCSR00771"
            elif (action == self.Cylinder_OUT):
                command = "%01#WCSR00791"

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
            if (action == self.Cylinder_IN or action == self.Cylinder_OUT):
                if (action == self.Cylinder_IN):
                    command = "%01#WCSR00770"
                elif (action == self.Cylinder_OUT):
                    command = "%01#WCSR00790"
                ret = self.__writeRead(command)
                if (ret != 0):
                    self.strErrorMessage = "Set_CylindeFunction Read command fail"
                    return -1
            if(myTimeCount >= timeOut):
                self.strErrorMessage = "Set_CylindeFunction time out"
                return -1
            return 0
        except:
            self.strErrorMessage = "Set_CylindeFunction error"
            return -1
    # ********************************************************************************************#

    # ********************************************************************************************#
    def AlarmBuzzer(self,state):
        if (self.ser.isOpen() == False):
            self.strErrorMessage = "The serial port is not opened"
            return -1
        try:
            if(state == self.Alarm_On):
                command = "%01#WCSR01300"
            elif(state == self.Alarm_Off):
                command = "%01#WCSR01301"
            ret = self.__writeRead(command)
            if (ret != 0):
                self.strErrorMessage = "AlarmBuzzer Red command fail"
                return -1
            return 0
        except Exception as e:
            self.strErrorMessage = "AlarmBuzzer except %s" % e
            return -1
    # ********************************************************************************************#

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
            if Interpreter == '3':
                command = command.encode('utf-8')
            self.ser.write(command)
            readString = self.ReadData(0.1)
            #?????
        except:
            self.strErrorMessage = "ReadAxisAlarm error"
            return -1
    # ********************************************************************************************#

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
            if Interpreter == '3':
                command = command.encode('utf-8')
            self.ser.write(command)
            readString = self.ReadData(0.1)
        except:
            self.strErrorMessage = "SetEStop except"
            return -1
    # ********************************************************************************************#

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
            self.strErrorMessage = "ResetTray except"
            return -1
    # ********************************************************************************************#

    # ********************************************************************************************#
    def BojayFFTStart(self):
        try:


            #2:the first time need to reset
            if(self.bFirstRunFunction == True):
                err = self.SignalReset(10)
                if(err == -1):
                    return -1

            #2:Z axis move to safety position
            ZaxisSafetyPosition = 0
            err = self.MoveToCoordinates(self.Z_axis,ZaxisSafetyPosition,10)
            if(err == -1):
                return -1

            # #3:Lock DUT
            # err = self.Set_CylindeFunction(self.Cylinder_LOCK)
            # if(err == -1):
            #     return -1

            #:you'd better to add check curtain command
            err = self.GetSensorStatus(self.Sensor_Curtain)
            if(err == 0):
                self.strErrorMessage = "Curtain is triggered"
                return -1

            #4:Tray in
            err = self.Set_CylindeFunction(self.Cylinder_IN)
            if(err == -1):
                err = self.ResetTray(self.Cylinder_IN)
                if(err == -1):
                    return -1
                return -1

            # #5:Finger up
            # err = self.Set_CylindeFunction(self.Cylinder_UP)
            # if(err == -1):
            #     return -1

            #6:Set speed
            if(self.bFirstRunFunction == True):
                err = self.SetSpeed(self.X_axis, 40)
                if (err == -1):
                    return -1
                err = self.SetSpeed(self.Y_axis, 40)
                if (err == -1):
                    return -1
                err = self.SetSpeed(self.Z_axis, 40)
                if (err == -1):
                    return -1

            # 7:Move this positon to check OSS
            ZAxisChcekOSSPosition = 15
            err = self.MoveToCoordinates(self.Z_axis, ZAxisChcekOSSPosition, 10)
            if (err == -1):
                return -1


            # if (DUT1 == True):
            #     ret = self.GetSensorStatus(self.OSS1CheckSensor)
            #     if (ret == 0):
            #         self.strErrorMessage = "Solt 1 DUT put error"
            #         return -1
            # if (DUT2 == True):
            #     ret = self.GetSensorStatus(self.OSS2CheckSensor)
            #     if (ret == 0):
            #         self.strErrorMessage = "Solt 2 DUT put error"
            #         return -1
            # if (DUT3 == True):
            #     ret = self.GetSensorStatus(self.OSS3CheckSensor)
            #     if (ret == 0):
            #         self.strErrorMessage = "Solt 3 DUT put error"
            #         return -1
            # if (DUT4 == True):
            #     ret = self.GetSensorStatus(self.OSS4CheckSensor)
            #     if (ret == 0):
            #         self.strErrorMessage = "Solt 4 DUT put error"
            #         return -1

            #6:Cheeck DUT
            # if(DUT1 == True):
                #Put DUT or not


            ret = self.GetSensorStatus(self.CheckDUT1Sensor)
            if(ret != 1):
                self.strErrorMessage = "No DUT in solt 1"
                return -1

                # if(DUTALL ==False):
                #     ret = self.DUTLcokOrOpen(self.DUT1,self.DUT_LOCK)
                #     if(ret != 0):
                #         self.strErrorMessage = "Lock DUT1 fail"
                #         return -1
            # if (DUT2 == True):
            #     #Put DUT or not
            #     ret = self.GetSensorStatus(self.CheckDUT2Sensor)
            #     if(ret != 1):
            #         self.strErrorMessage = "No DUT in solt 2"
            #         return -1
            #     if (DUTALL == False):
            #         ret = self.DUTLcokOrOpen(self.DUT2,self.DUT_LOCK)
            #         if(ret != 0):
            #             self.strErrorMessage = "Lock DUT2 fail"
            #             return -1
            # if (DUT3 == True):
            #     #Put DUT or not
            #     ret = self.GetSensorStatus(self.CheckDUT3Sensor)
            #     if(ret != 1):
            #         self.strErrorMessage = "No DUT in solt 3"
            #         return -1
            #     if (DUTALL == False):
            #         ret = self.DUTLcokOrOpen(self.DUT3,self.DUT_LOCK)
            #         if(ret != 0):
            #             self.strErrorMessage = "Lock DUT3 fail"
            #             return -1
            # if (DUT4 == True):
            #     #Put DUT or not
            #     ret = self.GetSensorStatus(self.CheckDUT4Sensor)
            #     if(ret != 1):
            #         self.strErrorMessage = "No DUT in solt 4"
            #         return -1
            #     if (DUTALL == False):
            #         ret = self.DUTLcokOrOpen(self.DUT4,self.DUT_LOCK)
            #         if(ret != 0):
            #             self.strErrorMessage = "Lock DUT4 fail"
            #             return -1

            # if(DUTALL ==True):
            #     ret = self.DUTLcokOrOpen(self.DUTALL, self.DUT_LOCK)
            #     if (ret != 0):
            #         self.strErrorMessage = "Lock DUT4 fail"
            #         return -1


            # #8:Move to calibraton position
            # if(self.bFirstRunFunction == True):
            #     exeFolderPath = os.getcwd()
            #     exeFolderPath += "\\calibration.txt"
            #     calibraionFile = open(exeFolderPath)
            #     alllines = calibraionFile.readlines()
            #     for line in alllines:
            #         strLine = line.strip()
            #         if("X-Finial=" in strLine):
            #             self.XAxisCalibration = float(strLine[strLine.find("=")+1:])
            #         elif("Y-Finial=" in strLine):
            #             self.YAxisCalibration = float(strLine[strLine.find("=")+1:])
            #         elif("Z-Finial=" in strLine):
            #             self.ZAxisCalibration = float(strLine[strLine.find("=")+1:])
            #     self.bFirstRunFunction = False
            # err = self.MoveToCoordinates(self.Z_axis,self.ZAxisCalibration,10)
            # if(err == -1):
            #     return -1
            # err = self.SynchronousXY(self.XAxisCalibration,self.YAxisCalibration,5)
            # if(err == -1):
            #     return -1

            #9:Run Patten
            err = self.RunPattern()
            if(err == -1):
                return -1

            #10 end of test
            err = self.MoveToCoordinates(self.Z_axis,0,10)
            if(err == -1):
                return -1
            err = self.MoveToCoordinates(self.X_axis,0,10)
            if(err == -1):
                return -1
            err = self.MoveToCoordinates(self.Y_axis,0,10)
            if(err == -1):
                return -1
            return 0
        except:
            self.strErrorMessage = "BojayFFTStart except"
            return -1
    # ********************************************************************************************#

    # ********************************************************************************************#
    def BojayFFTEnd(self):
        try:
            # #1:Fingerprint down
            # err = self.Set_CylindeFunction(self.Cylinder_DOWN)
            # if(err == -1):
            #     return -1
            #2:Z axis move to safety position
            ZaxisSafetyPosition = 0
            err = self.MoveToCoordinates(self.Z_axis,ZaxisSafetyPosition,5)
            if(err == -1):
                return -1

            #3:Open USB
            # if(DUTALL == True):
            #     ret = self.DUTLcokOrOpen(self.DUTALL, self.DUT_OPEN)
            #     if (ret != 0):
            #         return -1
            # else:
            #     if(DUT1 == True):
            #         ret = self.DUTLcokOrOpen(self.DUT1,self.DUT_OPEN)
            #         if(ret != 0):
            #             return -1
            #     if(DUT2 == True):
            #         ret = self.DUTLcokOrOpen(self.DUT2,self.DUT_OPEN)
            #         if(ret != 0):
            #             return -1
            #     if(DUT3 == True):
            #         ret = self.DUTLcokOrOpen(self.DUT3,self.DUT_OPEN)
            #         if(ret != 0):
            #             return -1
            #     if(DUT4 == True):
            #         ret = self.DUTLcokOrOpen(self.DUT4,self.DUT_OPEN)
            #         if(ret != 0):
            #             return -1

            #4:Cylinder out
            err = self.Set_CylindeFunction(self.Cylinder_OUT)
            if(err == -1):
                err = self.ResetTray(self.Cylinder_OUT)
                if(err == -1):
                    return -1
                return -1

            # # 5:Open lock
            # err = self.Set_CylindeFunction(self.Cylinder_OPEN)
            # if (err == -1):
            #     return -1
            return 0
        except:
            self.strErrorMessage = "BojayFFTEnd error"
            return -1
    # ********************************************************************************************#

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
            return 0
        except:
            return -1


if __name__ == '__main__':
    cls = GOEControlClass()
    cls.OpenSerial()
    cls.DUTSensorOnorOFF(cls.SensorOFF,cls.DUT1)
    cls.DUTSensorOnorOFF(cls.SensorOFF, cls.DUT2)
    # cls.DUTSensorOnorOFF(cls.SensorOn,cls.DUT1)
    # cls.DUTSensorOnorOFF(cls.SensorOn, cls.DUT2)
    # cls.AlarmBuzzer(cls.Alarm_On)
    # cls.AlarmBuzzer(cls.Alarm_Off)






























