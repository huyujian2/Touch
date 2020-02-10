#-*-coding:utf-8-*-
from PySide2 import QtCore,QtGui,QtWidgets
from PySide2.QtCore import QTimer
from PySide2.QtWidgets import QDialog,QMessageBox
from GOEPLCControl import *
from UI import *


myBojayClass = GOEControlClass()


class TonyFrame(QDialog):

    # **************************************************************#
    #initial function
    def __init__(self,parent=None):
        try:
            super(TonyFrame,self).__init__(parent)
            self.ui = Ui_Form()
            self.ui.setupUi(self)
            self.setFixedSize(self.width(), self.height())

            self.ui.pushButtonSensorOFF.clicked.connect(lambda :self.DUTSensor('off'))
            self.ui.pushButtonSensorON.clicked.connect(lambda: self.DUTSensor('on'))

            self.ui.pushButtonOpenPort.clicked.connect(lambda :self.OpenPort())
            self.ui.pushButtonClosePort.clicked.connect(lambda :self.ClosePort())
            self.ui.pushButtonSignalReSet.clicked.connect(lambda :self.ActionReset())
            self.ui.pushButtonSpeedSet.clicked.connect(lambda :self.PLCSpeed('set'))
            self.ui.pushButtonSpeedGet.clicked.connect(lambda :self.PLCSpeed('get'))

            self.ui.pushButtonLimitSet.clicked.connect(lambda :self.PLCLimit('set'))
            self.ui.pushButtonPassword.clicked.connect(lambda :self.PassWord())
            self.ui.pushButtonLimitGet.clicked.connect(lambda :self.PLCLimit('get'))

            self.ui.pushButtonMovex.clicked.connect(lambda :self.AbsoluteMove('x'))
            self.ui.pushButtonMovey.clicked.connect(lambda :self.AbsoluteMove('y'))
            self.ui.pushButtonMovez.clicked.connect(lambda :self.AbsoluteMove('z'))

            self.ui.pushButtonStepMoveX.clicked.connect(lambda :self.RelativeMove('x'))
            self.ui.pushButtonStepMoveY.clicked.connect(lambda :self.RelativeMove('y'))
            self.ui.pushButtonStepMoveZ.clicked.connect(lambda :self.RelativeMove('z'))

            self.ui.pushButtonGetx.clicked.connect(lambda :self.GetCurrent('x'))
            self.ui.pushButtonGety.clicked.connect(lambda :self.GetCurrent('y'))
            self.ui.pushButtonGetz.clicked.connect(lambda :self.GetCurrent('z'))

            self.ui.pushButtonEnableUSB.clicked.connect(lambda :self.ActionUSB('enable'))
            self.ui.pushButtonDisableUSB.clicked.connect(lambda :self.ActionUSB('disable'))

            self.ui.pushButtonDisablePower.clicked.connect(lambda :self.ActionPower('disable'))
            self.ui.pushButtonEnablePower.clicked.connect(lambda :self.ActionPower('enable'))

            self.ui.pushButtonLockDUT.clicked.connect(lambda :self.ActionDUT('lock'))
            self.ui.pushButtonUnlockDUT.clicked.connect(lambda :self.ActionDUT('unlock'))

            self.ui.ButtonSetXCalUp.clicked.connect(lambda :self.SetPosition('up'))
            self.ui.ButtonSetXCalDown.clicked.connect(lambda :self.SetPosition('down'))
            self.ui.ButtonSetYCalLeft.clicked.connect(lambda :self.SetPosition('left'))
            self.ui.ButtonSetYCalRight.clicked.connect(lambda :self.SetPosition('right'))
            self.ui.ButtonSetZCal.clicked.connect(lambda :self.SetPosition('z'))

            self.ui.ButtonStartCal.clicked.connect(lambda :self.StartCal())

            self.ui.ButtonCylinderIn.clicked.connect(lambda :self.ActionCylinder('in'))
            self.ui.ButtonCylinderOut.clicked.connect(lambda :self.ActionCylinder('out'))

            self.ui.ButtonCurtainON.clicked.connect(lambda :self.ActionCurtain('on'))
            self.ui.ButtonCurtainOFF.clicked.connect(lambda :self.ActionCurtain('off'))

            self.ui.ButtonRunPattern.clicked.connect(lambda :self.RunPattern())
            self.ui.ButtonBurninStart.clicked.connect(lambda :self.Burnin())
            self.ui.pushButtonGetPLCVer.clicked.connect(lambda :self.GetVer())
            self.ui.ButtonLEDControl.clicked.connect(lambda :self.LEDLight())

            self.ui.pushButtonLimitSet.setDisabled(True)
        except Exception as e:
            print ("__init__ except fail %s\n" % e)
            # self.ShowErroeMessage("__init__ except fail %s\n" % e)
            return
    # **************************************************************#

    # **************************************************************#
    def GetVer(self):
        err = myBojayClass.ReadVer()
        self.ui.textEditPLCVer.setText(str(err))
    # **************************************************************#

    # **************************************************************#
    def LEDLight(self):
        try:
            if self.ui.comboBoxLED.currentText() == '1-red-on':
                err = myBojayClass.SetLedLightColor(myBojayClass.DUT1,myBojayClass.Red_ON)
            elif self.ui.comboBoxLED.currentText() == '1-red-off':
                err = myBojayClass.SetLedLightColor(myBojayClass.DUT1, myBojayClass.Red_OFF)
            elif self.ui.comboBoxLED.currentText() == '1-yellow-on':
                err = myBojayClass.SetLedLightColor(myBojayClass.DUT1, myBojayClass.Yellow_ON)
            elif self.ui.comboBoxLED.currentText() == '1-yellow-off':
                err = myBojayClass.SetLedLightColor(myBojayClass.DUT1, myBojayClass.Yellow_OFF)
            elif self.ui.comboBoxLED.currentText() == '1-green-on':
                err = myBojayClass.SetLedLightColor(myBojayClass.DUT1, myBojayClass.Green_ON)
            elif self.ui.comboBoxLED.currentText() == '1-green-off':
                err = myBojayClass.SetLedLightColor(myBojayClass.DUT1, myBojayClass.Green_OFF)

            elif self.ui.comboBoxLED.currentText() == '2-red-on':
                err = myBojayClass.SetLedLightColor(myBojayClass.DUT2,myBojayClass.Red_ON)
            elif self.ui.comboBoxLED.currentText() == '2-red-off':
                err = myBojayClass.SetLedLightColor(myBojayClass.DUT2, myBojayClass.Red_OFF)
            elif self.ui.comboBoxLED.currentText() == '2-yellow-on':
                err = myBojayClass.SetLedLightColor(myBojayClass.DUT2, myBojayClass.Yellow_ON)
            elif self.ui.comboBoxLED.currentText() == '2-yellow-off':
                err = myBojayClass.SetLedLightColor(myBojayClass.DUT2, myBojayClass.Yellow_OFF)
            elif self.ui.comboBoxLED.currentText() == '2-green-on':
                err = myBojayClass.SetLedLightColor(myBojayClass.DUT2, myBojayClass.Green_ON)
            elif self.ui.comboBoxLED.currentText() == '2-green-off':
                err = myBojayClass.SetLedLightColor(myBojayClass.DUT2, myBojayClass.Green_OFF)

            if err != 0:
                self.ShowErroeMessage(myBojayClass.strErrorMessage)
                return -1
            return 0
        except Exception as e:
            self.ShowErroeMessage("LEDLight except Fail %s" % e)
            return -1
    # **************************************************************#

    # **************************************************************#
    def DUTSensor(self,operation):
        try:
            if operation == 'off':
                if self.ui.radioButtonDUT1Sensor.isChecked() == True:
                    err = myBojayClass.DUTSensorOnorOFF(myBojayClass.SensorOFF,myBojayClass.DUT1)
                elif self.ui.radioButtonDUT2Sensor.isChecked() == True:
                    err = myBojayClass.DUTSensorOnorOFF(myBojayClass.SensorOFF, myBojayClass.DUT2)
            elif operation == 'on':
                if self.ui.radioButtonDUT1Sensor.isChecked() == True:
                    err = myBojayClass.DUTSensorOnorOFF(myBojayClass.SensorOn,myBojayClass.DUT1)
                elif self.ui.radioButtonDUT2Sensor.isChecked() == True:
                    err = myBojayClass.DUTSensorOnorOFF(myBojayClass.SensorOn, myBojayClass.DUT2)
            if err != 0:
                return -1
            return 0
        except Exception as e:
            self.ShowErroeMessage("DUTSensor except Fail")
            return -1


    def PassWord(self):
        try:
            if self.ui.textEditPassword.toPlainText() == 'Bojay':
                self.ui.pushButtonLimitSet.setDisabled(False)
                return 0
            else:
                self.ShowErroeMessage('Please input the correct password!')
                return -1
        except Exception as e:
            self.ShowErroeMessage("PassWord except Fail")
            return -1
    # **************************************************************#

    # **************************************************************#
    # show error message
    def ShowErroeMessage(self, message):
        try:
            myMessageBox = QMessageBox()
            myMessageBox.information(self, "Warning", message, myMessageBox.Ok)
            return 0
        except Exception as e:
            self.ShowErroeMessage("ShowErroeMessage except Fail")
            print("ShowErroeMessage except Fail " + "{0}".format(e))
            return -1
    # **************************************************************#

    # **************************************************************#
    def OpenPort(self):
        try:
            err = myBojayClass.OpenSerial()
            if err != 0:
                self.ShowErroeMessage(myBojayClass.strErrorMessage)
                return -1
            self.ShowErroeMessage('open port successful!')
            return 0
        except Exception as e:
            self.ShowErroeMessage('OpenPort except %s' % e)
            return -1
    # **************************************************************#

    # **************************************************************#
    def ClosePort(self):
        try:
            err = myBojayClass.CloseSerial()
            if err != 0:
                self.ShowErroeMessage(myBojayClass.strErrorMessage)
                return -1
            self.ShowErroeMessage('close port successful!')
            return 0
        except Exception as e:
            self.ShowErroeMessage('ClosePort except %s' % e)
            return -1
    # **************************************************************#

    # **************************************************************#
    def ActionReset(self):
        try:
            err = myBojayClass.SignalReset()
            if err != 0:
                self.ShowErroeMessage(myBojayClass.strErrorMessage)
                return -1
            return 0
        except Exception as e:
            self.ShowErroeMessage('ActionReset except %s' % e)
            return -1
    # **************************************************************#

    # **************************************************************#
    def PLCSpeed(self,operation):
        try:
            if operation == 'set':
                xValue = self.ui.textEditXSpeedSet.toPlainText()
                if xValue != '':
                    ret = myBojayClass.SetSpeed(myBojayClass.X_axis,float(xValue))
                    if ret != 0:
                        self.ShowErroeMessage(myBojayClass.strErrorMessage)
                        return -1
                yValue = self.ui.textEditYSpeedSet.toPlainText()
                if yValue != '':
                    ret = myBojayClass.SetSpeed(myBojayClass.Y_axis,float(yValue))
                    if ret != 0:
                        self.ShowErroeMessage(myBojayClass.strErrorMessage)
                        return -1
                zValue = self.ui.textEditZSpeedSet.toPlainText()
                if zValue != '':
                    ret = myBojayClass.SetSpeed(myBojayClass.Z_axis,float(zValue))
                    if ret != 0:
                        self.ShowErroeMessage(myBojayClass.strErrorMessage)
                        return -1
            elif operation == 'get':
                xValue = myBojayClass.GetSpeed(myBojayClass.X_axis)
                if xValue != -1:
                    self.ui.textEditXSpeedSet.setText(str(xValue))
                yValue = myBojayClass.GetSpeed(myBojayClass.Y_axis)
                if yValue != -1:
                    self.ui.textEditYSpeedSet.setText(str(yValue))
                zValue = myBojayClass.GetSpeed(myBojayClass.Z_axis)
                if zValue != -1:
                    self.ui.textEditZSpeedSet.setText(str(zValue))
            return 0
        except Exception as e:
            self.ShowErroeMessage('PLCSpeed except %s' % e)
            return -1
    # **************************************************************#

    # **************************************************************#
    def PLCLimit(self,operation):
        try:
            if operation == 'set':
                # x axis
                xMin = self.ui.textEditXMinLimit.toPlainText()
                if xMin != '':
                    err = myBojayClass.SetLimit(myBojayClass.X_axis,myBojayClass.Min_limit,float(xMin))
                    if err != 0:
                        self.ShowErroeMessage(myBojayClass.strErrorMessage)
                        return -1
                xMax = self.ui.textEditXMaxLimit.toPlainText()
                if xMax != '':
                    err = myBojayClass.SetLimit(myBojayClass.X_axis,myBojayClass.Max_limit,float(xMax))
                    if err != 0:
                        self.ShowErroeMessage(myBojayClass.strErrorMessage)
                        return -1

                # y axis
                yMin = self.ui.textEditYMinLimit.toPlainText()
                if yMin != '':
                    err = myBojayClass.SetLimit(myBojayClass.Y_axis,myBojayClass.Min_limit,float(yMin))
                    if err != 0:
                        self.ShowErroeMessage(myBojayClass.strErrorMessage)
                        return -1
                yMax = self.ui.textEditYMaxLimit.toPlainText()
                if yMax != '':
                    err = myBojayClass.SetLimit(myBojayClass.Y_axis,myBojayClass.Max_limit,float(yMax))
                    if err != 0:
                        self.ShowErroeMessage(myBojayClass.strErrorMessage)
                        return -1


                # z axis
                zMin = self.ui.textEditZMinLimit.toPlainText()
                if zMin != '':
                    err = myBojayClass.SetLimit(myBojayClass.Z_axis, myBojayClass.Min_limit, float(zMin))
                    if err != 0:
                        self.ShowErroeMessage(myBojayClass.strErrorMessage)
                        return -1
                zMax = self.ui.textEditZMaxLimit.toPlainText()
                if zMax != '':
                    err = myBojayClass.SetLimit(myBojayClass.Z_axis, myBojayClass.Max_limit, float(zMax))
                    if err != 0:
                        self.ShowErroeMessage(myBojayClass.strErrorMessage)
                        return -1
            elif operation == 'get':
                # x axis
                xMin = myBojayClass.GetLimit(myBojayClass.X_axis,myBojayClass.Min_limit)
                if xMin == -9999:
                    self.ShowErroeMessage(myBojayClass.strErrorMessage)
                    return -1
                self.ui.textEditXMinLimit.setText(str(xMin))
                xMax = myBojayClass.GetLimit(myBojayClass.X_axis,myBojayClass.Max_limit)
                if xMax == -9999:
                    self.ShowErroeMessage(myBojayClass.strErrorMessage)
                    return -1
                self.ui.textEditXMaxLimit.setText(str(xMax))

                # y axis
                yMin = myBojayClass.GetLimit(myBojayClass.Y_axis,myBojayClass.Min_limit)
                if yMin == -9999:
                    self.ShowErroeMessage(myBojayClass.strErrorMessage)
                    return -1
                self.ui.textEditYMinLimit.setText(str(yMin))
                yMax = myBojayClass.GetLimit(myBojayClass.Y_axis,myBojayClass.Max_limit)
                if yMax == -9999:
                    self.ShowErroeMessage(myBojayClass.strErrorMessage)
                    return -1
                self.ui.textEditYMaxLimit.setText(str(yMax))

                # z axis
                zMin = myBojayClass.GetLimit(myBojayClass.Z_axis,myBojayClass.Min_limit)
                if zMin == -9999:
                    self.ShowErroeMessage(myBojayClass.strErrorMessage)
                    return -1
                self.ui.textEditZMinLimit.setText(str(zMin))
                zMax = myBojayClass.GetLimit(myBojayClass.Z_axis,myBojayClass.Max_limit)
                if zMax == -9999:
                    self.ShowErroeMessage(myBojayClass.strErrorMessage)
                    return -1
                self.ui.textEditZMaxLimit.setText(str(zMax))
            return 0
        except Exception as e:
            self.ShowErroeMessage('PLCLimit except %s' % e)
            return -1
    # **************************************************************#

    # **************************************************************#
    def AbsoluteMove(self,operation):
        try:
            if operation == 'x':
                value = self.ui.textEditxMove.toPlainText()
                if value != '':
                    err = myBojayClass.MoveToCoordinates(myBojayClass.X_axis,float(value))
                    if err != 0:
                        self.ShowErroeMessage(myBojayClass.strErrorMessage)
                        return -1
            elif operation == 'y':
                value = self.ui.textEdityMove.toPlainText()
                if value != '':
                    err = myBojayClass.MoveToCoordinates(myBojayClass.Y_axis,float(value))
                    if err != 0:
                        self.ShowErroeMessage(myBojayClass.strErrorMessage)
                        return -1

            elif operation == 'z':
                value = self.ui.textEditzMove.toPlainText()
                if value != '':
                    err = myBojayClass.MoveToCoordinates(myBojayClass.Z_axis,float(value))
                    if err != 0:
                        self.ShowErroeMessage(myBojayClass.strErrorMessage)
                        return -1
            return 0
        except Exception as e:
            self.ShowErroeMessage('AbsoluteMove except %s' % e)
            return -1
    # **************************************************************#

    # **************************************************************#
    def RelativeMove(self,operation):
        try:
            # x axis
            if operation == 'x':
                value = self.ui.textEditStepMoveX.toPlainText()
                if value != '':
                    err = myBojayClass.SetStepValue(myBojayClass.X_axis,float(value))
                    if err != 0:
                        self.ShowErroeMessage(myBojayClass.strErrorMessage)
                        return -1
                    err = myBojayClass.MoveIncrement(myBojayClass.X_axis)
                    if err != 0:
                        self.ShowErroeMessage(myBojayClass.strErrorMessage)
                        return -1

            # y axis
            elif operation == 'y':
                value = self.ui.textEditStepMoveY.toPlainText()
                if value != '':
                    err = myBojayClass.SetStepValue(myBojayClass.Y_axis,float(value))
                    if err != 0:
                        self.ShowErroeMessage(myBojayClass.strErrorMessage)
                        return -1
                    err = myBojayClass.MoveIncrement(myBojayClass.Y_axis)
                    if err != 0:
                        self.ShowErroeMessage(myBojayClass.strErrorMessage)
                        return -1

            # z axis
            elif operation == 'z':
                value = self.ui.textEditStepMoveZ.toPlainText()
                if value != '':
                    err = myBojayClass.SetStepValue(myBojayClass.Z_axis,float(value))
                    if err != 0:
                        self.ShowErroeMessage(myBojayClass.strErrorMessage)
                        return -1
                    err = myBojayClass.MoveIncrement(myBojayClass.Z_axis)
                    if err != 0:
                        self.ShowErroeMessage(myBojayClass.strErrorMessage)
                        return -1
            return 0
        except Exception as e:
            self.ShowErroeMessage('RelativeMove except %s' % e)
            return -1
    # **************************************************************#

    # **************************************************************#
    def GetCurrent(self,operation):
        try:
            # x axis
            if operation == 'x':
                err = myBojayClass.GetCurrentCoordinates(myBojayClass.X_axis)
                if err == -9999:
                    self.ShowErroeMessage(myBojayClass.strErrorMessage)
                    return -1
                self.ui.textEditxMove.setText(str(err))

            # y axis
            elif operation == 'y':
                err = myBojayClass.GetCurrentCoordinates(myBojayClass.Y_axis)
                if err == -9999:
                    self.ShowErroeMessage(myBojayClass.strErrorMessage)
                    return -1
                self.ui.textEdityMove.setText(str(err))

            # z axis
            elif operation == 'z':
                err = myBojayClass.GetCurrentCoordinates(myBojayClass.Z_axis)
                if err == -9999:
                    self.ShowErroeMessage(myBojayClass.strErrorMessage)
                    return -1
                self.ui.textEditzMove.setText(str(err))
            return 0
        except Exception as e:
            self.ShowErroeMessage('GetCurrent except %s' % e)
            return -1
    # **************************************************************#

    # **************************************************************#
    def ActionUSB(self,opertaion):
        try:
            if opertaion == 'enable':
                WhicUSB = 0
                if self.ui.radioButtonUSB1.isChecked() == True:
                    WhicUSB = myBojayClass.USB1
                elif self.ui.radioButtonUSB2.isChecked() == True:
                    WhicUSB = myBojayClass.USB2
                elif self.ui.radioButtonUSBall.isChecked() == True:
                    WhicUSB = myBojayClass.USB_all
                err = myBojayClass.USBEableOrDisable(myBojayClass.USBEnable,WhicUSB)
                if err != 0:
                    self.ShowErroeMessage(myBojayClass.strErrorMessage)
                    return -1
            elif opertaion == 'disable':
                WhicUSB = 0
                if self.ui.radioButtonUSB1.isChecked() == True:
                    WhicUSB = myBojayClass.USB1
                elif self.ui.radioButtonUSB2.isChecked() == True:
                    WhicUSB = myBojayClass.USB2
                elif self.ui.radioButtonUSBall.isChecked() == True:
                    WhicUSB = myBojayClass.USB_all
                err = myBojayClass.USBEableOrDisable(myBojayClass.USBDisable,WhicUSB)
                if err != 0:
                    self.ShowErroeMessage(myBojayClass.strErrorMessage)
                    return -1
            return 0
        except Exception as e:
            self.ShowErroeMessage('ActionUSB except %s' % e)
            return -1
    # **************************************************************#

    # **************************************************************#
    def ActionPower(self,operation):
        try:
            if operation == 'enable':
                WhichPower = 0
                if self.ui.radioButtonPower1.isChecked() == True:
                    WhichPower = myBojayClass.Power1
                elif self.ui.radioButtonPower2.isChecked() == True:
                    WhichPower = myBojayClass.Power2
                elif self.ui.radioButtonPowerall.isChecked() == True:
                    WhichPower = myBojayClass.Power_all
                err = myBojayClass.PowerEnableOrDisable(myBojayClass.PowerEnable,WhichPower)
                if err != 0:
                    self.ShowErroeMessage(myBojayClass.strErrorMessage)
                    return -1
            elif operation == 'disable':
                WhichPower = 0
                if self.ui.radioButtonPower1.isChecked() == True:
                    WhichPower = myBojayClass.Power1
                elif self.ui.radioButtonPower2.isChecked() == True:
                    WhichPower = myBojayClass.Power2
                elif self.ui.radioButtonPowerall.isChecked() == True:
                    WhichPower = myBojayClass.Power_all
                err = myBojayClass.PowerEnableOrDisable(myBojayClass.PowerDisable,WhichPower)
                if err != 0:
                    self.ShowErroeMessage(myBojayClass.strErrorMessage)
                    return -1
            return 0
        except Exception as e:
            self.ShowErroeMessage('ActionPower except %s' % e)
            return -1
    # **************************************************************#

    # **************************************************************#
    def ActionDUT(self,opertaion):
        try:
            if opertaion == 'lock':
                WhichDUT = 0
                if self.ui.radioButtonDUT1.isChecked() == True:
                    WhichDUT = myBojayClass.DUT1
                elif self.ui.radioButtonDUT2.isChecked() == True:
                    WhichDUT = myBojayClass.DUT2
                elif self.ui.radioButtonDUTall.isChecked() == True:
                    WhichDUT = myBojayClass.DUT_all
                err = myBojayClass.DUTLockOrUnlock(myBojayClass.DUTLock,WhichDUT)
                if err != 0:
                    self.ShowErroeMessage(myBojayClass.strErrorMessage)
                    return -1
            elif opertaion == 'unlock':
                WhichDUT = 0
                if self.ui.radioButtonDUT1.isChecked() == True:
                    WhichDUT = myBojayClass.DUT1
                elif self.ui.radioButtonDUT2.isChecked() == True:
                    WhichDUT = myBojayClass.DUT2
                elif self.ui.radioButtonDUTall.isChecked() == True:
                    WhichDUT = myBojayClass.DUT_all
                err = myBojayClass.DUTLockOrUnlock(myBojayClass.DUTUnlock,WhichDUT)
                if err != 0:
                    self.ShowErroeMessage(myBojayClass.strErrorMessage)
                    return -1
            return 0
        except Exception as e:
            self.ShowErroeMessage('ActionDUT except %s' % e)
            return -1
    # **************************************************************#

    # **************************************************************#
    def SetPosition(self,direction):
        try:
            retx = myBojayClass.GetCurrentCoordinates(myBojayClass.X_axis)
            if retx == -9999:
                self.ShowErroeMessage(myBojayClass.strErrorMessage)
                return -1


            rety = myBojayClass.GetCurrentCoordinates(myBojayClass.Y_axis)
            if rety == -9999:
                self.ShowErroeMessage(myBojayClass.strErrorMessage)
                return -1
            output = open("CalibrationInitial.txt",'a')
            if "up" in direction:
                self.SetUpx = retx
                self.SetUpy = rety
                output.write("XAxisCalIncrementX=" + str(self.SetUpx) + "\n")
                output.write("XAxisCalIncrementY=" + str(self.SetUpy) + "\n")
            elif "left" in direction:
                self.SetLeftx = retx
                self.SetLefty = rety
                output.write("YAxisCalIncrementX=" + str(self.SetLeftx) + "\n")
                output.write("YAxisCalIncrementY=" + str(self.SetLefty) + "\n")
            elif "down" in direction:
                self.SetDownx = retx
                self.SetDowny = rety
                output.write("XAxisCalDecrementX=" + str(self.SetDownx) + "\n")
                output.write("XAxisCalDecrementY=" + str(self.SetDowny) + "\n")
            elif "right" in direction:
                self.SetRightx = retx
                self.SetRighty = rety
                output.write("YAxisCalDecrementX=" + str(self.SetRightx) + "\n")
                output.write("YAxisCalDecrementY=" + str(self.SetRighty) + "\n")
            elif "z" in direction:
                self.SetZx = retx
                self.SetZy = rety
                output.write("ZIncrementX=" + str(self.SetZx) + "\n")
                output.write("ZIncrementY=" + str(self.SetZy) + "\n")
            output.close()
            return 0
        except Exception as e:
            self.ShowErroeMessage('SetPosition except %s' % e)
            return -1
    # **************************************************************#

    # **************************************************************#
    def StartCal(self):
        try:
            offset = self.ui.textEditOffset.toPlainText()
            if offset != '':
                offset = float(offset)
            else:
                offset = 0
            err = myBojayClass.CalibrationPosition(offset)
            if err != 0:
                self.ShowErroeMessage(myBojayClass.strErrorMessage)
                return -1
            self.ShowErroeMessage('Calibration finish!')
        except Exception as e:
            self.ShowErroeMessage('StartCal except %s' % e)
            return -1
    # **************************************************************#

    # **************************************************************#
    def ActionCylinder(self,operation):
        try:
            if operation == 'in':
                err = myBojayClass.Set_CylindeFunction(myBojayClass.Cylinder_IN)
                if err != 0:
                    self.ShowErroeMessage(myBojayClass.strErrorMessage)
                    return -1
            elif operation == 'out':
                err = myBojayClass.Set_CylindeFunction(myBojayClass.Cylinder_OUT)
                if err != 0:
                    self.ShowErroeMessage(myBojayClass.strErrorMessage)
                    return -1
            return 0
        except Exception as e:
            self.ShowErroeMessage('ActionCylinder except %s' % e)
            return -1
    # **************************************************************#

    # **************************************************************#
    def ActionCurtain(self,operation):
        try:
            if operation == 'on':
                err = myBojayClass.AlarmBuzzer(myBojayClass.Alarm_On)
                if err != 0:
                    self.ShowErroeMessage(myBojayClass.strErrorMessage)
                    return -1
            elif operation == 'off':
                err = myBojayClass.AlarmBuzzer(myBojayClass.Alarm_Off)
                if err != 0:
                    self.ShowErroeMessage(myBojayClass.strErrorMessage)
                    return -1
            return 0
        except Exception as e:
            self.ShowErroeMessage('ActionCurtain except %s' % e)
            return -1
    # **************************************************************#

    # **************************************************************#
    def RunPattern(self):
        try:
            type = self.ui.comboBox.currentText()
            if str(type) == 'Rectangle':
                err = myBojayClass.CreateRectangle(18.65,29.37,16,10,12,myBojayClass.XAxisMinLimit,myBojayClass.XAxisMaxLimit,myBojayClass.YAxisMinLimit,myBojayClass.YAxisMaxLimit)
                if err != 0:
                    self.ShowErroeMessage(myBojayClass.strErrorMessage)
                    return -1
            elif str(type) == 'Circle/EIIipse':
                err = myBojayClass.CreateCircle(18.65,29.37,2,2,0.5,5,myBojayClass.XAxisMinLimit,myBojayClass.XAxisMaxLimit,myBojayClass.YAxisMinLimit,myBojayClass.YAxisMaxLimit)
                if err != 0:
                    self.ShowErroeMessage(myBojayClass.strErrorMessage)
                    return -1
            err = myBojayClass.Set_CylindeFunction(myBojayClass.Cylinder_IN)
            if err != 0:
                self.ShowErroeMessage(myBojayClass.strErrorMessage)
                return -1
            err = myBojayClass.RunPattern()
            if err != 0:
                self.ShowErroeMessage(myBojayClass.strErrorMessage)
                return -1
            self.ShowErroeMessage('RunPattern finish!')
            return 0
        except Exception as e:
            self.ShowErroeMessage('RunPattern except %s' % e)
            return -1
    # **************************************************************#

    # **************************************************************#
    def Burnin(self):
        try:
            count = self.ui.textEditBurninTimes.toPlainText()
            if count == '':
                self.ShowErroeMessage('please input the burnin counts')
                return -1
            for i in range(int(count)):
                # 1.lock dut
                err = myBojayClass.DUTLockOrUnlock(myBojayClass.DUTLock)
                if err != 0:
                    self.ShowErroeMessage('burn in fail beause of locking dut err')
                    return -1

                # 2.enable usb and power
                err = myBojayClass.PowerEnableOrDisable(myBojayClass.PowerEnable)
                if err != 0:
                    self.ShowErroeMessage('burn in fail beause of enable power err')
                    return -1

                err = myBojayClass.USBEableOrDisable(myBojayClass.USBEnable)
                if err != 0:
                    self.ShowErroeMessage('burn in fail beause of enable usb err')
                    return -1

                # 3.cylinder in
                err = myBojayClass.Set_CylindeFunction(myBojayClass.Cylinder_IN)
                if err != 0:
                    self.ShowErroeMessage('burn in fail beause of cylinder in err')
                    return -1

                err = myBojayClass.MoveToCoordinates(myBojayClass.Z_axis,5)
                if err != 0:
                    self.ShowErroeMessage('burn in fail beause of move z axis err')
                    return -1

                # 4.RunPattern
                err = myBojayClass.RunPattern()
                if err != 0:
                    self.ShowErroeMessage('burn in fail beause of run pattern err')
                    return -1

                err = myBojayClass.MoveToCoordinates(myBojayClass.Z_axis,0)
                if err != 0:
                    self.ShowErroeMessage('burn in fail beause of move z axis go zero err')
                    return -1

                # 5.go home
                err = myBojayClass.SynchronousXY(0,0,10)
                if err != 0:
                    self.ShowErroeMessage('burn in fail beause of sync zero err')
                    return -1

                # 6.cylinder out
                err = myBojayClass.Set_CylindeFunction(myBojayClass.Cylinder_OUT)
                if err != 0:
                    self.ShowErroeMessage('burn in fail beause of cylinder out err')
                    return -1

                # 7.disable usb and power
                err = myBojayClass.PowerEnableOrDisable(myBojayClass.PowerDisable)
                if err != 0:
                    self.ShowErroeMessage('burn in fail beause of diable power err')
                    return -1

                err = myBojayClass.USBEableOrDisable(myBojayClass.USBDisable)
                if err != 0:
                    self.ShowErroeMessage('burn in fail beause of disable usb err')
                    return -1

                # 8.unlock dut
                err = myBojayClass.DUTLockOrUnlock(myBojayClass.DUTUnlock)
                if err != 0:
                    self.ShowErroeMessage('burn in fail beause of unlocking dut err')
                    return -1
                print(i+1)
            self.ShowErroeMessage('Burnin finish! Times %d' % int(count))
            return 0
        except Exception as e:
            self.ShowErroeMessage('RunPattern except %s' % e)
            return -1
    # **************************************************************#

    # **************************************************************#
    def GetDutFourCornerPoint(self):
        try:
            Z1 = 0
            Z2 = 0
            Z3 = 0
            Z4 = 0
            CenterX = 0
            CenterY = 0
            CenterZ = 0

            exeFolderPath = os.getcwd()
            exeFolderPath += "\\Calibration.txt"
            calibraionFile = open(exeFolderPath)
            alllines = calibraionFile.readlines()
            for line in alllines:
                strLine = line.strip()
                if ("X-Finial=" in strLine):
                    CenterX = float(strLine[strLine.find("=") + 1:])
                elif ("Y-Finial=" in strLine):
                    CenterY = float(strLine[strLine.find("=") + 1:])
                elif ("Z-Finial=" in strLine):
                    CenterZ= float(strLine[strLine.find("=") + 1:])

            # First Point Z1
            myBojayClass.MoveToCoordinates(myBojayClass.Z_axis,0,10)
            err = myBojayClass.MoveToCoordinates(myBojayClass.X_axis, CenterX - 50)
            if err != 0:
                self.ShowErroeMessage(myBojayClass.strErrorMessage)
                return -1
            err = myBojayClass.MoveToCoordinates(myBojayClass.Y_axis, CenterY - 30)
            if err != 0:
                self.ShowErroeMessage(myBojayClass.strErrorMessage)
                return -1
            err = myBojayClass.MoveToCoordinates(myBojayClass.Z_axis, CenterZ-5, 10)
            if err != 0:
                self.ShowErroeMessage(myBojayClass.strErrorMessage)
                return -1
            Z1 = myBojayClass.Calibrate(myBojayClass.Z_axis,"increment")
            if (Z1 == -1):
                self.ShowErroeMessage(myBojayClass.strErrorMessage)
                print("Z1 axis calibration error")
                return -1
            else:
                print("Z1 axis calibration value=" + str(Z1))

            # First Point Z2
            myBojayClass.MoveToCoordinates(myBojayClass.Z_axis, 0, 10)
            err = myBojayClass.MoveToCoordinates(myBojayClass.X_axis, CenterX - 50)
            if err != 0:
                self.ShowErroeMessage(myBojayClass.strErrorMessage)
                return -1
            err = myBojayClass.MoveToCoordinates(myBojayClass.Y_axis, CenterY + 30)
            if err != 0:
                self.ShowErroeMessage(myBojayClass.strErrorMessage)
                return -1
            err = myBojayClass.MoveToCoordinates(myBojayClass.Z_axis, CenterZ - 5, 10)
            if err != 0:
                self.ShowErroeMessage(myBojayClass.strErrorMessage)
                return -1
            Z2 = myBojayClass.Calibrate(myBojayClass.Z_axis, "increment")
            if (Z2 == -1):
                self.ShowErroeMessage(myBojayClass.strErrorMessage)
                print("Z2 axis calibration error")
                return -1
            else:
                print("Z2 axis calibration value=" + str(Z2))

            # First Point Z3
            myBojayClass.MoveToCoordinates(myBojayClass.Z_axis, 0, 10)
            err = myBojayClass.MoveToCoordinates(myBojayClass.X_axis, CenterX + 50)
            if err != 0:
                self.ShowErroeMessage(myBojayClass.strErrorMessage)
                return -1
            err = myBojayClass.MoveToCoordinates(myBojayClass.Y_axis, CenterY - 30)
            if err != 0:
                self.ShowErroeMessage(myBojayClass.strErrorMessage)
                return -1
            err = myBojayClass.MoveToCoordinates(myBojayClass.Z_axis, CenterZ - 5, 10)
            if err != 0:
                self.ShowErroeMessage(myBojayClass.strErrorMessage)
                return -1
            Z3 = myBojayClass.Calibrate(myBojayClass.Z_axis, "increment")
            if (Z3 == -1):
                self.ShowErroeMessage(myBojayClass.strErrorMessage)
                print("Z3 axis calibration error")
                return -1
            else:
                print("Z3 axis calibration value=" + str(Z3))

            # First Point Z4
            myBojayClass.MoveToCoordinates(myBojayClass.Z_axis, 0, 10)
            err = myBojayClass.MoveToCoordinates(myBojayClass.X_axis, CenterX + 50)
            if err != 0:
                self.ShowErroeMessage(myBojayClass.strErrorMessage)
                return -1
            err = myBojayClass.MoveToCoordinates(myBojayClass.Y_axis, CenterY + 30)
            if err != 0:
                self.ShowErroeMessage(myBojayClass.strErrorMessage)
                return -1
            err = myBojayClass.MoveToCoordinates(myBojayClass.Z_axis, CenterZ - 5, 10)
            if err != 0:
                self.ShowErroeMessage(myBojayClass.strErrorMessage)
                return -1
            Z4 = myBojayClass.Calibrate(myBojayClass.Z_axis, "increment")
            if (Z4 == -1):
                self.ShowErroeMessage(myBojayClass.strErrorMessage)
                print("Z4 axis calibration error")
                return -1
            else:
                print("Z4 axis calibration value=" + str(Z4))

            exeFolderPath = os.getcwd()
            exeFolderPath += "\\GetDutFourCornerPoint.txt"
            output = open(exeFolderPath, 'w')
            output.write("Z1=" + str(Z1) + "\n")
            output.write("Z2=" + str(Z2) + "\n")
            output.write("Z3=" + str(Z3) + "\n")
            output.write("Z4=" + str(Z4) + "\n")

        except Exception as e:
            self.ShowErroeMessage('GetDutFourCornerPoint except %s' % e)
            return -1
    # **************************************************************#

    # **************************************************************#

app = QtWidgets.QApplication(sys.argv)
myTonyFrame = TonyFrame()
myTonyFrame.show()
myTonyFrame.exec_()