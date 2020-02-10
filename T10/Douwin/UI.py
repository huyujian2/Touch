# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UI.ui'
#
# Created: Fri Jan 11 10:41:56 2019
#      by: PyQt5 UI code generator 5.3.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_DemoTemperature(object):
    def setupUi(self, DemoTemperature):
        DemoTemperature.setObjectName("DemoTemperature")
        DemoTemperature.resize(638, 283)
        self.pushButtonOpenPort = QtWidgets.QPushButton(DemoTemperature)
        self.pushButtonOpenPort.setGeometry(QtCore.QRect(20, 10, 101, 31))
        self.pushButtonOpenPort.setStyleSheet("")
        self.pushButtonOpenPort.setObjectName("pushButtonOpenPort")
        self.pushButtonClosePort = QtWidgets.QPushButton(DemoTemperature)
        self.pushButtonClosePort.setGeometry(QtCore.QRect(510, 10, 101, 31))
        self.pushButtonClosePort.setStyleSheet("")
        self.pushButtonClosePort.setObjectName("pushButtonClosePort")
        self.groupBoxControlArea = QtWidgets.QGroupBox(DemoTemperature)
        self.groupBoxControlArea.setGeometry(QtCore.QRect(10, 50, 271, 151))
        self.groupBoxControlArea.setStyleSheet("")
        self.groupBoxControlArea.setObjectName("groupBoxControlArea")
        self.pushButtonStart = QtWidgets.QPushButton(self.groupBoxControlArea)
        self.pushButtonStart.setGeometry(QtCore.QRect(10, 40, 101, 31))
        self.pushButtonStart.setObjectName("pushButtonStart")
        self.pushButtonStop = QtWidgets.QPushButton(self.groupBoxControlArea)
        self.pushButtonStop.setGeometry(QtCore.QRect(10, 90, 101, 31))
        self.pushButtonStop.setObjectName("pushButtonStop")
        self.pushButtonDeviceStop = QtWidgets.QPushButton(self.groupBoxControlArea)
        self.pushButtonDeviceStop.setGeometry(QtCore.QRect(150, 40, 101, 31))
        self.pushButtonDeviceStop.setObjectName("pushButtonDeviceStop")
        self.pushButtonDeviceContinue = QtWidgets.QPushButton(self.groupBoxControlArea)
        self.pushButtonDeviceContinue.setGeometry(QtCore.QRect(150, 90, 101, 31))
        self.pushButtonDeviceContinue.setObjectName("pushButtonDeviceContinue")
        self.line = QtWidgets.QFrame(self.groupBoxControlArea)
        self.line.setGeometry(QtCore.QRect(120, 20, 20, 130))
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.groupBoxShow = QtWidgets.QGroupBox(DemoTemperature)
        self.groupBoxShow.setGeometry(QtCore.QRect(299, 49, 321, 201))
        self.groupBoxShow.setObjectName("groupBoxShow")
        self.pushButtonGetCurrentTemp = QtWidgets.QPushButton(self.groupBoxShow)
        self.pushButtonGetCurrentTemp.setGeometry(QtCore.QRect(20, 30, 141, 31))
        self.pushButtonGetCurrentTemp.setObjectName("pushButtonGetCurrentTemp")
        self.pushButtonSetAimsTemp = QtWidgets.QPushButton(self.groupBoxShow)
        self.pushButtonSetAimsTemp.setGeometry(QtCore.QRect(20, 90, 141, 31))
        self.pushButtonSetAimsTemp.setObjectName("pushButtonSetAimsTemp")
        self.pushButtonGetAimsTemp = QtWidgets.QPushButton(self.groupBoxShow)
        self.pushButtonGetAimsTemp.setGeometry(QtCore.QRect(20, 150, 141, 31))
        self.pushButtonGetAimsTemp.setObjectName("pushButtonGetAimsTemp")
        self.plainTextEditGetCurrentTemp = QtWidgets.QPlainTextEdit(self.groupBoxShow)
        self.plainTextEditGetCurrentTemp.setGeometry(QtCore.QRect(190, 30, 121, 31))
        self.plainTextEditGetCurrentTemp.setObjectName("plainTextEditGetCurrentTemp")
        self.plainTextEditSetAimsTemp = QtWidgets.QPlainTextEdit(self.groupBoxShow)
        self.plainTextEditSetAimsTemp.setGeometry(QtCore.QRect(190, 90, 121, 31))
        self.plainTextEditSetAimsTemp.setObjectName("plainTextEditSetAimsTemp")
        self.plainTextEditGetAimsTemp = QtWidgets.QPlainTextEdit(self.groupBoxShow)
        self.plainTextEditGetAimsTemp.setGeometry(QtCore.QRect(190, 150, 121, 31))
        self.plainTextEditGetAimsTemp.setObjectName("plainTextEditGetAimsTemp")

        self.retranslateUi(DemoTemperature)
        QtCore.QMetaObject.connectSlotsByName(DemoTemperature)

    def retranslateUi(self, DemoTemperature):
        _translate = QtCore.QCoreApplication.translate
        DemoTemperature.setWindowTitle(_translate("DemoTemperature", "Douwin"))
        self.pushButtonOpenPort.setText(_translate("DemoTemperature", "OpenPort"))
        self.pushButtonClosePort.setText(_translate("DemoTemperature", "ClosePort"))
        self.groupBoxControlArea.setTitle(_translate("DemoTemperature", "ControlArea"))
        self.pushButtonStart.setText(_translate("DemoTemperature", "Start"))
        self.pushButtonStop.setText(_translate("DemoTemperature", "Stop"))
        self.pushButtonDeviceStop.setText(_translate("DemoTemperature", "DeviceStop"))
        self.pushButtonDeviceContinue.setText(_translate("DemoTemperature", "DeviceContinue"))
        self.groupBoxShow.setTitle(_translate("DemoTemperature", "Get/Set"))
        self.pushButtonGetCurrentTemp.setText(_translate("DemoTemperature", "GetCurrentTemp"))
        self.pushButtonSetAimsTemp.setText(_translate("DemoTemperature", "SetAimsTemp"))
        self.pushButtonGetAimsTemp.setText(_translate("DemoTemperature", "GetAimsTemp"))

