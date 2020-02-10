#-*-coding:utf-8-*-
from PySide2 import QtCore,QtGui,QtWidgets
from PySide2.QtCore import QTimer
from PySide2.QtWidgets import QDialog,QMessageBox
# from PyQt5 import QtCore,QtGui,QtWidgets
# from PyQt5.QtCore import QTimer
# from PyQt5.QtWidgets import QDialog,QMessageBox
from GOEPLCControl import *
from UI import *
import pandas as pd

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

            self.ui.pushButtonOpenPort.clicked.connect(lambda :self.OpenPort())
            self.ui.pushButtonClosePort.clicked.connect(lambda :self.ClosePort())
            self.ui.pushButtonClosePort.setEnabled(False)
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

            self.ui.pushButtonUSBIn.clicked.connect(lambda :self.ActionUSB('enable'))
            self.ui.pushButtonUSBOut.clicked.connect(lambda :self.ActionUSB('disable'))

            self.ui.pushButtonDCIn.clicked.connect(lambda: self.ActionDC('enable'))
            self.ui.pushButtonDCOut.clicked.connect(lambda: self.ActionDC('disable'))

            self.ui.pushButtonCylinderIn.clicked.connect(lambda :self.ActionCylinder('in'))
            self.ui.pushButtonCylinderOut.clicked.connect(lambda :self.ActionCylinder('out'))


            self.ui.pushButtonPin1Down.clicked.connect(lambda :self.ActionPin(1,'down'))
            self.ui.pushButtonPin1Up.clicked.connect(lambda: self.ActionPin(1, 'up'))

            self.ui.pushButtonPin2Down.clicked.connect(lambda: self.ActionPin(2, 'down'))
            self.ui.pushButtonPin2Up.clicked.connect(lambda: self.ActionPin(2, 'up'))



            self.ui.pushButtonOpenCurtain.clicked.connect(lambda :self.ActionCurtain('on'))
            self.ui.pushButtonCloseCurtain.clicked.connect(lambda :self.ActionCurtain('off'))

            self.ui.pushButtonBurn.clicked.connect(self.actionStartTest)
            # self.ui.pushButtonSaveCalData.clicked.connect(self.SaveCalData)

            self.ui.pushButtonUp.clicked.connect(lambda :self.SetCalPos('up'))
            self.ui.pushButtonLeft.clicked.connect(lambda: self.SetCalPos('left'))
            self.ui.pushButtonDown.clicked.connect(lambda: self.SetCalPos('down'))
            self.ui.pushButtonRight.clicked.connect(lambda: self.SetCalPos('right'))
            self.ui.pushButtonMiddle.clicked.connect(lambda: self.SetCalPos('middle'))
            self.ui.pushButtonStartCal.clicked.connect(self.StartCal)
            self.ui.pushButtonGetPLCVer.clicked.connect(self.GetPlcVersion)

            self.ui.pushButtonClosePort.setEnabled(False)
            self.ui.pushButtonSignalReSet.setEnabled(False)
            self.ui.pushButtonSpeedSet.setEnabled(False)
            self.ui.pushButtonSpeedGet.setEnabled(False)
            self.ui.pushButtonLimitSet.setEnabled(False)
            self.ui.pushButtonPassword.setEnabled(False)
            self.ui.pushButtonLimitGet.setEnabled(False)
            self.ui.pushButtonMovex.setEnabled(False)
            self.ui.pushButtonMovey.setEnabled(False)
            self.ui.pushButtonMovez.setEnabled(False)
            self.ui.pushButtonGetx.setEnabled(False)
            self.ui.pushButtonGety.setEnabled(False)
            self.ui.pushButtonGetz.setEnabled(False)
            self.ui.pushButtonUSBIn.setEnabled(False)
            self.ui.pushButtonUSBOut.setEnabled(False)
            self.ui.pushButtonDCIn.setEnabled(False)
            self.ui.pushButtonDCOut.setEnabled(False)
            self.ui.pushButtonCylinderIn.setEnabled(False)
            self.ui.pushButtonCylinderOut.setEnabled(False)
            self.ui.pushButtonPin1Down.setEnabled(False)
            self.ui.pushButtonPin1Up.setEnabled(False)
            self.ui.pushButtonPin2Down.setEnabled(False)
            self.ui.pushButtonPin2Down.setEnabled(False)
            self.ui.pushButtonPin2Up.setEnabled(False)
            self.ui.pushButtonOpenCurtain.setEnabled(False)
            self.ui.pushButtonCloseCurtain.setEnabled(False)
            self.ui.pushButtonBurn.setEnabled(False)
            self.ui.pushButtonStartCal.setEnabled(False)
            self.ui.pushButtonGetPLCVer.setEnabled(False)
            self.ui.pushButtonStepMoveX.setEnabled(False)
            self.ui.pushButtonStepMoveY.setEnabled(False)
            self.ui.pushButtonStepMoveZ.setEnabled(False)
        except Exception as e:
            print ("__init__ except fail %s\n" % e)
            # self.ShowErroeMessage("__init__ except fail %s\n" % e)
            return
    # **************************************************************#

    # # **************************************************************#
    # def GetVer(self):
    #     err = myBojayClass.ReadVer()
    #     self.ui.textEditPLCVer.setText(str(err))
    # # **************************************************************#

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
    def PassWord(self):
        try:
            if self.ui.textEditPassword.toPlainText() == 'Bojay':
                self.ui.pushButtonLimitSet.setEnabled(True)
                self.ui.pushButtonLimitGet.setEnabled(True)
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
            # self.ShowErroeMessage('open port successful!')
            self.ui.pushButtonClosePort.setEnabled(True)
            self.ui.pushButtonSignalReSet.setEnabled(True)
            self.ui.pushButtonSpeedSet.setEnabled(True)
            #self.ui.pushButtonSpeedGet.setEnabled(True)
            #self.ui.pushButtonLimitSet.setEnabled(True)
            self.ui.pushButtonPassword.setEnabled(True)
            #self.ui.pushButtonLimitGet.setEnabled(True)
            self.ui.pushButtonMovex.setEnabled(True)
            self.ui.pushButtonMovey.setEnabled(True)
            self.ui.pushButtonMovez.setEnabled(True)
            self.ui.pushButtonGetx.setEnabled(True)
            self.ui.pushButtonGety.setEnabled(True)
            self.ui.pushButtonGetz.setEnabled(True)
            self.ui.pushButtonUSBIn.setEnabled(True)
            self.ui.pushButtonUSBOut.setEnabled(True)
            self.ui.pushButtonDCIn.setEnabled(True)
            self.ui.pushButtonDCOut.setEnabled(True)
            self.ui.pushButtonCylinderIn.setEnabled(True)
            self.ui.pushButtonCylinderOut.setEnabled(True)
            self.ui.pushButtonPin1Down.setEnabled(True)
            self.ui.pushButtonPin1Up.setEnabled(True)
            self.ui.pushButtonPin2Down.setEnabled(True)
            self.ui.pushButtonPin2Down.setEnabled(True)
            self.ui.pushButtonPin2Up.setEnabled(True)
            self.ui.pushButtonOpenCurtain.setEnabled(True)
            self.ui.pushButtonCloseCurtain.setEnabled(True)
            self.ui.pushButtonBurn.setEnabled(True)
            self.ui.pushButtonStartCal.setEnabled(True)
            self.ui.pushButtonGetPLCVer.setEnabled(True)
            self.ui.pushButtonStepMoveX.setEnabled(True)
            self.ui.pushButtonStepMoveY.setEnabled(True)
            self.ui.pushButtonStepMoveZ.setEnabled(True)
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
                else:
                    self.ShowErroeMessage(myBojayClass.strErrorMessage)
                    return -1
                yValue = myBojayClass.GetSpeed(myBojayClass.Y_axis)
                if yValue != -1:
                    self.ui.textEditYSpeedSet.setText(str(yValue))
                else:
                    self.ShowErroeMessage(myBojayClass.strErrorMessage)
                    return -1
                zValue = myBojayClass.GetSpeed(myBojayClass.Z_axis)
                if zValue != -1:
                    self.ui.textEditZSpeedSet.setText(str(zValue))
                else:
                    self.ShowErroeMessage(myBojayClass.strErrorMessage)
                    return -1
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
                    err = myBojayClass.SetPLCLimit(myBojayClass.X_axis,myBojayClass.Min_limit,float(xMin))
                    if err != 0:
                        self.ShowErroeMessage(myBojayClass.strErrorMessage)
                        return -1
                xMax = self.ui.textEditXMaxLimit.toPlainText()
                if xMax != '':
                    err = myBojayClass.SetPLCLimit(myBojayClass.X_axis,myBojayClass.Max_limit,float(xMax))
                    if err != 0:
                        self.ShowErroeMessage(myBojayClass.strErrorMessage)
                        return -1

                # y axis
                yMin = self.ui.textEditYMinLimit.toPlainText()
                if yMin != '':
                    err = myBojayClass.SetPLCLimit(myBojayClass.Y_axis,myBojayClass.Min_limit,float(yMin))
                    if err != 0:
                        self.ShowErroeMessage(myBojayClass.strErrorMessage)
                        return -1
                yMax = self.ui.textEditYMaxLimit.toPlainText()
                if yMax != '':
                    err = myBojayClass.SetPLCLimit(myBojayClass.Y_axis,myBojayClass.Max_limit,float(yMax))
                    if err != 0:
                        self.ShowErroeMessage(myBojayClass.strErrorMessage)
                        return -1


                # z axis
                zMin = self.ui.textEditZMinLimit.toPlainText()
                if zMin != '':
                    err = myBojayClass.SetPLCLimit(myBojayClass.Z_axis, myBojayClass.Min_limit, float(zMin))
                    if err != 0:
                        self.ShowErroeMessage(myBojayClass.strErrorMessage)
                        return -1
                zMax = self.ui.textEditZMaxLimit.toPlainText()
                if zMax != '':
                    err = myBojayClass.SetPLCLimit(myBojayClass.Z_axis, myBojayClass.Max_limit, float(zMax))
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
                    dValue  =float(value)
                    err = myBojayClass.MoveToCoordinates(myBojayClass.X_axis,dValue)
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
                ret = myBojayClass.USBLockandUnlock(myBojayClass.USBLock)
                if ret != 0:
                    self.ShowErroeMessage(myBojayClass.strErrorMessage)
                    return -1
            elif opertaion == 'disable':
                ret = myBojayClass.USBLockandUnlock(myBojayClass.USBUnlock)
                if ret != 0:
                    self.ShowErroeMessage(myBojayClass.strErrorMessage)
                    return -1
            return 0
        except Exception as e:
            self.ShowErroeMessage('ActionUSB except %s' % e)
            return -1
    # **************************************************************#



    # **************************************************************#
    def ActionDC(self,opertaion):
        try:
            if opertaion == 'enable':
                ret = myBojayClass.DCLockandUnlock(myBojayClass.DCLock)
                if ret != 0:
                    self.ShowErroeMessage(myBojayClass.strErrorMessage)
                    return -1
            elif opertaion == 'disable':
                ret = myBojayClass.DCLockandUnlock(myBojayClass.DCUnlock)
                if ret != 0:
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
            PositionList = []
            df = pd.read_csv(os.path.join(os.getcwd(),'CalibrationInitial.csv'))
            for index,row in df.iterrows():
                PositionList.append(df.loc[index]["coordinate"])
            print (PositionList)
            CenetrPoint = []
            err = myBojayClass.CalibratePositionOfV71(CenetrPoint,PositionList)
            if err != 0:
                self.ShowErroeMessage(myBojayClass.strErrorMessage)
                return -1
            self.ShowErroeMessage('Calibration finish!')
        except Exception as e:
            self.ShowErroeMessage('StartCal except %s' % e)
            return -1
    # **************************************************************#

    # **************************************************************#
    def ActionPin(self,index,direction):
        try:
            if index == 1:
                if 'down' in direction:
                    ret = myBojayClass.PushPinDown(myBojayClass.Pin1)
                elif 'up' in direction:
                    ret = myBojayClass.LiftPinUp(myBojayClass.Pin1)
            elif index == 2:
                if 'down' in direction:
                    ret = myBojayClass.PushPinDown(myBojayClass.Pin2)
                elif 'up' in direction:
                    ret = myBojayClass.LiftPinUp(myBojayClass.Pin2)
            if ret != 0:
                self.ShowErroeMessage(myBojayClass.strErrorMessage)
                return -1
            return 0
        except Exception as e:
            self.ShowErroeMessage('ActionPin except %s' % e)
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
                err = myBojayClass.SetLightCurtain(myBojayClass.LightCurtainOn)
                if err != 0:
                    self.ShowErroeMessage(myBojayClass.strErrorMessage)
                    return -1
            elif operation == 'off':
                err = myBojayClass.SetLightCurtain(myBojayClass.LightCurtainOff)
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
            count = self.ui.textEditBurnTimes.toPlainText()
            if count == '':
                self.ShowErroeMessage('please input the burnin counts')
                return -1

            intTimes = int(count)
            ret = myBojayClass.BurningTestOfV71(intTimes)
            if ret == 0:
                return 0
            else:
                self.ShowErroeMessage(myBojayClass.strErrorMessage)
                return -1
        except Exception as e:
            self.ShowErroeMessage('RunPattern except %s' % e)
            return -1
    # **************************************************************#


    # **************************************************************#
    def SaveCalData(self):
        try:
            x = myBojayClass.GetCurrentCoordinates(myBojayClass.X_axis)
            y = myBojayClass.GetCurrentCoordinates(myBojayClass.Y_axis)
            z = myBojayClass.GetCurrentCoordinates(myBojayClass.Z_axis)

        except Exception as e:
            self.ShowErroeMessage('SaveCalData except %s' % e)
            return -1
    # **************************************************************#

    # **************************************************************#
    def SetCalPos(self,direction):
        try:
            column_list = [ 'Zincrementx','Zincrementy','XAxisCalIncrementX',
                            'XAxisCalIncrementY','XAxisCalDecrementX',
                            'XAxisCalDecrementY', 'YAxisCalIncrementX',
                            'YAxisCalIncrementY','YAxisCalDecrementX',
                            'YAxisCalDecrementY']
            print (os.getcwd())
            if not os.path.exists(os.path.join(os.getcwd(),'CalibrationInitial.csv')):
                data_list = []
                for i in range(len(column_list)):
                    data_list.append([column_list[i],0])
                df = pd.DataFrame(data=data_list,columns=['item','coordinate'])
                df.to_csv(os.path.join(os.getcwd(),'CalibrationInitial.csv'),index=False)

            df = pd.read_csv(os.path.join(os.getcwd(),'CalibrationInitial.csv'))
            for index,row in df.iterrows():
                if 'up' in direction:
                    if "YAxisCalIncrementX" in row["item"]:
                        df.loc[index,'coordinate'] = myBojayClass.GetCurrentCoordinates(myBojayClass.X_axis)
                    if "YAxisCalIncrementY" in row["item"]:
                        df.loc[index,'coordinate'] = myBojayClass.GetCurrentCoordinates(myBojayClass.Y_axis)
                elif 'down' in direction:
                    if "YAxisCalDecrementX" in row["item"]:
                        df.loc[index,'coordinate'] = myBojayClass.GetCurrentCoordinates(myBojayClass.X_axis)
                    if "YAxisCalDecrementY" in row["item"]:
                        df.loc[index,'coordinate'] = myBojayClass.GetCurrentCoordinates(myBojayClass.Y_axis)
                elif 'left' in direction:
                    if "XAxisCalIncrementX" in row["item"]:
                        df.loc[index,'coordinate'] = myBojayClass.GetCurrentCoordinates(myBojayClass.X_axis)
                    if "XAxisCalIncrementY" in row["item"]:
                        df.loc[index,'coordinate'] = myBojayClass.GetCurrentCoordinates(myBojayClass.Y_axis)
                elif 'right' in direction:
                    if "XAxisCalDecrementX" in row["item"]:
                        df.loc[index,'coordinate'] = myBojayClass.GetCurrentCoordinates(myBojayClass.X_axis)
                    if "XAxisCalDecrementY" in row["item"]:
                        df.loc[index,'coordinate'] = myBojayClass.GetCurrentCoordinates(myBojayClass.Y_axis)
                elif 'middle' in direction:
                    if "Zincrementx" in row["item"]:
                        df.loc[index,'coordinate'] = myBojayClass.GetCurrentCoordinates(myBojayClass.X_axis)
                    if "Zincrementy" in row["item"]:
                        df.loc[index,'coordinate'] = myBojayClass.GetCurrentCoordinates(myBojayClass.Y_axis)
                # if 'up' in direction:
                #     if "YAxisCalIncrementX" in row["item"]:
                #         df.loc[index,'coordinate'] = 100
                #     if "YAxisCalIncrementY" in row["item"]:
                #         df.loc[index,'coordinate'] = 1000
                # elif 'down' in direction:
                #     if "YAxisCalDecrementX" in row["item"]:
                #         df.loc[index,'coordinate'] = 10000
                #     if "YAxisCalDecrementY" in row["item"]:
                #         df.loc[index,'coordinate'] = 100000
                # elif 'left' in direction:
                #     if "XAxisCalIncrementX" in row["item"]:
                #         df.loc[index,'coordinate'] = 1000000
                #     if "XAxisCalIncrementY" in row["item"]:
                #         df.loc[index,'coordinate'] = 10000000
                # elif 'right' in direction:
                #     if "XAxisCalDecrementX" in row["item"]:
                #         df.loc[index,'coordinate'] = 1000000000
                #     if "XAxisCalDecrementY" in row["item"]:
                #         df.loc[index,'coordinate'] = 10000000000
                # elif 'middle' in direction:
                #     if "Zincrementx" in row["item"]:
                #         df.loc[index,'coordinate'] = 100000000000
                #     if "Zincrementy" in row["item"]:
                #         df.loc[index,'coordinate'] = 1000000000000
            df.to_csv(os.path.join(os.getcwd(), 'CalibrationInitial.csv'), index=False)
        except Exception as e:
            self.ShowErroeMessage('SetCalPos except %s' % e)
            return -1
    # **************************************************************#


    # **************************************************************#
    def GetPlcVersion(self):
        try:
            ret = myBojayClass.GetVer()
            if ret == -1:
                self.ShowErroeMessage(myBojayClass.strErrorMessage)
                return -1
            else:
                self.ui.textEditPLCVer.setText(str(ret))
                return 0
        except Exception as e:
            self.ShowErroeMessage('ReadPlcVersion except %s' % e)
            return -1

    #*********************************************************************************#
    def actionStartTest(self):
        # #print 'actionStartTest'
        try:
            # ret = goectl.GetSensorStatus(goectl.RUNPatternSensor)
            # if ret == 0:
            #     tkMessageBox.showinfo("Error", "stimpad mode, not allowed to run pattern!!")
            #     #print 'stimpad mode, not allowed to run pattern!!'
            #     return
            # goectl.DrawCicleFlag(True)
            # err = goectl.BojayDutStartTest()
            # if(err != 0):
            #     tkMessageBox.showinfo("Error", goectl.GetErrorMessage())

            ret = myBojayClass.SignalReset(20)
            if ret != 0:
                self.ShowErroeMessage("Error", "SignalReset error")
                return
            Move_list = [[83,22,16],[95,33,20],[85,55,12],[95,79,20],[83,89,16]]
            count = self.ui.textEditBurnTimes.toPlainText()
            if count == '':
                self.ShowErroeMessage('please input the burnin counts')
                return -1

            intTimes = int(count)
            for i in range(intTimes):
                ret = myBojayClass.Set_CylindeFunction(myBojayClass.Cylinder_IN)
                if ret != 0:
                    self.ShowErroeMessage("Error", "Set_CylindeFunction error")
                    return

                ret = myBojayClass.DCLockandUnlock(myBojayClass.DCLock)
                if ret != 0:
                    self.ShowErroeMessage("Error", "DCLockandUnlock error")
                    return

                ret = myBojayClass.USBLockandUnlock(myBojayClass.USBLock)
                if ret != 0:
                    self.ShowErroeMessage("Error", "USBLockandUnlockerror")
                    return



                ret = myBojayClass.MoveToCoordinates(myBojayClass.X_axis, 87, 20)
                if ret != 0:
                    self.ShowErroeMessage("Error", "MoveToCoordinates error")
                    return


                ret = myBojayClass.MoveToCoordinates(myBojayClass.Y_axis, 55, 20)
                if ret != 0:
                    self.ShowErroeMessage("Error", "MoveToCoordinates error")
                    return

                ret = myBojayClass.MoveToCoordinates(myBojayClass.Z_axis, 20, 20)
                if ret != 0:
                    self.ShowErroeMessage("Error", "MoveToCoordinates error")
                    return

                ret = myBojayClass.PushPinDown(myBojayClass.Pin1)
                if ret != 0:
                    self.ShowErroeMessage("Error", "PushPinDown error")
                    return
                time.sleep(1)
                ret = myBojayClass.LiftPinUp(myBojayClass.Pin1)
                if ret != 0:
                    self.ShowErroeMessage("Error", "PushPinDown error")
                    return
                time.sleep(1)


                for i in range(0,5,1):
                    ret = myBojayClass.MoveToCoordinates(myBojayClass.Z_axis, 0, 20)
                    if ret != 0:
                        self.ShowErroeMessage("Error", "MoveToCoordinates error")
                        return

                    ret = myBojayClass.MoveToCoordinates(myBojayClass.X_axis, Move_list[i][0], 20)
                    if ret != 0:
                        self.ShowErroeMessage("Error", "MoveToCoordinates error")
                        return

                    ret = myBojayClass.MoveToCoordinates(myBojayClass.Y_axis, Move_list[i][1], 20)
                    if ret != 0:
                        self.ShowErroeMessage("Error", "MoveToCoordinates error")
                        return

                    ret = myBojayClass.MoveToCoordinates(myBojayClass.Z_axis, Move_list[i][2], 20)
                    if ret != 0:
                        self.ShowErroeMessage("Error", "MoveToCoordinates error")
                        return


                    ret = myBojayClass.PushPinDown(myBojayClass.Pin2)
                    if ret != 0:
                        self.ShowErroeMessage("Error", "PushPinDown error")
                        return

                    time.sleep(2)

                    ret = myBojayClass.LiftPinUp(myBojayClass.Pin2)
                    if ret != 0:
                        self.ShowErroeMessage("Error", "PushPinDown error")
                        return
                    time.sleep(2)


                ret = myBojayClass.MoveToCoordinates(myBojayClass.Z_axis, 0, 20)
                if ret != 0:
                    self.ShowErroeMessage("Error", "MoveToCoordinates error")
                    return


                # ret = goectl.DCLockandUnlock(goectl.DCUnlock)
                # if ret != 0:
                #     tkMessageBox.showinfo("Error", "DCLockandUnlock error")
                #     return
                #
                # ret = goectl.USBLockandUnlock(goectl.USBUnlock)
                # if ret != 0:
                #     tkMessageBox.showinfo("Error", "USBLockandUnlockerror")
                #     return

                ret = myBojayClass.SignalReset(20)
                if ret != 0:
                    self.ShowErroeMessage("Error", "SignalReset error")
                    return

                # ret = goectl.Set_CylindeFunction(goectl.Cylinder_OUT)
                # if ret != 0:
                #     tkMessageBox.showinfo("Error", "Set_CylindeFunction error")
                #     return


        except:
            self.ShowErroeMessage("Error", "actionStartTest error")
    # *********************************************************************************#





app = QtWidgets.QApplication(sys.argv)
myTonyFrame = TonyFrame()
myTonyFrame.show()
myTonyFrame.exec_()
