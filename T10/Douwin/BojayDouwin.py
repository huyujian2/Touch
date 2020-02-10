from PyQt5 import QtCore,QtGui,QtWidgets
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QDialog,QMessageBox
import sys
import os
import serial
from serial import *

from UI import *
from DouwinAPI import *
goectl = TempControl()



class TonyFrame(QDialog):

    # **************************************************************#
    #initial function
    def __init__(self, parent=None):
        try:
            super(TonyFrame,self).__init__(parent)
            self.ui = Ui_DemoTemperature()
            self.ui.setupUi(self)

            #pushButtonOpenPort
            self.ui.pushButtonOpenPort.clicked.connect(self.OpenPort)

            #pushButtonClosePort
            self.ui.pushButtonClosePort.clicked.connect(self.ClosePort)

            #Start
            self.ui.pushButtonStart.clicked.connect(self.actionStart)

            #Stop
            self.ui.pushButtonStop.clicked.connect(self.actionStop)

            #DeviceStop
            self.ui.pushButtonDeviceStop.clicked.connect(self.actionDeviceStop)

            #DeviceContinue
            self.ui.pushButtonDeviceContinue.clicked.connect(self.actionDeviceContinue)

            #GetCurrentTemp
            self.ui.pushButtonGetCurrentTemp.clicked.connect(self.actionGetCurrentTemp)

            #SetAimsTemp
            self.ui.pushButtonSetAimsTemp.clicked.connect(self.actionSetAimsTemp)

            #GetAimsTemp
            self.ui.pushButtonGetAimsTemp.clicked.connect(self.actionGetAimsTemp)

            self.ui.pushButtonOpenPort.setEnabled(True)
            self.ui.pushButtonClosePort.setEnabled(False)
            self.ui.pushButtonStart.setEnabled(False)
            self.ui.pushButtonStop.setEnabled(False)
            self.ui.pushButtonDeviceStop.setEnabled(False)
            self.ui.pushButtonDeviceContinue.setEnabled(False)

            self.ui.pushButtonGetCurrentTemp.setEnabled(False)
            self.ui.pushButtonSetAimsTemp.setEnabled(False)
            self.ui.pushButtonGetAimsTemp.setEnabled(False)
        except:
            self.ShowErroeMessage("__init__  except Fai")

    # **************************************************************#
    #show error message
    def ShowErroeMessage(self, message):
        try:
            myMessageBox = QMessageBox()
            myMessageBox.information(self, "Warning", message, myMessageBox.Ok)
            return 0
        except:
            self.ShowErroeMessage("ShowErroeMessage except Fail")
            return -1
    # **************************************************************#
    #actionOpenPort
    def OpenPort(self):
        try:
            print "actionOpenPort"
            err = goectl.OpenSerial("/dev/ttyUSB2")
            if(err == -1):
                self.ShowErroeMessage("actionOpenPort error")
                return

            self.ui.pushButtonOpenPort.setEnabled(False)
            self.ui.pushButtonClosePort.setEnabled(True)
            self.ui.pushButtonStart.setEnabled(True)
            self.ui.pushButtonStop.setEnabled(True)
            self.ui.pushButtonDeviceStop.setEnabled(True)
            self.ui.pushButtonDeviceContinue.setEnabled(True)

            self.ui.pushButtonGetCurrentTemp.setEnabled(True)
            self.ui.pushButtonSetAimsTemp.setEnabled(True)
            self.ui.pushButtonGetAimsTemp.setEnabled(True)

        except:
            self.ShowErroeMessage("actionOpenPort fail")
            return -1
    # **************************************************************#
    #actionClose
    def ClosePort(self):
        print "actionClosePort"
        try:
            err = goectl.CloseSerial()
            if(err != 0):
                self.ShowErroeMessage("actionClosePort error")
                return

            self.ui.pushButtonOpenPort.setEnabled(True)
            self.ui.pushButtonClosePort.setEnabled(False)
            self.ui.pushButtonStart.setEnabled(False)
            self.ui.pushButtonStop.setEnabled(False)
            self.ui.pushButtonDeviceStop.setEnabled(False)
            self.ui.pushButtonDeviceContinue.setEnabled(False)

            self.ui.pushButtonGetCurrentTemp.setEnabled(False)
            self.ui.pushButtonSetAimsTemp.setEnabled(False)
            self.ui.pushButtonGetAimsTemp.setEnabled(False)

        except:
            self.ShowErroeMessage("actionClosePort fail")
            return -1
    # **************************************************************#
    def actionStart(self):
        try:
            ret = goectl.Start_Douwin()
            if(ret != 0):
                self.ShowErroeMessage("actionStart error")
                return
        except:
            self.ShowErroeMessage("actionStart fail")
            return -1
    # **************************************************************#
    def actionStop(self):
        try:
            ret = goectl.Stop_Douwin()
            if(ret != 0):
                self.ShowErroeMessage("actionStop error")
                return
        except:
            self.ShowErroeMessage("actionStop fail")
            return -1
    # **************************************************************#
    def actionDeviceStop(self):
        try:
            ret = goectl.DeviceStop_Douwin()
            if(ret != 0):
                self.ShowErroeMessage("actionDeviceStop error")
                return
        except:
            self.ShowErroeMessage("actionDeviceStop fail")
            return -1
    # **************************************************************#
    def actionDeviceContinue(self):
        try:
            ret = goectl.DeviceContinue_Douwin()
            if(ret != 0):
                self.ShowErroeMessage("actionDeviceContinue error")
                return
        except:
            self.ShowErroeMessage("actionDeviceContinue fail")
            return -1
    # **************************************************************#
    def actionGetCurrentTemp(self):
        try:
            ret = goectl.GetCurrentTemp_Douwin()
            if(ret == -1):
                self.ShowErroeMessage("actionGetCurrentTemp error")
                return
            else:
                self.ui.plainTextEditGetCurrentTemp.setPlainText(str(ret))
        except:
            self.ShowErroeMessage("actionGetCurrentTemp fail")
            return -1
    # **************************************************************#
    def actionSetAimsTemp(self):
        try:
            SetTemp = self.ui.plainTextEditSetAimsTemp.toPlainText()
            ret = goectl.SetAimsTemp_Douwin(SetTemp)
            if(ret != 0):
                self.ShowErroeMessage("actionSetAimsTemp error")
                return
        except:
            self.ShowErroeMessage("actionSetAimsTemp fail")
            return -1
    # **************************************************************#
    def actionGetAimsTemp(self):
        try:
            ret = goectl.GetAimsTemp_Douwin()
            if(ret == -1):
                self.ShowErroeMessage("actionGetAimsTemp error")
                return
            else:
                self.ui.plainTextEditGetAimsTemp.setPlainText(str(ret))
        except:
            self.ShowErroeMessage("actionGetAimsTemp fail")
            return -1
    # **************************************************************#
app = QtWidgets.QApplication(sys.argv)
myTonyFrame = TonyFrame()
myTonyFrame.exec_()
exit(app.exec_())