#Tony modify : 2018-6-16
#add set max&min limit


from Tkinter import *
# import tkinter
import ttk
import os
import tkFont
import tkMessageBox
from GOEPLCControl import*
goectl=GOEControlClass()

root = Tk()
var_com = StringVar()

def change_com_port(*args):
    try:
        goectl.OpenSerial()
    except:
        tkMessageBox.showinfo("Error", "Invalid COM port.")


def ButtonState(state):
    if(state):
        buttonClose.configure(state ='active')#close serial port
        buttonGetVer.configure(state = 'active')
        buttonMinLimit.configure(state ='active')#get min limit
        buttonGetMaxLimit.configure(state ='active')#get max limit

        buttonIncrementx.configure(state ='active')#x axis step move
        buttonDecrementx.configure(state='active')#x axis step move
        buttonIncrementy.configure(state ='active')#y aixs step move
        buttonDecrementy.configure(state='active')#y axis step move
        buttonIncrementz.configure(state ='active')#z axis step move
        buttonDecrementz.configure(state='active')#z axis step move
        buttonGetPosition.configure(state='active')#get current position

        XbuttonSetSpeed.configure(state='active')#x speed set
        YbuttonSetSpeed.configure(state='active')#y speed set
        ZbuttonSetSpeed.configure(state='active')#z speed set

        buttonReset.configure(state='active')#reset
        buttonClose.configure(state='active')#close
        buttonGetVer.configure(state = 'active')



        XbuttonMove.configure(state='active')#draw circle
        YbuttonMove.configure(state='active')#draw reactangle
        ZbuttonMove.configure(state='active')#run pattern



        buttonB1Calibration.configure(state='active')#B1Calibration



        buttonDU1Lock.configure(state='active')#DU1 lock
        buttonDU2Lock.configure(state='active')#DU2 lock

        
        buttonDU1Open.configure(state='active')#DU1 open
        buttonDU2Open.configure(state='active')#DU2 open

        buttonCylinderIN.config(state='active')
        buttonCylinderOut.config(state='active')

        buttonStartTest.configure(state='active')

        buttonDot.configure(state='active')


       #add new buttons
        buttonSetXMaxLimit.configure(state='active')
        buttonSetXMinLimit.configure(state='active')
        buttonSetYMaxLimit.configure(state='active')
        buttonSetYMinLimit.configure(state='active')
        buttonSetZMaxLimit.configure(state='active')
        buttonSetZMinLimit.configure(state='active')

        buttonCloseLightcurtain.configure(state='active')
        buttonOpenLightcurtain.configure(state= 'active')
        buttonFullScreenTest.config(state='active')

    else:
        buttonClose.configure(state ='disabled')#close serial port
        buttonMinLimit.configure(state ='disabled')#get min limit
        buttonGetMaxLimit.configure(state ='disabled')#get max limit

        buttonIncrementx.configure(state ='disabled')#x axis step move
        buttonDecrementx.configure(state='disabled')#x axis step move
        buttonIncrementy.configure(state ='disabled')#y aixs step move
        buttonDecrementy.configure(state='disabled')#y axis step move
        buttonIncrementz.configure(state ='disabled')#z axis step move
        buttonDecrementz.configure(state='disabled')#z axis step move
        buttonGetPosition.configure(state='disabled')#get current position

        XbuttonSetSpeed.configure(state='disabled')#x speed set
        YbuttonSetSpeed.configure(state='disabled')#y speed set
        ZbuttonSetSpeed.configure(state='disabled')#z speed set

        buttonReset.configure(state='disabled')#reset
        buttonClose.configure(state='disabled')#close

        XbuttonMove.configure(state='disabled')#draw circle
        YbuttonMove.configure(state='disabled')#draw reactangle
        ZbuttonMove.configure(state='disabled')#run pattern



        buttonB1Calibration.configure(state='disabled')#B1Calibration

        buttonGetVer.configure(state='disabled')
        # buttonGetButtons.configure(state = 'disabled')

        buttonDU1Lock.configure(state='disabled')#DU1 lock
        buttonDU2Lock.configure(state='disabled')#DU2 lock


        buttonDU1Open.configure(state='disabled')#DU1 open
        buttonDU2Open.configure(state='disabled')#DU2 open


        # buttonAlarmbuzzer.configure(state='disabled') #Alarmbuzzer
        # buttonAlarmbuzzerOff.configure(state='disabled') #Alarmbuzzer off

        # buttonFinger#printUP.configure(state='disabled')#buttonFinger#print up
        # buttonFinger#printDown.configure(state='disabled')#buttonFinger#print down

        buttonCylinderIN.config(state='disabled')
        buttonCylinderOut.config(state='disabled')

        buttonStartTest.configure(state='disabled')
        # buttonEndTest.configure(state='disabled')
        buttonReset.configure(state='disabled')

        buttonDot.configure(state='disabled')

        # add new buttons
        buttonSetXMaxLimit.configure(state='disabled')
        buttonSetXMinLimit.configure(state='disabled')
        buttonSetYMaxLimit.configure(state='disabled')
        buttonSetYMinLimit.configure(state='disabled')
        buttonSetZMaxLimit.configure(state='disabled')
        buttonSetZMinLimit.configure(state='disabled')
        buttonFullScreenTest.config(state='disabled')

        buttonCloseLightcurtain.configure(state='disabled')
        buttonOpenLightcurtain.configure(state='disabled')
        # buttonSetPassword.config(state='disable')
def actionOPenPort():

    try:
        err = goectl.OpenSerial()
        if(err == -1):
            tkMessageBox.showinfo("Error", "actionOPenPort fail")
            return
        ButtonState(True)
        buttonOpenPort.configure(state='disabled')
        #UpdateSpeed()
    except :
        tkMessageBox.showinfo("Error", "actionOPenPort fail")
#Function 1
#*********************************************************************************#
def UpdateSpeed():
    try:
        # get speed
        xSpeed = goectl.GetSpeed(goectl.X_axis)
        if (xSpeed != 0):
            tkMessageBox.showinfo("Error", goectl.GetErrorMessage())
        else:
            varXSpeed.set(xSpeed)
        ySpeed = goectl.GetSpeed(goectl.Y_axis)
        if (ySpeed != 0):
            tkMessageBox.showinfo("Error", goectl.GetErrorMessage())
        else:
            varYSpeed.set(ySpeed)
        zSpeed = goectl.GetSpeed(goectl.Z_axis)
        if (zSpeed != 0):
            tkMessageBox.showinfo("Error", goectl.GetErrorMessage())
        else:
            varZSpeed.set(zSpeed)
    except:
        tkMessageBox.showinfo("Error", "UpdateSpeed fail")
# *********************************************************************************#


#Function 2
#*********************************************************************************#
def actionReset():
    try:
        err = goectl.SignalReset(3)
        time.sleep(1)
		# OUT = goectl.Set_CylindeFunctionPack5(goectl.Cylinder_OPEN)
        OUT = goectl.Set_CylindeFunctionPack5(goectl.Cylinder_OPEN)
        if(err != 0):
            tkMessageBox.showinfo("Error", goectl.strErrorMessage)
    except:
        tkMessageBox.showinfo("Error", "actionReset fail")
#*********************************************************************************#


#*********************************************************************************#
def actionEnableUSBSensor():
    try:
        goectl.SetUSBSensorFlag(False)
    except:
        tkMessageBox.showinfo("Error", "actionEnableUSBSensor fail")
#*********************************************************************************#


#*********************************************************************************#
def actionDisableUSBSensor():
    try:
        goectl.SetUSBSensorFlag(True)
    except:
        tkMessageBox.showinfo("Error", "actionDisableUSBSensor fail")
#*********************************************************************************#

#*********************************************************************************#
def actionEnablePowerSource():
    try:
        goectl.EnablePowerSource(True)
    except:
        tkMessageBox.showinfo("Error", "actionEnablePowerSource fail")
#*********************************************************************************#


#*********************************************************************************#
def actionDisablePowerSource():
    try:
        goectl.EnablePowerSource(False)
    except:
        tkMessageBox.showinfo("Error", "actionDisablePowerSource fail")
#*********************************************************************************#

#*********************************************************************************#
def actionDot():
    try:
        xPoint = varXCoordinateEntry.get()
        if xPoint.__len__() < 1:
            tkMessageBox.showinfo("Error", "Please input x coordinate")
            return -1

        yPoint = varYCoordinateEntry.get()
        if yPoint.__len__() < 1:
            tkMessageBox.showinfo("Error", "Please input y coordinate")
            return -1

        zPoint = varZCoordinateEntry.get()
        if zPoint.__len__() < 1:
            tkMessageBox.showinfo("Error", "Please input z coordinate")
            return -1

        if(str(varDotEntry.get()).__len__() < 1):
            tkMessageBox.showinfo("Error", "actionDot error")
            return
        err = goectl.DotFunction(float(xPoint),float(yPoint),float(zPoint),int(varDotEntry.get()))
        if(err != 0):
            tkMessageBox.showinfo("Error", "actionDot error")
    except:
        tkMessageBox.showinfo("Error", "actionReset fail")
#*********************************************************************************#


#*********************************************************************************#
def actionAlarmbuzzer():
    try:
        err = goectl.AlarmBuzzer(goectl.Alarm_On)
        if(err != 0):
            tkMessageBox.showinfo("Error", "actionAlarmbuzzer error")
    except:
        tkMessageBox.showinfo("Error", "actionAlarmbuzzer fail")
#*********************************************************************************#


#*********************************************************************************#
def actionAlarmbuzzerOff():
    try:
        err = goectl.AlarmBuzzer(goectl.Alarm_Off)
        if(err != 0):
            tkMessageBox.showinfo("Error", "actionAlarmbuzzerOff error")
    except:
        tkMessageBox.showinfo("Error", "actionAlarmbuzzerOff fail")
#*********************************************************************************#



#Function 3
#*********************************************************************************#
def actionClose():
    #print ('actionClose')
    try:
        err = goectl.CloseSerial()
        if(err != 0):
            tkMessageBox.showinfo("Error", goectl.GetErrorMessage())
        ButtonState(False)
        buttonOpenPort.configure(state='active')
    except :
        tkMessageBox.showinfo("Error", "Close serial port fail")
# *********************************************************************************#

#*********************************************************************************#
def actionGetVer():
    #print ('actionGetVersion')
    try:
        ver = goectl.GetVer()
        if(ver != 0):
            tkMessageBox.showinfo("Version", ver)
            varversion.set(ver)
        # ButtonState(False)
        # buttonOpenPort.configure(state='active')
    except:
        tkMessageBox.showinfo("Error", "Getversion fail")
# *********************************************************************************#


#*********************************************************************************#
def actionGetButtons():
    #print ('actionGetButtonStatus')
    ret = -1
    try:
        ret = goectl.StartButtonsTriggered(goectl.StartButtonsTrigger)
        if(ret == 1):
            tkMessageBox.showinfo("Buttons Triggered","Buttons Triggered")
        elif(ret == 0):
            tkMessageBox.showinfo("Start", "Buttons donot triggered")
            # ButtonState(False)
            # buttonOpenPort.configure(state='active')
    except:
        tkMessageBox.showinfo("Exception", "Error: Buttons donot triggered")
# *********************************************************************************#

#*********************************************************************************#
def actionCylinderLock():
    #print ('actionCylinderLock')
    try:
        err = goectl.Set_CylindeFunction(goectl.Cylinder_LOCK)
        if(err != 0):
            tkMessageBox.showinfo("Error", goectl.GetErrorMessage())
    except:
        tkMessageBox.showinfo("Error", "actionCylinderLock error")


def actionCylinderLock2():
    #print ('actionCylinderLock')
    try:
        err = goectl.Set_CylindeFunctionPack2(goectl.Cylinder_LOCK)
        if(err != 0):
            tkMessageBox.showinfo("Error", goectl.GetErrorMessage())
    except:
        tkMessageBox.showinfo("Error", "actionCylinderLock error")


def actionCylinderLock3():
    #print ('actionCylinderLock')
    try:
        err = goectl.Set_CylindeFunctionPack3(goectl.Cylinder_LOCK)
        if(err != 0):
            tkMessageBox.showinfo("Error", goectl.GetErrorMessage())
    except:
        tkMessageBox.showinfo("Error", "actionCylinderLock error")


def actionCylinderLock4():
    #print ('actionCylinderLock')
    try:
        err = goectl.Set_CylindeFunctionPack4(goectl.Cylinder_LOCK)
        if(err != 0):
            tkMessageBox.showinfo("Error", goectl.GetErrorMessage())
    except:
        tkMessageBox.showinfo("Error", "actionCylinderLock error")


def actionCylinderLock5():
    try:
        err = goectl.Set_CylindeFunctionPack5(goectl.Cylinder_LOCK)
        if(err != 0):
            tkMessageBox.showinfo("Error", goectl.GetErrorMessage())
    except:
        tkMessageBox.showinfo("Error", "actionCylinderLock error")
# *********************************************************************************#


#*********************************************************************************#
def actionCylinderOpen():
    # #print 'actionCylinderOpen'
    try:
        err = goectl.Set_CylindeFunction(goectl.Cylinder_OPEN)
        if(err != 0):
            tkMessageBox.showinfo("Error", goectl.GetErrorMessage())
    except:
        tkMessageBox.showinfo("Error", "actionCylinderOpen fail")


def actionCylinderOpen2():
    # #print 'actionCylinderOpen'
    try:
        err = goectl.Set_CylindeFunctionPack2(goectl.Cylinder_OPEN)
        if(err != 0):
            tkMessageBox.showinfo("Error", goectl.GetErrorMessage())
    except:
        tkMessageBox.showinfo("Error", "actionCylinderOpen fail")


def actionCylinderOpen3():
    # #print 'actionCylinderOpen'
    try:
        err = goectl.Set_CylindeFunctionPack3(goectl.Cylinder_OPEN)
        if(err != 0):
            tkMessageBox.showinfo("Error", goectl.GetErrorMessage())
    except:
        tkMessageBox.showinfo("Error", "actionCylinderOpen fail")


def actionCylinderOpen4():
    # #print 'actionCylinderOpen'
    try:
        err = goectl.Set_CylindeFunctionPack4(goectl.Cylinder_OPEN)
        if(err != 0):
            tkMessageBox.showinfo("Error", goectl.GetErrorMessage())
    except:
        tkMessageBox.showinfo("Error", "actionCylinderOpen fail")


def actionCylinderOpen5():
    # #print 'actionCylinderOpen'
    try:
        err = goectl.Set_CylindeFunctionPack5(goectl.Cylinder_OPEN)
        if(err != 0):
            tkMessageBox.showinfo("Error", goectl.GetErrorMessage())
    except:
        tkMessageBox.showinfo("Error", "actionCylinderOpen fail")
# *********************************************************************************#



#*********************************************************************************#
def actionStartTest():
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

        ret = goectl.SignalReset(20)
        if ret != 0:
            tkMessageBox.showinfo("Error", "SignalReset error")
            return
        Move_list = [[83,22,16],[95,33,20],[85,55,12],[95,79,20],[83,89,16]]
        for i in range(100):
            ret = goectl.Set_CylindeFunction(goectl.Cylinder_IN)
            if ret != 0:
                tkMessageBox.showinfo("Error", "Set_CylindeFunction error")
                return

            ret = goectl.DCLockandUnlock(goectl.DCLock)
            if ret != 0:
                tkMessageBox.showinfo("Error", "DCLockandUnlock error")
                return

            ret = goectl.USBLockandUnlock(goectl.USBLock)
            if ret != 0:
                tkMessageBox.showinfo("Error", "USBLockandUnlockerror")
                return



            ret = goectl.MoveToCoordinates(goectl.X_axis, 87, 20)
            if ret != 0:
                tkMessageBox.showinfo("Error", "MoveToCoordinates error")
                return


            ret = goectl.MoveToCoordinates(goectl.Y_axis, 55, 20)
            if ret != 0:
                tkMessageBox.showinfo("Error", "MoveToCoordinates error")
                return

            ret = goectl.MoveToCoordinates(goectl.Z_axis, 20, 20)
            if ret != 0:
                tkMessageBox.showinfo("Error", "MoveToCoordinates error")
                return

            ret = goectl.PushPinDown(goectl.Pin1)
            if ret != 0:
                tkMessageBox.showinfo("Error", "PushPinDown error")
                return
            time.sleep(1)
            ret = goectl.LiftPinUp(goectl.Pin1)
            if ret != 0:
                tkMessageBox.showinfo("Error", "PushPinDown error")
                return
            time.sleep(1)


            for i in range(0,5,1):
                ret = goectl.MoveToCoordinates(goectl.Z_axis, 0, 20)
                if ret != 0:
                    tkMessageBox.showinfo("Error", "MoveToCoordinates error")
                    return

                ret = goectl.MoveToCoordinates(goectl.X_axis, Move_list[i][0], 20)
                if ret != 0:
                    tkMessageBox.showinfo("Error", "MoveToCoordinates error")
                    return

                ret = goectl.MoveToCoordinates(goectl.Y_axis, Move_list[i][1], 20)
                if ret != 0:
                    tkMessageBox.showinfo("Error", "MoveToCoordinates error")
                    return

                ret = goectl.MoveToCoordinates(goectl.Z_axis, Move_list[i][2], 20)
                if ret != 0:
                    tkMessageBox.showinfo("Error", "MoveToCoordinates error")
                    return


                ret = goectl.PushPinDown(goectl.Pin2)
                if ret != 0:
                    tkMessageBox.showinfo("Error", "PushPinDown error")
                    return

                time.sleep(2)

                ret = goectl.LiftPinUp(goectl.Pin2)
                if ret != 0:
                    tkMessageBox.showinfo("Error", "PushPinDown error")
                    return
                time.sleep(2)


            ret = goectl.MoveToCoordinates(goectl.Z_axis, 0, 20)
            if ret != 0:
                tkMessageBox.showinfo("Error", "MoveToCoordinates error")
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

            ret = goectl.SignalReset(20)
            if ret != 0:
                tkMessageBox.showinfo("Error", "SignalReset error")
                return

            # ret = goectl.Set_CylindeFunction(goectl.Cylinder_OUT)
            # if ret != 0:
            #     tkMessageBox.showinfo("Error", "Set_CylindeFunction error")
            #     return


    except:
        tkMessageBox.showinfo("Error", "actionStartTest error")
# *********************************************************************************#


#*********************************************************************************#
def actionEndTest():
    # #print 'actionEndTest'
    try:
        err = goectl.BojayFFTEnd(True,True,True,True,True)
        if(err != 0):
            tkMessageBox.showinfo("Error", goectl.GetErrorMessage())
    except:
        tkMessageBox.showinfo("Error", "BojayFFTEnd error")
# *********************************************************************************#



#Function 4
#*********************************************************************************#
def actionDrawCircle():
    # #print 'actionDrawCircle'
    try:

        xPoint = varXCoordinateEntry.get()
        if xPoint.__le__() < 1:
            tkMessageBox.showinfo("Error", "Please input x coordinate")
            return -1

        yPoint = varYCoordinateEntry.get()
        if yPoint.__le__() < 1:
            tkMessageBox.showinfo("Error", "Please input y coordinate")
            return -1
        err = goectl.CreateCircle(float(xPoint),float(yPoint),8,2,0.5,3,goectl.XAxisMinLimit,goectl.XAxisMaxLimit,goectl.YAxisMinLimit,goectl.YAxisMaxLimit)
        if(err != 0):
            tkMessageBox.showinfo("Error", goectl.GetErrorMessage())
        else:
            tkMessageBox.showinfo("Finish", "Create pattern finish")
    except:
        tkMessageBox.showinfo("Error", "actionDrawCircle fail")

#*********************************************************************************#


#Function 5
# *********************************************************************************#
def actionDrawRectangle():
    # #print 'actionDrawRectangle'
    try:
        xPoint = varXCoordinateEntry.get()
        if xPoint.__le__() < 1:
            tkMessageBox.showinfo("Error", "Please input x coordinate")
            return -1

        yPoint = varYCoordinateEntry.get()
        if yPoint.__le__() < 1:
            tkMessageBox.showinfo("Error", "Please input y coordinate")
            return -1
        err = goectl.CreateRectangle(float(xPoint),float(yPoint),8,10,9,goectl.XAxisMinLimit,goectl.XAxisMaxLimit,goectl.YAxisMinLimit,goectl.YAxisMaxLimit)
        if(err != 0):
            tkMessageBox.showinfo("Error", goectl.GetErrorMessage())
        else:
            tkMessageBox.showinfo("Finish", "Create pattern finish")
    except:
        tkMessageBox.showinfo("Error", "actionDrawRectangle fail")


# *********************************************************************************#



#Function 6
# *********************************************************************************#
def B1actionCalibration():
    # #print 'buttonB1Calibration'
    try:
        ret = goectl.GetSensorStatus(goectl.RUNPatternSensor)
        if ret == 0:
            tkMessageBox.showinfo("Error", "stimpad mode, not allowed to run pattern!!")
            # #print 'stimpad mode, not allowed to run pattern!!'
            return
        err = goectl.CalibrationPosition("B1")
        if(err != 0):
            tkMessageBox.showinfo("Error", goectl.GetErrorMessage())
        else:
            tkMessageBox.showinfo("Finish", "Create pattern finish")
    except:
        tkMessageBox.showinfo("Error", "actionDrawRectangle fail")
# *********************************************************************************#

# *********************************************************************************#
def B11actionCalibration():
    # #print 'buttonB11Calibration'
    try:
        ret = goectl.GetSensorStatus(goectl.RUNPatternSensor)
        if ret == 1:
            tkMessageBox.showinfo("Error", "pattern mode, not allowed to run stimpad!!")
            # #print 'pattern mode, not allowed to run stimpad!!'
            return
        if (str(varsleeptimeEntry.get()).__len__() < 1):
            pauseSec = 1
        else:
            pauseSec = int(varsleeptimeEntry.get())
        err = goectl.BojayFulltest("B11",pauseSec)
        if(err != 0):
            tkMessageBox.showinfo("Error", goectl.GetErrorMessage())
        else:
            # sleep(st)
            goectl.MoveToCoordinates(goectl.Z_axis, 0, 10)
            sleep(0.5)
            goectl.MoveToCoordinates(goectl.X_axis, 0, 10)
            goectl.MoveToCoordinates(goectl.Y_axis,0,10)

            tkMessageBox.showinfo("Finish", "B11 stimpad finish")
    except:
        tkMessageBox.showinfo("Error", "B11 stimpad fail")
# *********************************************************************************#


# *********************************************************************************#
def B12actionCalibration():
    # #print 'buttonB12Calibration'
    try:
        ret = goectl.GetSensorStatus(goectl.RUNPatternSensor)
        if ret == 1:
            tkMessageBox.showinfo("Error", "pattern mode, not allowed to run stimpad!!")
            # #print 'pattern mode, not allowed to run stimpad!!'
            return
        if (str(varsleeptimeEntry.get()).__len__() < 1):
            pauseSec = 1
        else:
            pauseSec = int(varsleeptimeEntry.get())

        err = goectl.BojayFulltest("B12",pauseSec)
        if(err != 0):
            tkMessageBox.showinfo("Error", goectl.GetErrorMessage())
        else:
            # sleep(st)
            goectl.MoveToCoordinates(goectl.Z_axis, 0, 10)
            sleep(0.5)
            goectl.MoveToCoordinates(goectl.X_axis, 0, 10)
            goectl.MoveToCoordinates(goectl.Y_axis, 0, 10)
            tkMessageBox.showinfo("Finish", "B12 stimpad finish")
    except:
        tkMessageBox.showinfo("Error", "B12 stimpad fail")
# *********************************************************************************#

# *********************************************************************************#
def C11actionCalibration():
    # #print 'buttonC11Calibration'
    try:
        ret = goectl.GetSensorStatus(goectl.RUNPatternSensor)
        if ret == 1:
            tkMessageBox.showinfo("Error", "pattern mode, not allowed to run stimpad!!")
            # #print 'pattern mode, not allowed to run stimpad!!'
            return
        if (str(varsleeptimeEntry.get()).__len__() < 1):
            pauseSec = 1
        else:
            pauseSec = int(varsleeptimeEntry.get())
        err = goectl.BojayFulltest("C11",pauseSec)
        if(err != 0):
            tkMessageBox.showinfo("Error", goectl.GetErrorMessage())
        else:
            # sleep(st)
            # ##print pauseSec
            goectl.MoveToCoordinates(goectl.Z_axis, 0, 10)
            sleep(0.5)
            goectl.MoveToCoordinates(goectl.X_axis, 0, 10)
            goectl.MoveToCoordinates(goectl.Y_axis, 0, 10)

            tkMessageBox.showinfo("Finish", "C11 stimpad finish")
    except:
        tkMessageBox.showinfo("Error", "C11 stimpad fail")
# *********************************************************************************#

# *********************************************************************************#
def C12actionCalibration():
    # ##print 'buttonC12Calibration'
    try:
        ret = goectl.GetSensorStatus(goectl.RUNPatternSensor)
        if ret == 1:
            tkMessageBox.showinfo("Error", "pattern mode, not allowed to run stimpad!!")
            # #print 'pattern mode, not allowed to run stimpad!!'
            return
        if (str(varsleeptimeEntry.get()).__len__() < 1):
            pauseSec = 1
        else:
            pauseSec = int(varsleeptimeEntry.get())
        err = goectl.BojayFulltest("C12",pauseSec)
        if(err != 0):
            tkMessageBox.showinfo("Error", goectl.GetErrorMessage())
        else:
            # sleep(st)
            # #print pauseSec
            goectl.MoveToCoordinates(goectl.Z_axis, 0, 10)
            sleep(0.5)
            goectl.MoveToCoordinates(goectl.X_axis, 0, 10)
            goectl.MoveToCoordinates(goectl.Y_axis, 0, 10)
            tkMessageBox.showinfo("Finish", "C12 stimpad finish")
    except:
        tkMessageBox.showinfo("Error", "C12 stimpad fail")
# *********************************************************************************#




# *********************************C1_calibration************************************************#
def C1actionCalibration():
    # #print 'buttonC1Calibration'
    try:
        ret = goectl.GetSensorStatus(goectl.RUNPatternSensor)
        if ret == 0:
            tkMessageBox.showinfo("Error", "stimpad mode, not allowed to run pattern!!")
            # #print 'stimpad mode, not allowed to run pattern!!'
            return
        err = goectl.CalibrationPosition("C1")
        if(err != 0):
            tkMessageBox.showinfo("Error", goectl.GetErrorMessage())
        else:
            tkMessageBox.showinfo("Finish", "Create pattern finish")
    except:
        tkMessageBox.showinfo("Error", "actionDrawRectangle fail")
# *********************************************************************************#


# *********************************V71_calibration************************************************#
def actionCalibration():
    # #print 'buttonCalibration'
    try:
        centerPoint = []
        err = goectl.CalibratePositionOfV71(centerPoint)
        if(err != 0):
            tkMessageBox.showinfo("Error", goectl.GetErrorMessage())
        else:
            tkMessageBox.showinfo("Finish", "Create pattern finish")
    except:
        tkMessageBox.showinfo("Error", "actionCalibration fail")
# *********************************************************************************#


#*********************************************************************************#
def actionRunPattern():
    # #print 'actionRunPattern'
    try:
        ret = goectl.GetSensorStatus(goectl.RUNPatternSensor)
        if ret == 0:
            tkMessageBox.showinfo("Error", "stimpad mode, not allowed to run pattern!!")
            # #print 'stimpad mode, not allowed to run pattern!!'
            return
        err = goectl.RunPattern()
        if(err != 0):
            tkMessageBox.showinfo("Error", goectl.GetErrorMessage())
    except:
        tkMessageBox.showinfo("Error", "actionRunPattern fail")

#*********************************************************************************#


#*********************************************************************************#
def actionFingerprintDown():
    # #print 'actionFinger#printDown'
    try:
        err = goectl.Set_CylindeFunction(goectl.Cylinder_DOWN)
        if(err != 0):
            tkMessageBox.showinfo("Error", goectl.GetErrorMessage())
    except:
        tkMessageBox.showinfo("Error", "actionFinger#printDown fail")

#*********************************************************************************#



#*********************************************************************************#
def actionFingerprintUp():
    # #print 'actionFinger#printUp'
    try:
        ret = goectl.GetSensorStatus(goectl.CylinderINSensor)
        if ret == 0:
            tkMessageBox.showinfo("Error", "Cylinder_IN first!!")
            # #print 'Cylinder_IN first!!'
            return
        err = goectl.Set_CylindeFunction(goectl.Cylinder_UP)
        if(err != 0):
            tkMessageBox.showinfo("Error", goectl.GetErrorMessage())
    except:
        tkMessageBox.showinfo("Error", "actionFinger#printUp fail")



#*********************************************************************************#




#*********************************************************************************#
def actionSet_DM_5V_ON():
    # #print 'actionSet_DM_5V_ON'
    try:
        err = goectl.Set_DM_5V_ONOFF(goectl.Set_DM_5V_ON)
        if(err != 0):
            tkMessageBox.showinfo("Error", goectl.GetErrorMessage())
    except:
        tkMessageBox.showinfo("Error", "actionSet_DM_5V_ON fail")


def actionSet_DM_5V_OFF():
    # #print 'actionSet_DM_5V_OFF'
    try:
        err = goectl.Set_DM_5V_ONOFF(goectl.Set_DM_5V_OFF)
        if (err != 0):
            tkMessageBox.showinfo("Error", goectl.GetErrorMessage())
    except:
        tkMessageBox.showinfo("Error", "actionSet_DM_5V_OFF fail")

#*********************************************************************************#



#*********************************************************************************#
def actionCylinderIN():
    # #print 'actionCylinderIN'
    try:
        err = goectl.Set_CylindeFunction(goectl.Cylinder_IN)
        if(err != 0):
            goectl.ResetTray(goectl.Cylinder_IN)
            tkMessageBox.showinfo("Error", goectl.GetErrorMessage())
    except:
        tkMessageBox.showinfo("Error", "actionCylinderIN fail")


def actionCylinderOUT():
    # #print 'actionCylinderOUT'
    try:
        err = goectl.Set_CylindeFunction(goectl.Cylinder_OUT)
        if (err != 0):
            goectl.ResetTray(goectl.Cylinder_OUT)
            tkMessageBox.showinfo("Error", goectl.GetErrorMessage())
    except:
        tkMessageBox.showinfo("Error", "actionCylinderOUT fail")

#*********************************************************************************#


#*********************************************************************************#
def actionSet_LED_STATE():
    # #print 'actionSet_LED_STATE'
    try:
        LEDStr = varLEDStateEntry.get()
        myStr = []
        myStr = LEDStr.split(",")
        if(len(myStr) < 2):
            tkMessageBox.showinfo("Error", "Input parameter format is not correct")
            return
        DUT = int(myStr[0])
        strColor = str(myStr[1])
        strColor = strColor.lower()
        if(DUT == 1):
            DUT = goectl.DUT1
        elif(DUT == 2):
            DUT = goectl.DUT2
        elif(DUT == 3):
            DUT = goectl.DUT3
        elif(DUT == 4):
            DUT = goectl.DUT4
        if("yellowoff" in strColor):
            color = goectl.Yellow_OFF
        elif("yellowon" in strColor):
            color = goectl.Yellow_ON
        elif("redoff" in strColor):
            color = goectl.Red_OFF
        elif("redon" in strColor):
            color = goectl.Red_ON
        elif("greenoff" in strColor):
            color = goectl.Green_OFF
        elif("greenon" in strColor):
            color = goectl.Green_ON
        err = goectl.SetLedLightColor(DUT,color)
        if(err != 0):
            tkMessageBox.showinfo("Error", goectl.GetErrorMessage())
    except:
        tkMessageBox.showinfo("Error", "actionSet_LED_STATE fail")
# *********************************************************************************#

#*********************************************************************************#
def actionGet_Sensor_STATE():
    # #print 'actionGet_Sensor_STATE'
    try:
        command = str(varSensorStateEntry.get())
        if(command == "%01#RCP1X0018"):
            sensor = goectl.Sensor_X_Origin
        elif (command == "%01#RCP1X0019"):
            sensor = goectl.Sensor_X_Min
        elif (command == "%01#RCP1X001A"):
            sensor = goectl.Sensor_X_Max
        ret = goectl.GetSensorStatus(sensor)
        if(ret == -1):
            tkMessageBox.showinfo("Error", "actionGet_Sensor_STATE fail")
            return
        varSensorResultEntry.set(str(ret))
    except:
        tkMessageBox.showinfo("Error", "actionGet_Sensor_STATE fail")


#*********************************************************************************#



#*********************************************************************************#
"""
def actionSet_Steep():
    try:
        #print ("actionSet_Steep")
        strSetSteep = str(varSteepSetEntry.get())
        myStr = []
        myStr = strSetSteep.split(",")
        if(len(myStr) < 2):
            tkMessageBox.showinfo("Error", "Input parameter format is not correct")
            return
        if("x" in myStr[0]):
            axis =  goectl.X_axis
        elif("y" in myStr[0]):
            axis = goectl.Y_axis
        elif("z" in myStr[0]):
            axis = goectl.Z_axis
        else:
            tkMessageBox.showinfo("Error", "Input parameter format is not correct")
            return
        if("0.01" in myStr[1]):
            step = 0.01
        elif("0.1" in myStr[1]):
            step = 0.1
        elif("1" in myStr[1]):
            step = 1
        elif("5" in myStr[1]):
            step = 5
        else:
            tkMessageBox.showinfo("Error", "Input parameter format is not correct")
            return
        err = goectl.SetStepValue(axis,step)
        if(err == -1):
            tkMessageBox.showinfo("Error",goectl.GetErrorMessage())
            return
        else:
            ret = goectl.GetStepValue(axis)
            varSteepGetEntry.set(ret)
    except:
        tkMessageBox.showinfo("Error", "actionSet_Step fail")
"""

#USB Lock
def actionUSBLock():
    # #print 'actionUSBLock'
    try:
        err = goectl.USBLockandUnlock(goectl.USBLock)
        if(err != 0):
            tkMessageBox.showinfo("Error", goectl.GetErrorMessage())
    except:
        tkMessageBox.showinfo("Error", "actionUSBLock fail")

# USB UnLock
def actionUSBUnlock():
    # #print 'actionUSBUnlock'
    try:
        err = goectl.USBLockandUnlock(goectl.USBUnlock)
        if (err != 0):
            tkMessageBox.showinfo("Error", goectl.GetErrorMessage())
    except:
        tkMessageBox.showinfo("Error", "actionUSBUnLock fail")

#DC Lock
def actionDCLock():
    # #print 'actionDCLock'
    try:
        err = goectl.DCLockandUnlock(goectl.DCLock)
        if(err != 0):
            tkMessageBox.showinfo("Error", goectl.GetErrorMessage())
    except:
        tkMessageBox.showinfo("Error", "actionDCLock fail")

# DC UnLock
def actionDCUnlock():
    # #print 'actionDCUnlock'
    try:
        err = goectl.DCLockandUnlock(goectl.DCUnlock)
        if (err != 0):
            tkMessageBox.showinfo("Error", goectl.GetErrorMessage())
    except:
        tkMessageBox.showinfo("Error", "actionDCUnLock fail")




# *********************************************************************************#
#DU2 Lock
def actionDU2Lock():
    # #print 'actionDU2Lock'
    try:
        err = goectl.PushPinDown(goectl.Pin2)
        if(err != 0):
            tkMessageBox.showinfo("Error", goectl.GetErrorMessage())
    except:
        tkMessageBox.showinfo("Error", "actionDU2Lock fail")

# DU2 Lock
def actionDU1Lock():
    #print 'actionDU1Lock'
    try:
        err = goectl.PushPinDown(goectl.Pin1)
        if (err != 0):
            tkMessageBox.showinfo("Error", goectl.GetErrorMessage())
    except:
        tkMessageBox.showinfo("Error", "actionDU1Lock fail")

# DU3 Lock
def actionDU3Lock():
    #print 'actionDU3Lock'
    try:
        err = goectl.PushPinDown(goectl.Pin3)
        if (err != 0):
            tkMessageBox.showinfo("Error", goectl.GetErrorMessage())
    except:
        tkMessageBox.showinfo("Error", "actionDU3Lock fail")

# DU4 Lock
def actionDU4Lock():
    #print 'actionDU4Lock'
    try:
        err = goectl.DUTLcokOrOpen(goectl.DUT4,goectl.DUT_LOCK)
        if (err != 0):
            tkMessageBox.showinfo("Error", goectl.GetErrorMessage())
    except:
        tkMessageBox.showinfo("Error", "actionDU4Lock fail")

# DU2 Open
def actionDU2Open():
    #print 'actionDU2Open'
    try:
        err = goectl.LiftPinUp(goectl.Pin2)
        if (err != 0):
            tkMessageBox.showinfo("Error", goectl.GetErrorMessage())
    except:
        tkMessageBox.showinfo("Error", "actionDU2Open fail")

# DU1 Open
def actionDU1Open():
    #print 'actionDU1Open'
    try:
        err = goectl.LiftPinUp(goectl.Pin1)
        if (err != 0):
            tkMessageBox.showinfo("Error", goectl.GetErrorMessage())
    except:
        tkMessageBox.showinfo("Error", "actionDU1Open fail")

# DU3 Open
def actionDU3Open():
    #print 'actionDU3Open'
    try:
        err = goectl.LiftPinUp(goectl.Pin3)
        if (err != 0):
            tkMessageBox.showinfo("Error", goectl.GetErrorMessage())
    except:
        tkMessageBox.showinfo("Error", "actionDU3Open fail")

# DU4 Open
def actionDU4Open():
    #print 'actionDU4Open'
    try:
        err = goectl.DUTLcokOrOpen(goectl.DUT4, goectl.DUT_OPEN)
        if (err != 0):
            tkMessageBox.showinfo("Error", goectl.GetErrorMessage())
    except:
        tkMessageBox.showinfo("Error", "actionDU4Open fail")
#*********************************************************************************#




#************************************************************************************#
#Increment step
def XactionIncrement():
        #print 'actionIncrement'
        try:
            if (str(varXIncrement_step.get()).__len__() < 1):
                tkMessageBox.showinfo("Error", "You need to input the increment step vale")
            err = goectl.SetStepValue(goectl.X_axis, float(varXIncrement_step.get()))
            if (err == -1):
                tkMessageBox.showinfo("Error", goectl.GetErrorMessage())
                return
            err = goectl.MoveIncrement(goectl.X_axis)
            if (err == -1):
                tkMessageBox.showinfo("Error", goectl.GetErrorMessage())
                return
            GetPosition()
        except:
            tkMessageBox.showinfo("Error", "XactionIncrement fail")

#Decrement step move
def XactionDecrement():
    #print 'Decrement_step'
    try:
        if (str(varXDecrement_step.get()).__len__() < 1):
            tkMessageBox.showinfo("Error", "You need to input the decrement step vale")
        err = goectl.SetStepValue(goectl.X_axis, float(varXDecrement_step.get()))
        if (err == -1):
            tkMessageBox.showinfo("Error", goectl.GetErrorMessage())
            return
        err = goectl.MoveDecrement(goectl.X_axis)
        if (err == -1):
            tkMessageBox.showinfo("Error", goectl.GetErrorMessage())
            return
            GetPosition()
    except:
        tkMessageBox.showinfo("Error", "XactionDecrement fail")
# ************************************************************************************#



#************************************************************************************#
#Y Step
#Increment step
def YactionIncrement():
        #print 'YactionIncrement'
        try:
            if (str(varYIncrement_step.get()).__len__() < 1):
                tkMessageBox.showinfo("Error", "You need to input the increment step vale")
            err = goectl.SetStepValue(goectl.Y_axis, float(varYIncrement_step.get()))
            if (err == -1):
                tkMessageBox.showinfo("Error", goectl.GetErrorMessage())
                return
            err = goectl.MoveIncrement(goectl.Y_axis)
            if (err == -1):
                tkMessageBox.showinfo("Error", goectl.GetErrorMessage())
                return
                GetPosition()
        except:
            tkMessageBox.showinfo("Error", "YactionIncrement fail")

#Decrement step move
def YactionDecrement():
    #print 'YXactionDecrement'
    try:
        if (str(varYDecrement_step.get()).__len__() < 1):
            tkMessageBox.showinfo("Error", "You need to input the decrement step vale")
        err = goectl.SetStepValue(goectl.Y_axis, float(varYDecrement_step.get()))
        if (err == -1):
            tkMessageBox.showinfo("Error", goectl.GetErrorMessage())
            return
        err = goectl.MoveDecrement(goectl.Y_axis)
        if (err == -1):
            tkMessageBox.showinfo("Error", goectl.GetErrorMessage())
            return
            GetPosition()
    except:
        tkMessageBox.showinfo("Error", "YactionDecrement fail")
# ************************************************************************************#



#************************************************************************************#
#Y Step
#Increment step
def ZactionIncrement():
        #print 'ZactionIncrement'
        try:
            if (str(varZIncrement_step.get()).__len__() < 1):
                tkMessageBox.showinfo("Error", "You need to input the increment step vale")
            err = goectl.SetStepValue(goectl.Z_axis, float(varZIncrement_step.get()))
            if (err == -1):
                tkMessageBox.showinfo("Error", goectl.GetErrorMessage())
                return
            err = goectl.MoveIncrement(goectl.Z_axis)
            if (err == -1):
                tkMessageBox.showinfo("Error", goectl.GetErrorMessage())
                return
                GetPosition()
        except:
            tkMessageBox.showinfo("Error", "ZactionIncrement fail")

#Decrement step move
def ZactionDecrement():
    #print 'ZactionDecrement'
    try:
        if (str(ZDecrement_step.get()).__len__() < 1):
            tkMessageBox.showinfo("Error", "You need to input the decrement step vale")
        err = goectl.SetStepValue(goectl.Z_axis, float(ZDecrement_step.get()))
        if (err == -1):
            tkMessageBox.showinfo("Error", goectl.GetErrorMessage())
            return
        err = goectl.MoveDecrement(goectl.Z_axis)
        if (err == -1):
            tkMessageBox.showinfo("Error", goectl.GetErrorMessage())
            return
            GetPosition()
    except:
        tkMessageBox.showinfo("Error", "ZactionDecrement fail")
# ************************************************************************************#



# ************************************************************************************#
#Get max limit
def GetMaxLimit():
    #print 'Get max limit'
    try:
        xMaxLimit = goectl.GetLimit(goectl.X_axis, goectl.Max_limit)
        if(xMaxLimit == -1):
            tkMessageBox.showinfo("Error", goectl.GetErrorMessage())
            return

        yMaxLimit = goectl.GetLimit(goectl.Y_axis, goectl.Max_limit)
        if(yMaxLimit == -1):
            tkMessageBox.showinfo("Error", goectl.GetErrorMessage())
            return

        zMaxLimit = goectl.GetLimit(goectl.Z_axis, goectl.Max_limit)
        if(zMaxLimit == -1):
            tkMessageBox.showinfo("Error", goectl.GetErrorMessage())
            return

        varXMax_limit.set(str(xMaxLimit))
        varYMax_limit.set(str(yMaxLimit))
        varZMax_limit.set(str(zMaxLimit))
        return 0
    except:
        tkMessageBox.showinfo("Error", "Get max limit error")
        return 1
 # ************************************************************************************#



# ************************************************************************************#
# Get min limit
def GetMinLimit():
    #print 'Get min limit'
    try:
        xMinLimit = goectl.GetLimit(goectl.X_axis, goectl.Min_limit)
        if(xMinLimit == -1):
            tkMessageBox.showinfo("Error", goectl.GetErrorMessage())
            return
        yMinLimit = goectl.GetLimit(goectl.Y_axis, goectl.Min_limit)
        if(yMinLimit == -1):
            tkMessageBox.showinfo("Error", goectl.GetErrorMessage())
            return
        zMinLimit = goectl.GetLimit(goectl.Z_axis, goectl.Min_limit)
        # if(zMinLimit == -1):
        #     tkMessageBox.showinfo("Error", goectl.GetErrorMessage())
        #     return

        varXMin_limit.set(str(xMinLimit))
        varYMin_limit.set(str(yMinLimit))
        varZMin_limit.set(str(zMinLimit))
        return 0
    except:
        tkMessageBox.showinfo("Error", "Get min limit error")
        return 1
# ************************************************************************************#



# ************************************************************************************#
# Get position
def GetPosition():
    try:
        #print 'Get position'
        xPosition = goectl.GetCurrentCoordinates(goectl.X_axis)
        if(xPosition == -9999):
            tkMessageBox.showinfo("Error", goectl.GetErrorMessage())
            return
        yPosition = goectl.GetCurrentCoordinates(goectl.Y_axis)
        if(yPosition == -9999):
            tkMessageBox.showinfo("Error", goectl.GetErrorMessage())
            return
        zPosition = goectl.GetCurrentCoordinates(goectl.Z_axis)
        if(zPosition == -9999):
            tkMessageBox.showinfo("Error", goectl.GetErrorMessage())
            return

        varXPosition.set(xPosition)
        varYPosition.set(yPosition)
        varZPosition.set(zPosition)
        return 0
    except:
        tkMessageBox.showinfo("Error", "Get min limit error")
        return 1
# ************************************************************************************#



# ************************************************************************************#
def actionSetSpeedX():
    try:
        speedx = float(ent_speedx.get())
        err = goectl.SetSpeed(goectl.X_axis,speedx)
        if(err == -1):
            tkMessageBox.showinfo("Error", goectl.GetErrorMessage())
            return
        #UpdateSpeed()
    except:
        tkMessageBox.showinfo("Error", "actionSetSpeedX error")
# ************************************************************************************#


# ************************************************************************************#
def actionSetSpeedY():
    try:
        speedy = float(ent_speedy.get())
        err = goectl.SetSpeed(goectl.Y_axis,speedy)
        if(err == -1):
            tkMessageBox.showinfo("Error", goectl.GetErrorMessage())
            return
        #UpdateSpeed()
    except:
        tkMessageBox.showinfo("Error", "actionSetSpeedY error")
# ************************************************************************************#



# ************************************************************************************#
def actionSetSpeedZ():
    try:
        speedz = float(ent_speedz.get())
        err = goectl.SetSpeed(goectl.Z_axis,speedz)
        if(err == -1):
            tkMessageBox.showinfo("Error", goectl.GetErrorMessage())
            return
        #UpdateSpeed()
    except:
        tkMessageBox.showinfo("Error", "actionSetSpeedZ error")
# ************************************************************************************#



# ************************************************************************************#
def actionMoveX():
    try:
        if (str(coordinateX.get()).__len__() < 1):
            tkMessageBox.showinfo("Error", "You need to input the X  coordiante vale")
        coordinatex = float(coordinateX.get())
        err = goectl.MoveToCoordinates(goectl.X_axis,coordinatex,5)
        if(err != 0):
            tkMessageBox.showinfo("Error", goectl.GetErrorMessage())
    except:
        tkMessageBox.showinfo("Error", "actionMoveX error")
# ************************************************************************************#


# ************************************************************************************#
def actionOpenCurtain():
    try:
        err = goectl.SetLightCurtain(goectl.LightCurtainOn)
        if(err != 0):
            tkMessageBox.showinfo("Error", goectl.GetErrorMessage())
    except:
        tkMessageBox.showinfo("Error", "Open light curtain error")
# ************************************************************************************#


# ************************************************************************************#
def actionCloseCurtain():
    try:
        err = goectl.SetLightCurtain(goectl.LightCurtainOff)
        if(err != 0):
            tkMessageBox.showinfo("Error", goectl.GetErrorMessage())
    except:
        tkMessageBox.showinfo("Error", "Close light curtain error")
# ************************************************************************************#


# ************************************************************************************#
def actionMoveY():
    try:
        if (str(coordinateY.get()).__len__() < 1):
            tkMessageBox.showinfo("Error", "You need to input the Y  coordiante vale")
        coordinatey = float(coordinateY.get())
        err = goectl.MoveToCoordinates(goectl.Y_axis,coordinatey,5)
        if(err != 0):
            tkMessageBox.showinfo("Error", goectl.GetErrorMessage())
    except:
        tkMessageBox.showinfo("Error", "actionMoveY error")
# ************************************************************************************#


# ************************************************************************************#
def actionMoveZ():
    try:
        if (str(coordinateZ.get()).__len__() < 1):
            tkMessageBox.showinfo("Error", "You need to input the Z  coordiante vale")
        coordinatex = float(coordinateZ.get())
        err = goectl.MoveToCoordinates(goectl.Z_axis,coordinatex,5)

        if(err != 0):
            tkMessageBox.showinfo("Error", goectl.GetErrorMessage())
    except:
        tkMessageBox.showinfo("Error", "actionMoveZ error")
# ************************************************************************************#



# *********************************************************************************#
def actionSetXMaxLimit():
    try:
        #print("SetXMaxLimit")

        # check the password first
        Passwd = "bojay"
        strPassword = str(varPassword.get())
        # get local password
        # strPasswordPath = os.getcwd() + "/YourPasswd.txt"
        # LocalPassword = open(strPasswordPath, "r")
        # strAllLine = str(LocalPassword.readline())
        # #print(strAllLine)
        if (Passwd == strPassword):
            varPassword.set("bojay")
        else:
            tkMessageBox.showinfo("Error", "You need to input correct password")
            return

        value = varSetXMaxLimitEntry.get()
        ret = goectl.SetPLCLimit(goectl.X_axis,goectl.Max_limit,float(value))
        if ret != 0:
            tkMessageBox.showinfo("Error", "SetXMaxLimit fail")
        goectl.SaveLimitTXT("XAxisMaxLimit", value)
    except:
        tkMessageBox.showinfo("Error", "SetXMaxLimit error")


# def actionSetXMaxLimit():
#     try:
#         if(str(varSetXMaxLimit.get()).__len__() < 1):
#             tkMessageBox.showinfo("Error", "You need to input the x  max limit")

#         # check the password first
#         Passwd = "bojay"
#         # strPassword = str(varPassword.get())
#         # get local password
#         strPasswordPath = os.getcwd() + "/YourPasswd.txt"
#         LocalPassword = open(strPasswordPath, "r")
#         strAllLine = str(LocalPassword.readline())
#         #print(strAllLine)
#         #print type(strAllLine)
#         if (Passwd == strAllLine):
#             varPassword.set("bojay")
#         else:
#             tkMessageBox.showinfo("Error", "You need to input correct password")
#             return

#         ret = goectl.SetPLCLimit(goectl.X_axis,goectl.Max_limit,float(varSetXMaxLimitEntry.get()))
#         if ret != 0:
#             tkMessageBox.showinfo("Error", goectl.strErrorMessage)
#             return
#     except:
#         tkMessageBox.showinfo("Error", "SetXMaxLimit error")

# *********************************************************************************#
def actionSetXMinLimit():
    try:
        #print("SetXMinLimit")

        # check the password first
        Passwd = "bojay"
        strPassword = str(varPassword.get())
        # get local password
        # strPasswordPath = os.getcwd() + "/YourPasswd.txt"
        # LocalPassword = open(strPasswordPath, "r")
        # strAllLine = str(LocalPassword.readline())
        # #print(strAllLine)
        if (Passwd == strPassword):
            varPassword.set("bojay")
        else:
            tkMessageBox.showinfo("Error", "You need to input correct password")
            return

        value = varSetXMinLimitEntry.get()
        ret = goectl.SetPLCLimit(goectl.X_axis,goectl.Min_limit,float(value))
        if ret != 0:
            tkMessageBox.showinfo("Error", "SetXMinLimit fail")
        goectl.SaveLimitTXT("XAxisMinLimit", value)
    except:
        tkMessageBox.showinfo("Error", "SetXMinLimit error")


# def actionSetXMinLimit():
#     try:
#         if(str(varSetXMinLimit.get()).__len__() < 1):
#             tkMessageBox.showinfo("Error", "You need to input the x  min limit")

#         # check the password first
#         Passwd = "bojay"
#         # strPassword = str(varPassword.get())
#         # get local password
#         strPasswordPath = os.getcwd() + "\YourPasswd.txt"
#         LocalPassword = open(strPasswordPath, "r")
#         strAllLine = str(LocalPassword.readline())
#         #print(strAllLine)
#         if (Passwd == strAllLine):
#             varPassword.set("bojay")
#         else:
#             tkMessageBox.showinfo("Error", "You need to input correct password")
#             return

#         ret = goectl.SetPLCLimit(goectl.X_axis,goectl.Min_limit,float(varSetXMinLimitEntry.get()))
#         if ret != 0:
#             tkMessageBox.showinfo("Error", goectl.strErrorMessage)
#             return

#     	goectl.SaveLimitTXT("XAxisMinLimit", varSetXMinLimitEntry.get())
#     except:
#         tkMessageBox.showinfo("Error", "SetXMinLimit error")

# *********************************************************************************#
def actionSetYMaxLimit():
    try:
        #print("actionSetYMaxLimit")

        # check the password first
        Passwd = "bojay"
        strPassword = str(varPassword.get())
        # get local password
        # strPasswordPath = os.getcwd() + "/YourPasswd.txt"
        # LocalPassword = open(strPasswordPath, "r")
        # strAllLine = str(LocalPassword.readline())
        # #print(strAllLine)
        if (Passwd == strPassword):
            varPassword.set("bojay")
        else:
            tkMessageBox.showinfo("Error", "You need to input correct password")
            return

        value = varSetYMaxLimitEntry.get()
        ret = goectl.SetPLCLimit(goectl.Y_axis,goectl.Max_limit,float(value))
        if ret != 0:
            tkMessageBox.showinfo("Error", "actionSetYMaxLimit fail")
        goectl.SaveLimitTXT("YAxisMaxLimit", value)
    except:
        tkMessageBox.showinfo("Error", "actionSetYMaxLimit error")


# def actionSetYMaxLimit():
#     try:
#         if (str(varSetYMaxLimit.get()).__len__() < 1):
#             tkMessageBox.showinfo("Error", "You need to input the y  max limit")

#         # check the password first
#         Passwd = "bojay"
#         # strPassword = str(varPassword.get())
#         # get local password
#         strPasswordPath = os.getcwd() + "\YourPasswd.txt"
#         LocalPassword = open(strPasswordPath, "r")
#         strAllLine = str(LocalPassword.readline())
#         #print(strAllLine)
#         if (Passwd == strAllLine):
#             varPassword.set("bojay")
#         else:
#             tkMessageBox.showinfo("Error", "You need to input correct password")
#             return

#         ret = goectl.SetPLCLimit(goectl.Y_axis, goectl.Max_limit, float(varSetYMaxLimitEntry.get()))
#         if ret != 0:
#             tkMessageBox.showinfo("Error", goectl.strErrorMessage)
#             return
#     except:
#         tkMessageBox.showinfo("Error", "SetYMaxLimit error")


# *********************************************************************************#
def actionSetYMinLimit():
    try:
        #print("actionSetYMinLimit")

        # check the password first
        Passwd = "bojay"
        strPassword = str(varPassword.get())
        # get local password
        # strPasswordPath = os.getcwd() + "/YourPasswd.txt"
        # LocalPassword = open(strPasswordPath, "r")
        # strAllLine = str(LocalPassword.readline())
        # #print(strAllLine)
        if (Passwd == strPassword):
            varPassword.set("bojay")
        else:
            tkMessageBox.showinfo("Error", "You need to input correct password")
            return

        value = varSetYMinLimitEntry.get()
        ret = goectl.SetPLCLimit(goectl.Y_axis,goectl.Min_limit,float(value))
        if ret != 0:
            tkMessageBox.showinfo("Error", "actionSetYMinLimit fail")
        goectl.SaveLimitTXT("YAxisMinLimit", value)
    except:
        tkMessageBox.showinfo("Error", "actionSetYMinLimit error")


# def actionSetYMinLimit():
#     try:
#         if (str(varSetYMinLimit.get()).__len__() < 1):
#             tkMessageBox.showinfo("Error", "You need to input the Y  min limit")

#         # check the password first
#         Passwd = "bojay"
#         # strPassword = str(varPassword.get())
#         # get local password
#         strPasswordPath = os.getcwd() + "/YourPasswd.txt"
#         LocalPassword = open(strPasswordPath, "r")
#         strAllLine = str(LocalPassword.readline())
#         #print(strAllLine)
#         if (Passwd == strAllLine):
#             varPassword.set("bojay")
#         else:
#             tkMessageBox.showinfo("Error", "You need to input correct password")
#             return

#         ret = goectl.SetPLCLimit(goectl.Y_axis, goectl.Min_limit, float(varSetYMinLimitEntry.get()))
#         if ret != 0:
#             tkMessageBox.showinfo("Error", goectl.strErrorMessage)
#             return
#     except:
#         tkMessageBox.showinfo("Error", "SetYMinLimit error")


# *********************************************************************************#
def actionSetZMaxLimit():
    try:
        #print("actionSetZMaxLimit")

        # check the password first
        Passwd = "bojay"
        strPassword = str(varPassword.get())
        # get local password
        # strPasswordPath = os.getcwd() + "/YourPasswd.txt"
        # LocalPassword = open(strPasswordPath, "r")
        # strAllLine = str(LocalPassword.readline())
        # #print(strAllLine)
        if (Passwd == strPassword):
            varPassword.set("bojay")
        else:
            tkMessageBox.showinfo("Error", "You need to input correct password")
            return

        value = varSetZMaxLimitEntry.get()
        ret = goectl.SetPLCLimit(goectl.Z_axis,goectl.Max_limit,float(value))
        if ret != 0:
            tkMessageBox.showinfo("Error", "actionSetZMaxLimit fail")
        goectl.SaveLimitTXT("ZAxisMaxLimit", value)
    except:
        tkMessageBox.showinfo("Error", "actionSetZMaxLimit error")

# def actionSetZMaxLimit():
#     try:
#         if (str(varSetZMaxLimitEntry.get()).__len__() < 1):
#             tkMessageBox.showinfo("Error", "You need to input the Z  max limit")

#         # check the password first
#         Passwd = "bojay"
#         # strPassword = str(varPassword.get())
#         # get local password
#         strPasswordPath = os.getcwd() + "/YourPasswd.txt"
#         LocalPassword = open(strPasswordPath, "r")
#         strAllLine = str(LocalPassword.readline())
#         #print(strAllLine)
#         if (Passwd == strAllLine):
#             varPassword.set("bojay")
#         else:
#             tkMessageBox.showinfo("Error", "You need to input correct password")
#             return

#         ret = goectl.SetPLCLimit(goectl.Z_axis, goectl.Max_limit, float(varSetZMaxLimitEntry.get()))
#         if ret != 0:
#             tkMessageBox.showinfo("Error", goectl.strErrorMessage)
#             return
#     except:
#         tkMessageBox.showinfo("Error", "SetZMaxLimit error")


# *********************************************************************************#
def actionSetZMinLimit():
    try:
        #print("actionSetZMinLimit")

        # check the password first
        Passwd = "bojay"
        strPassword = str(varPassword.get())
        # get local password
        # strPasswordPath = os.getcwd() + "/YourPasswd.txt"
        # LocalPassword = open(strPasswordPath, "r")
        # strAllLine = str(LocalPassword.readline())
        # #print(strAllLine)
        if (Passwd == strPassword):
            varPassword.set("bojay")
        else:
            tkMessageBox.showinfo("Error", "You need to input correct password")
            return

        value = varSetZMinLimitEntry.get()
        ret = goectl.SetPLCLimit(goectl.Z_axis,goectl.Min_limit,float(value))
        if ret != 0:
            tkMessageBox.showinfo("Error", "actionSetZMinLimit fail")
        goectl.SaveLimitTXT("ZAxisMinLimit", value)
    except:
        tkMessageBox.showinfo("Error", "actionSetZMinLimit error")

# def actionSetZMinLimit():
#     try:
#         if (str(varSetZMinLimitEntry.get()).__len__() < 1):
#             tkMessageBox.showinfo("Error", "You need to input the Z  min limit")

#         # check the password first
#         Passwd = "bojay"
#         # strPassword = str(varPassword.get())
#         get local password
#         strPasswordPath = os.getcwd() + "/YourPasswd.txt"
#         LocalPassword = open(strPasswordPath, "r")
#         strAllLine = str(LocalPassword.readline())
#         #print(strAllLine)
#         if (Passwd == strPassword):
#             varPassword.set("bojay")
#         else:
#             tkMessageBox.showinfo("Error", "You need to input correct password")
#             return

#         ret = goectl.SetPLCLimit(goectl.Z_axis, goectl.Min_limit, float(varSetZMinLimitEntry.get()))
#         if ret != 0:
#             tkMessageBox.showinfo("Error", goectl.strErrorMessage)
#             return
#     except:
#         tkMessageBox.showinfo("Error", "SetZMinLimit error")
# ************************************************************************************#



# *********************************************************************************#
def actionSetZX1Limit():
    try:
        #print("actionSetZX1Limit")

        # check the password first
        Passwd = "bojay"
        strPassword = str(varPassword.get())
        # get local password
        # strPasswordPath = os.getcwd() + "/YourPasswd.txt"
        # LocalPassword = open(strPasswordPath, "r")
        # strAllLine = str(LocalPassword.readline())
        # #print(strAllLine)
        if (Passwd == strPassword):
            varPassword.set("bojay")
        else:
            tkMessageBox.showinfo("Error", "You need to input correct password")
            return

        value = varSetZAxisX1Entry.get()
        ret = goectl.SetPLCLimit(goectl.ZAxisX1Limit,goectl.Min_limit,float(value))
        if ret != 0:
            tkMessageBox.showinfo("Error", "actionSetZX1Limit fail")
        goectl.SaveLimitTXT("ZAxisX1Limit", value)
    except:
        tkMessageBox.showinfo("Error", "actionSetZX1Limit error")
# ************************************************************************************#


# *********************************************************************************#
def actionSetZX2Limit():
    try:
        #print("actionSetZX2Limit")

        # check the password first
        Passwd = "bojay"
        strPassword = str(varPassword.get())
        # get local password
        # strPasswordPath = os.getcwd() + "/YourPasswd.txt"
        # LocalPassword = open(strPasswordPath, "r")
        # strAllLine = str(LocalPassword.readline())
        # #print(strAllLine)
        if (Passwd == strPassword):
            varPassword.set("bojay")
        else:
            tkMessageBox.showinfo("Error", "You need to input correct password")
            return

        value = varSetZAxisX2Entry.get()
        ret = goectl.SetPLCLimit(goectl.ZAxisX2Limit,goectl.Min_limit,float(value))
        if ret != 0:
            tkMessageBox.showinfo("Error", "actionSetZX2Limit fail")
        goectl.SaveLimitTXT("ZAxisX2Limit", value)
    except:
        tkMessageBox.showinfo("Error", "actionSetZX2Limit error")
# ************************************************************************************#


# *********************************************************************************#
def actionSetZY1Limit():
    try:
        #print("actionSetZY1Limit")

        # check the password first
        Passwd = "bojay"
        strPassword = str(varPassword.get())
        # get local password
        # strPasswordPath = os.getcwd() + "/YourPasswd.txt"
        # LocalPassword = open(strPasswordPath, "r")
        # strAllLine = str(LocalPassword.readline())
        # #print(strAllLine)
        if (Passwd == strPassword):
            varPassword.set("bojay")
        else:
            tkMessageBox.showinfo("Error", "You need to input correct password")
            return

        value = varSetZAxisY1Entry.get()
        ret = goectl.SetPLCLimit(goectl.ZAxisY1Limit,goectl.Min_limit,float(value))
        if ret != 0:
            tkMessageBox.showinfo("Error", "actionSetZY1Limit fail")
        goectl.SaveLimitTXT("ZAxisY1Limit", value)
    except:
        tkMessageBox.showinfo("Error", "actionSetZY1Limit error")
# ************************************************************************************#


# *********************************************************************************#
def actionFullScreenTest():
    try:
        #print("actionSetZY1Limit")
        #get x1
        x1 = varXCoordinateEntry.get()
        y1 = varYCoordinateEntry.get()
        z1 = varZCoordinateEntry.get()


        x2 = varX1CoordinateEntry.get()
        y2 = varY1CoordinateEntry.get()
        z2 = varZ1CoordinateEntry.get()

        ret = goectl.SignalReset(10)

	    # tempDUTALock = goectl.DUTLcokOrOpen(goectl.DUTALL,goectl.DUT_LOCK)
        # time.sleep(0.2)
        for i in range(0,50,1):
            tempIN = goectl.Set_CylindeFunction(goectl.Cylinder_IN)
            time.sleep(1)

            #move x
            ret = goectl.MoveToCoordinates(goectl.X_axis,float(x1),10)
            if ret != 0:
                tkMessageBox.showinfo("Error", "actionFullScreenTest error")
                return -1
            #move y
            ret = goectl.MoveToCoordinates(goectl.Y_axis, float(y1), 10)
            if ret != 0:
                tkMessageBox.showinfo("Error", "actionFullScreenTest error")
                return -1
            #move z
            ret = goectl.MoveToCoordinates(goectl.Z_axis, float(z1), 10)
            if ret != 0:
                tkMessageBox.showinfo("Error", "actionFullScreenTest error")
                return -1

            #pin
            pin1 = goectl.PushPinDown(goectl.Pin1)
            time.sleep(0.5)
            pin1 = goectl.LiftPinUp(goectl.Pin1)
            time.sleep(0.5)
            pin2 = goectl.PushPinDown(goectl.Pin2)
            time.sleep(0.5)
            # pin3 = goectl.PushPinDown(goectl.Pin3)
            # time.sleep(0.5)
            # power = goectl.EnablePowerSource(True)
            # time.sleep(1)

            pin2 = goectl.LiftPinUp(goectl.Pin2)
            time.sleep(0.5)
            # pin3 = goectl.LiftPinUp(goectl.Pin3)
            # time.sleep(0.5)
            # power = goectl.EnablePowerSource(False)
            # time.sleep(1)



            #safe
            # ret = goectl.MoveToCoordinates(goectl.Z_axis, 0, 10)
            # if ret != 0:
            #     tkMessageBox.showinfo("Error", "actionFullScreenTest error")
            #     return -1

            #move x
            ret = goectl.MoveToCoordinates(goectl.X_axis,float(x2),10)
            if ret != 0:
                tkMessageBox.showinfo("Error", "actionFullScreenTest error")
                return -1
            #move y
            ret = goectl.MoveToCoordinates(goectl.Y_axis, float(y2), 10)
            if ret != 0:
                tkMessageBox.showinfo("Error", "actionFullScreenTest error")
                return -1
            #move z
            ret = goectl.MoveToCoordinates(goectl.Z_axis, float(z2), 10)
            if ret != 0:
                tkMessageBox.showinfo("Error", "actionFullScreenTest error")
                return -1

            #safe
            # ret = goectl.MoveToCoordinates(goectl.Z_axis, 0, 10)
            # if ret != 0:
            #     tkMessageBox.showinfo("Error", "actionFullScreenTest error")
            #     return -1

            #reset
            ret = goectl.SignalReset(10)
            time.sleep(1)

    except:
        tkMessageBox.showinfo("Error", "actionSetZY1Limit error")
# ************************************************************************************#



# *********************************************************************************#
def actionSetZY2Limit():
    try:
        #print("actionSetZY2Limit")

        # check the password first
        Passwd = "bojay"
        strPassword = str(varPassword.get())
        # get local password
        # strPasswordPath = os.getcwd() + "/YourPasswd.txt"
        # LocalPassword = open(strPasswordPath, "r")
        # strAllLine = str(LocalPassword.readline())
        # #print(strAllLine)
        if (Passwd == strPassword):
            varPassword.set("bojay")
        else:
            tkMessageBox.showinfo("Error", "You need to input correct password")
            return

        value = varSetZAxisY2Entry.get()
        ret = goectl.SetPLCLimit(goectl.ZAxisY2Limit,goectl.Min_limit,float(value))
        if ret != 0:
            tkMessageBox.showinfo("Error", "actionSetZY2Limit fail")
        goectl.SaveLimitTXT("ZAxisY2Limit", value)
    except:
        tkMessageBox.showinfo("Error", "actionSetZY2Limit error")
# ************************************************************************************#


# *********************************************************************************#
def actionSetZY3Limit():
    try:
        #print("actionSetZY3Limit")

        # check the password first
        Passwd = "bojay"
        strPassword = str(varPassword.get())
        # get local password
        # strPasswordPath = os.getcwd() + "/YourPasswd.txt"
        # LocalPassword = open(strPasswordPath, "r")
        # strAllLine = str(LocalPassword.readline())
        # #print(strAllLine)
        if (Passwd == strPassword):
            varPassword.set("bojay")
        else:
            tkMessageBox.showinfo("Error", "You need to input correct password")
            return

        value = varSetZAxisY3Entry.get()
        ret = goectl.SetPLCLimit(goectl.ZAxisY3Limit,goectl.Min_limit,float(value))
        if ret != 0:
            tkMessageBox.showinfo("Error", "actionSetZY3Limit fail")
        goectl.SaveLimitTXT("ZAxisY3Limit", value)
    except:
        tkMessageBox.showinfo("Error", "actionSetZY3Limit error")
# ************************************************************************************#



# *********************************************************************************#
def actionSetZY4Limit():
    try:
        #print("actionSetZY4Limit")

        # check the password first
        Passwd = "bojay"
        strPassword = str(varPassword.get())
        # get local password
        # strPasswordPath = os.getcwd() + "/YourPasswd.txt"
        # LocalPassword = open(strPasswordPath, "r")
        # strAllLine = str(LocalPassword.readline())
        # #print(strAllLine)
        if (Passwd == strPassword):
            varPassword.set("bojay")
        else:
            tkMessageBox.showinfo("Error", "You need to input correct password")
            return

        value = varSetZAxisY4Entry.get()
        ret = goectl.SetPLCLimit(goectl.ZAxisY4Limit,goectl.Min_limit,float(value))
        if ret != 0:
            tkMessageBox.showinfo("Error", "actionSetZY4Limit fail")
    except:
        tkMessageBox.showinfo("Error", "actionSetZY4Limit error")
# ************************************************************************************#
def YourPasswd():
    FolderPath = os.getcwd() + "/YourPasswd.txt"
    output = open(FolderPath,'w')
    output.write(str(varPassword.get())+'\n')
    output.close()
    time.sleep(0.5)

def OpenSenorPort():
    try:
        #print("Get Sensor pressure")
        ret = goectl.OpenSensorPort()
        if ret == -1:
            tkMessageBox.showinfo("Error", "OpenSensorPort fail")
            return -1
        buttonCloseSensor.configure(state='active')
        buttonGetSensor.configure(state='active')
        buttonSetToZero.configure(state='active')
        buttonOpenSensor.configure(state='disabled')
    except :
        tkMessageBox.showinfo("Error", "OpenSensorPort fail")

def actionGetSensorPessure():
    try:
        #print("Get Sensor pressure")
        ret = goectl.GetLigentPressure(goectl.command_lines)
        if ret == -1:
            tkMessageBox.showinfo("Error", "GetSensorPressure fail")
            return -1
        varLine1Entry.set(float(ret[0]))
        varLine2Entry.set(float(ret[1]))
        varLine3Entry.set(float(ret[2]))

    except Exception as e:
        tkMessageBox.showinfo("Error", "GetSensorPressure fail")


def actionSetPessureZore():
    try:
        ret = goectl.SetLigentToZero(goectl.command_SetLinesZero)
        if ret == -1:
            tkMessageBox.showinfo("Error", "SetLigentToZero fail")
            return -1
    except Exception as e:
        tkMessageBox.showinfo("Error", "SetLigentToZero fail")


def CloseSensorPort():
    try:
        #print("Get Sensor pressure")
        ret = goectl.CloseSensorPort()
        if ret == -1:
            tkMessageBox.showinfo("Error", "CloseSensorPort fail")
            return -1
        buttonGetSensor.configure(state='disabled')
        buttonSetToZero.configure(state='disabled')
        buttonCloseSensor.configure(state='disabled')
        buttonOpenSensor.configure(state='active')
    except:
        tkMessageBox.showinfo("Error", "CloseSensorPort fail")

# title and font
root.title('Bojay P71 GUI V1.0')
helv10 = tkFont.Font(family="Helvetica",size=10,weight="bold")


#motion parameter
Label(root, text='X', width=10).grid(row=1, column=7)
Label(root, text='Y', width=10).grid(row=1, column=8)
Label(root, text='Z', width=10).grid(row=1, column=9)
Label(root, text='Parameter', width=10, font=helv10).grid(row=1, column=6)
Label(root, text='Speed', width=10, font=helv10).grid(row=4, column=6)
Label(root, text='Move', width=10, font=helv10).grid(row=5, column=6)
coordinateX = Entry(root, width=10)
coordinateX.grid(row=5, column=7)
XbuttonMove = Button(root, text='MoveX', command=actionMoveX, width=10)
XbuttonMove.grid(row=6, column=7)
XbuttonMove.configure(state='disabled')

coordinateY = Entry(root, width=10)
coordinateY.grid(row=5, column=8)
YbuttonMove = Button(root, text='MoveY', command=actionMoveY, width=10)
YbuttonMove.grid(row=6, column=8)
YbuttonMove.configure(state='disabled')


coordinateZ = Entry(root, width=10)
coordinateZ.grid(row=5, column=9)
ZbuttonMove = Button(root, text='MoveZ', command=actionMoveZ, width=10)
ZbuttonMove.grid(row=6, column=9)
ZbuttonMove.configure(state='disabled')



XbuttonSetSpeed = Button(root, text='SetSpeedX', command=actionSetSpeedX, width=10)
XbuttonSetSpeed.grid(row=3, column=7)
XbuttonSetSpeed.configure(state='disabled')
varXSpeed=StringVar()
XSpeed = Entry(root, textvariable = varXSpeed,width=10)
XSpeed.grid(row=4, column=7)



YbuttonSetSpeed = Button(root, text='SetSpeedY', command=actionSetSpeedY, width=10)
YbuttonSetSpeed.grid(row=3, column=8)
YbuttonSetSpeed.configure(state='disabled')
varYSpeed=StringVar()
YSpeed = Entry(root, textvariable = varYSpeed,width=10)
YSpeed.grid(row=4, column=8)



ZbuttonSetSpeed = Button(root, text='SetSpeedZ', command=actionSetSpeedZ, width=10)
ZbuttonSetSpeed.grid(row=3, column=9)
ZbuttonSetSpeed.configure(state='disabled')
varZSpeed=StringVar()
XSpeed = Entry(root, textvariable = varZSpeed,width=10)
XSpeed.grid(row=4, column=9)

ent_speedx = Entry(root, width=10)
ent_speedx.grid(row=2, column=7)
ent_speedy = Entry(root, width=10)
ent_speedy.grid(row=2, column=8)
ent_speedz = Entry(root, width=10)
ent_speedz.grid(row=2, column=9)



# com port selection
Label(root, text='COM', width=10).grid(row=0, column=1)
buttonOpenPort = Button(root, text='OpenPort', command=actionOPenPort, width=10)
buttonOpenPort.grid(row=0, column=2)

# close
buttonClose = Button(root, text='Close', command=actionClose, width=10)
buttonClose.grid(row=0, column=3)
buttonClose.configure(state='disabled')

buttonGetVer = Button(root, text='GetVer', command=actionGetVer, width=10)
buttonGetVer.grid(row=0, column=4)
buttonGetVer.configure(state='disabled')

# Create open/close safe light curtain
buttonOpenLightcurtain = Button(root, text='OpenCurtain', command=actionOpenCurtain, width=10)
buttonOpenLightcurtain.grid(row=15, column=7)
buttonOpenLightcurtain.configure(state='disabled')
# Create open/close safe light curtain
buttonCloseLightcurtain = Button(root, text='CloseCurtain', command=actionCloseCurtain, width=10)
buttonCloseLightcurtain.grid(row=15, column=8)
buttonCloseLightcurtain.configure(state='disabled')




# B1Calibrate button
buttonB1Calibration = Button(root, text='Calibration', command=actionCalibration, width=16)
buttonB1Calibration.grid(row=10, column=7)
buttonB1Calibration.configure(state='disabled')



# Presshole button
buttonCloseSensor = Button(root, text='CloseSensor', command=CloseSensorPort, width=12)
buttonCloseSensor.grid(row=9, column=5)
buttonCloseSensor.configure(state='disabled')



# reset
buttonReset = Button(root, text='Reset', command=actionReset, width=10)
buttonReset.grid(row=15, column=9)
buttonReset.configure(state='disabled')

# Dot
buttonDot = Button(root, text='Dot', command=actionDot, width=10)
buttonDot.grid(row=20, column=9)
buttonDot.configure(state='disabled')
varDotEntry=StringVar()
DotEntry = Entry(root, textvariable = varDotEntry,width=10)
DotEntry.grid(row=19, column=9)

#Burning times
buttonGetSensor = Button(root, text='Get', command=actionGetSensorPessure, width=12)
buttonGetSensor.grid(row=13, column=4)
buttonGetSensor.configure(state='disabled')
buttonSetToZero = Button(root, text='SetToZero', command=actionSetPessureZore, width=12)
buttonSetToZero.grid(row=13, column=5)
buttonSetToZero.configure(state='disabled')


Label(root, text='LCDLine1', width=10).grid(row=10, column=4)
Label(root, text='LCDLine2', width=10).grid(row=11, column=4)
Label(root, text='LCDLine2', width=10).grid(row=12, column=4)

varLine1Entry=StringVar()
Line1Entry = Entry(root, textvariable = varLine1Entry,width=10)
Line1Entry.grid(row=10, column=5)

varLine2Entry=StringVar()
Line2Entry = Entry(root, textvariable = varLine2Entry,width=10)
Line2Entry.grid(row=11, column=5)

varLine3Entry=StringVar()
Line3Entry = Entry(root, textvariable = varLine3Entry,width=10)
Line3Entry.grid(row=12, column=5)

varversion=StringVar()
version = Entry(root, textvariable = varversion,width=10)
version.grid(row=0, column=5)


# Burning start
buttonOpenSensor = Button(root, text='OpenSensor', command=OpenSenorPort, width=12)
buttonOpenSensor.grid(row=9, column=4)
buttonOpenSensor.configure(state='active')

# Alarm buzzer(
# buttonAlarmbuzzer = Button(root, text='AlarmOn', command=actionAlarmbuzzer, width=10)
# buttonAlarmbuzzer.grid(row=13, column=8)
# buttonAlarmbuzzer.configure(state='disabled')
#
#
# buttonAlarmbuzzerOff = Button(root, text='AlarmOff', command=actionAlarmbuzzerOff, width=10)
# buttonAlarmbuzzerOff.grid(row=12, column=8)
# buttonAlarmbuzzerOff.configure(state='disabled')







#Start Test
buttonStartTest = Button(root, text='Start Test', command=actionStartTest, width=10)
buttonStartTest.grid(row=17, column=9)
buttonStartTest.configure(state='disabled')


# Cylinder IN
buttonCylinderIN = Button(root, text='Cylinder IN', command=actionCylinderIN, width=10)
buttonCylinderIN.grid(row=13, column=9)
buttonCylinderIN.configure(state='disabled')


# Cylinder Out
buttonCylinderOut = Button(root, text='Cylinder Out', command=actionCylinderOUT, width=10)
buttonCylinderOut.grid(row=14, column=9)
buttonCylinderOut.configure(state='disabled')



# DU1 Lock
buttonDU1Lock = Button(root, text='UST2 Lock', command=actionDU2Lock, width=10)
buttonDU1Lock.grid(row=14, column=8)
buttonDU1Lock.configure(state='disabled')
buttonDU2Lock = Button(root, text='UST1 Lock', command=actionDU1Lock, width=10)
buttonDU2Lock.grid(row=13, column=8)
buttonDU2Lock.configure(state='disabled')




# DU1 Open
buttonDU1Open = Button(root, text='UST2 Unlock', command=actionDU2Open, width=10)
buttonDU1Open.grid(row=14, column=7)
buttonDU1Open.configure(state='disabled')
buttonDU2Open = Button(root, text='UST1 Unlock', command=actionDU1Open, width=10)
buttonDU2Open.grid(row=13, column=7)
buttonDU2Open.configure(state='disabled')


# USB Lock and DC Lock
buttonUSBLock = Button(root, text='USB Lock', command=actionUSBLock, width=10)
buttonUSBLock.grid(row=12, column=8)
buttonUSBLock.configure(state='active')
buttonDCLock = Button(root, text='DC Lock', command=actionDCLock, width=10)
buttonDCLock.grid(row=11, column=8)
buttonDCLock.configure(state='active')




# USB Unlock and DC Unlock
buttonUSBUnlock = Button(root, text='USB Unlock', command=actionUSBUnlock, width=10)
buttonUSBUnlock .grid(row=12, column=7)
buttonUSBUnlock .configure(state='active')
buttonDCUnlock = Button(root, text='DC Unlock', command=actionDCUnlock, width=10)
buttonDCUnlock.grid(row=11, column=7)
buttonDCUnlock.configure(state='active')



#################################################################
#Tony add below to set max&min limit
#for x
Label(root, text='SetXMaxLimit', width=10).grid(row=16, column=1)
varSetXMaxLimitEntry=StringVar()
SetXMaxLimitEntry = Entry(root, textvariable = varSetXMaxLimitEntry,width=10)
SetXMaxLimitEntry.grid(row=16, column=2)

buttonSetXMaxLimit= Button(root, text='SetXMaxLimit', command=actionSetXMaxLimit, width=15)
buttonSetXMaxLimit.grid(row=16, column=3)
buttonSetXMaxLimit.configure(state='disabled')

Label(root, text='SetXMinLimit', width=10).grid(row=17, column=1)
varSetXMinLimitEntry=StringVar()
SetXMinLimitEntry = Entry(root, textvariable = varSetXMinLimitEntry,width=10)
SetXMinLimitEntry.grid(row=17, column=2)

buttonSetXMinLimit = Button(root, text='SetXMinLimit', command=actionSetXMinLimit, width=15)
buttonSetXMinLimit.grid(row=17, column=3)
buttonSetXMinLimit.configure(state='disabled')

#for y
Label(root, text='SetYMaxLimit', width=10).grid(row=18, column=1)
varSetYMaxLimitEntry=StringVar()
SetYMaxLimitEntry = Entry(root, textvariable = varSetYMaxLimitEntry,width=10)
SetYMaxLimitEntry.grid(row=18, column=2)

buttonSetYMaxLimit= Button(root, text='SetYMaxLimit', command=actionSetYMaxLimit, width=15)
buttonSetYMaxLimit.grid(row=18, column=3)
buttonSetYMaxLimit.configure(state='disabled')

Label(root, text='SetYMinLimit', width=10).grid(row=19, column=1)
varSetYMinLimitEntry=StringVar()
SetYMinLimitEntry = Entry(root, textvariable = varSetYMinLimitEntry,width=10)
SetYMinLimitEntry.grid(row=19, column=2)
#SetYMinLimitEntry.configure(state='disabled')
buttonSetYMinLimit = Button(root, text='SetYMinLimit', command=actionSetYMinLimit, width=15)
buttonSetYMinLimit.grid(row=19, column=3)
buttonSetYMinLimit.configure(state='disabled')



#for z
Label(root, text='SetZMaxLimit', width=10).grid(row=20, column=1)
varSetZMaxLimitEntry=StringVar()
SetZMaxLimitEntry = Entry(root, textvariable = varSetZMaxLimitEntry,width=10)
SetZMaxLimitEntry.grid(row=20, column=2)
#SetZMaxLimitEntry.configure(state='disabled')
buttonSetZMaxLimit= Button(root, text='SetZMaxLimit', command=actionSetZMaxLimit, width=15)
buttonSetZMaxLimit.grid(row=20, column=3)
buttonSetZMaxLimit.configure(state='disabled')

Label(root, text='SetZMinLimit', width=10).grid(row=21, column=1)
varSetZMinLimitEntry=StringVar()
SetZMinLimitEntry = Entry(root, textvariable = varSetZMinLimitEntry,width=10)
SetZMinLimitEntry.grid(row=21, column=2)

buttonSetZMinLimit = Button(root, text='SetZMinLimit', command=actionSetZMinLimit, width=15)
buttonSetZMinLimit.grid(row=21, column=3)
buttonSetZMinLimit.configure(state='disabled')


# ##############################################################
# Label(root, text='SetZAxis-X1', width=10).grid(row=18, column=4)
# varSetZAxisX1Entry=StringVar()
# SetZAxisX1Entry = Entry(root, textvariable = varSetZAxisX1Entry,width=10)
# SetZAxisX1Entry.grid(row=18, column=5)
# #SetZAxisX1Entry.configure(state='disabled')
# buttonSetZAxisX1Entry = Button(root, text='SetZAxis-X1', command=actionSetZX1Limit, width=15)
# buttonSetZAxisX1Entry.grid(row=18, column=6)
# buttonSetZAxisX1Entry.configure(state='disabled')


# Label(root, text='SetZAxis-X2', width=10).grid(row=19, column=4)
# varSetZAxisX2Entry=StringVar()
# SetZAxisX2Entry = Entry(root, textvariable = varSetZAxisX2Entry,width=10)
# SetZAxisX2Entry.grid(row=19, column=5)
# #SetZAxisX2Entry.configure(state='disabled')
# buttonSetZAxisX2Entry = Button(root, text='SetZAxis-X2', command=actionSetZX2Limit, width=15)
# buttonSetZAxisX2Entry.grid(row=19, column=6)
# buttonSetZAxisX2Entry.configure(state='disabled')


# Label(root, text='SetZAxis-Y1', width=10).grid(row=20, column=4)
# varSetZAxisY1Entry=StringVar()
# SetZAxisY1Entry = Entry(root, textvariable = varSetZAxisY1Entry,width=10)
# SetZAxisY1Entry.grid(row=20, column=5)
# #SetZAxisY1Entry.configure(state='disabled')
# buttonSetZAxisY1Entry = Button(root, text='SetZAxis-Y1', command=actionSetZY1Limit, width=15)
# buttonSetZAxisY1Entry.grid(row=20, column=6)
# buttonSetZAxisY1Entry.configure(state='disabled')


# Label(root, text='SetZAxis-Y2', width=10).grid(row=21, column=4)
# varSetZAxisY2Entry=StringVar()
# SetZAxisY2Entry = Entry(root, textvariable = varSetZAxisY2Entry,width=10)
# SetZAxisY2Entry.grid(row=21, column=5)
# #SetZAxisY2Entry.configure(state='disabled')
# buttonSetZAxisY2Entry = Button(root, text='SetZAxis-Y2', command=actionSetZY2Limit, width=15)
# buttonSetZAxisY2Entry.grid(row=21, column=6)
# buttonSetZAxisY2Entry.configure(state='disabled')



# Label(root, text='SetZAxis-Y3', width=10).grid(row=22, column=4)
# varSetZAxisY3Entry=StringVar()
# SetZAxisY3Entry = Entry(root, textvariable = varSetZAxisY3Entry,width=10)
# SetZAxisY3Entry.grid(row=22, column=5)
# #SetZAxisY3Entry.configure(state='disabled')
# buttonSetZAxisY3Entry = Button(root, text='SetZAxis-Y3', command=actionSetZY3Limit, width=15)
# buttonSetZAxisY3Entry.grid(row=22, column=6)
# buttonSetZAxisY3Entry.configure(state='disabled')


# Label(root, text='SetZAxis-Y4', width=10).grid(row=23, column=4)
# varSetZAxisY4Entry=StringVar()
# SetZAxisY4Entry = Entry(root, textvariable = varSetZAxisY4Entry,width=10)
# SetZAxisY4Entry.grid(row=23, column=5)
# #SetZAxisY4Entry.configure(state='disabled')
# buttonSetZAxisY4Entry = Button(root, text='SetZAxis-Y4', command=actionSetZY4Limit, width=15)
# buttonSetZAxisY4Entry.grid(row=23, column=6)
# buttonSetZAxisY4Entry.configure(state='disabled')




################################################################
#the coordinate for draw circle & rectangle & dot
Label(root, text='X Coordinate', width=10).grid(row=16, column=7)
varXCoordinateEntry=StringVar()
XCoordinateEntry = Entry(root, textvariable = varXCoordinateEntry,width=10)
XCoordinateEntry.grid(row=16, column=8)
#XCoordinateEntry.configure(state='disabled')


Label(root, text='Y Coordinate', width=10).grid(row=17, column=7)
varYCoordinateEntry=StringVar()
YCoordinateEntry = Entry(root, textvariable = varYCoordinateEntry,width=10)
YCoordinateEntry.grid(row=17, column=8)
#YCoordinateEntry.configure(state='disabled')


Label(root, text='Z Coordinate', width=10).grid(row=18, column=7)
varZCoordinateEntry=StringVar()
ZCoordinateEntry = Entry(root, textvariable = varZCoordinateEntry,width=10)
ZCoordinateEntry.grid(row=18, column=8)
#ZCoordinateEntry.configure(state='disabled')


Label(root, text='X1 Coordinate', width=10).grid(row=19, column=7)
varX1CoordinateEntry=StringVar()
X1CoordinateEntry = Entry(root, textvariable = varX1CoordinateEntry,width=10)
X1CoordinateEntry.grid(row=19, column=8)
#XCoordinateEntry.configure(state='disabled')


Label(root, text='Y1 Coordinate', width=10).grid(row=20, column=7)
varY1CoordinateEntry=StringVar()
Y1CoordinateEntry = Entry(root, textvariable = varY1CoordinateEntry,width=10)
Y1CoordinateEntry.grid(row=20, column=8)
#YCoordinateEntry.configure(state='disabled')


Label(root, text='Z1 Coordinate', width=10).grid(row=21, column=7)
varZ1CoordinateEntry=StringVar()
Z1CoordinateEntry = Entry(root, textvariable = varZ1CoordinateEntry,width=10)
Z1CoordinateEntry.grid(row=21, column=8)


buttonFullScreenTest = Button(root, text='FullScreenTest', command=actionFullScreenTest, width=15)
buttonFullScreenTest.grid(row=18, column=9)
buttonFullScreenTest.configure(state='disabled')

#ZCoordinateEntry.configure(state='disabled')

#################################################################


#Steep set
# Label(root, text='Steep set', width=10).grid(row=17, column=1)
# varSteepSetEntry=StringVar()
# SteepSetEntry = Entry(root, textvariable = varSteepSetEntry,width=10)
# SteepSetEntry.grid(row=17, column=2)
# SteepSetEntry.configure(state='disabled')
# buttonSetSteep = Button(root, text='SetSteepAction', command=actionSet_Steep, width=15)
# buttonSetSteep.grid(row=17, column=3)
# buttonSetSteep.configure(state='disabled')
# varSteepGetEntry=StringVar()
# SteepGetEntry = Entry(root, textvariable = varSteepGetEntry,width=10)
# SteepGetEntry.grid(row=17, column=4)
# SteepGetEntry.configure(state='disabled')
#Password
# buttonSetPassword = Button(root, text='Password', command=YourPasswd, width=10)
# buttonSetPassword.grid(row=17, column=1)
# buttonSetPassword.configure(state='disabled')
Label(root, text='Password', width=10).grid(row=15, column=1)
varPassword = StringVar()
Password = Entry(root, textvariable = varPassword,width=10)
Password.grid(row=15, column=2)


# ************************************************************************************#
# Increment
#X
Label(root, text='XStep', width=10).grid(row=9, column=1)
varXIncrement_step = StringVar()
XIncrement_step = Entry(root, textvariable = varXIncrement_step,width=10)
XIncrement_step.grid(row=9, column=2)
buttonIncrementx = Button(root, text='Increment', command=XactionIncrement, width=10)
buttonIncrementx.grid(row=9, column=3)
buttonIncrementx.configure(state='disabled')
# Decrement
Label(root, text='XStep', width=10).grid(row=10, column=1)
varXDecrement_step = StringVar()
XDecrement_step = Entry(root, textvariable = varXDecrement_step,width=10)
XDecrement_step.grid(row=10, column=2)
buttonDecrementx = Button(root, text='Decrement', command=XactionDecrement, width=10)
buttonDecrementx.grid(row=10, column=3)
buttonDecrementx.configure(state='disabled')
# ************************************************************************************#



# ************************************************************************************#
#Y
Label(root, text='YStep', width=10).grid(row=11, column=1)
varYIncrement_step = StringVar()
YIncrement_step = Entry(root, textvariable = varYIncrement_step,width=10)
YIncrement_step.grid(row=11, column=2)
buttonIncrementy = Button(root, text='Increment', command=YactionIncrement, width=10)
buttonIncrementy.grid(row=11, column=3)
buttonIncrementy.configure(state='disabled')
# Decrement
Label(root, text='YStep', width=10).grid(row=12, column=1)
varYDecrement_step = StringVar()
YDecrement_step = Entry(root, textvariable = varYDecrement_step,width=10)
YDecrement_step.grid(row=12, column=2)
buttonDecrementy = Button(root, text='Decrement', command=YactionDecrement, width=10)
buttonDecrementy.grid(row=12, column=3)
buttonDecrementy.configure(state='disabled')
# ************************************************************************************#


# ************************************************************************************#
#Z
Label(root, text='ZStep', width=10).grid(row=13, column=1)
varZIncrement_step = StringVar()
ZIncrement_step = Entry(root, textvariable = varZIncrement_step,width=10)
ZIncrement_step.grid(row=13, column=2)
buttonIncrementz = Button(root, text='Increment', command=ZactionIncrement, width=10)
buttonIncrementz.grid(row=13, column=3)
buttonIncrementz.configure(state='disabled')
# Decrement
Label(root, text='ZStep', width=10).grid(row=14, column=1)
varZDecrement_step = StringVar()
ZDecrement_step = Entry(root, textvariable = varZDecrement_step,width=10)
ZDecrement_step.grid(row=14, column=2)
buttonDecrementz = Button(root, text='Decrement', command=ZactionDecrement, width=10)
buttonDecrementz.grid(row=14, column=3)
buttonDecrementz.configure(state='disabled')
# ************************************************************************************#




# ************************************************************************************#
#X&Y&Z Max limit
Label(root, text='X', width=10).grid(row=1, column=2)

Label(root, text='Y', width=10).grid(row=1, column=3)
Label(root, text='Z', width=10).grid(row=1, column=4)
Label(root, text='Max Limit', width=10).grid(row=2, column=1)
varXMax_limit=StringVar()
XMax_limit = Entry(root, textvariable = varXMax_limit,width=10)
XMax_limit.grid(row=2, column=2)
varYMax_limit=StringVar()
YMax_limit = Entry(root, textvariable = varYMax_limit,width=10)
YMax_limit.grid(row=2, column=3)
varZMax_limit=StringVar()
ZMax_limit = Entry(root, textvariable = varZMax_limit,width=10)
ZMax_limit.grid(row=2, column=4)
buttonGetMaxLimit = Button(root, text='Get Max Limit', command=GetMaxLimit, width=15)
buttonGetMaxLimit.grid(row=2, column=5)
buttonGetMaxLimit.configure(state='disabled')
# ************************************************************************************#




# ************************************************************************************#
#X&Y&Z Min limit
Label(root, text='Min Limit', width=10).grid(row=3, column=1)
varXMin_limit=StringVar()
XMin_limit = Entry(root, textvariable = varXMin_limit,width=10)
XMin_limit.grid(row=3, column=2)
varYMin_limit=StringVar()
YMin_limit = Entry(root, textvariable = varYMin_limit,width=10)
YMin_limit.grid(row=3, column=3)
varZMin_limit=StringVar()
ZMin_limit = Entry(root, textvariable = varZMin_limit,width=10)
ZMin_limit.grid(row=3, column=4)
buttonMinLimit = Button(root, text='Get Min Limit', command=GetMinLimit, width=15)
buttonMinLimit.grid(row=3, column=5)
buttonMinLimit.configure(state='disabled')
# ************************************************************************************#



# ************************************************************************************#
#X&Y&Z position
Label(root, text='Position', width=10).grid(row=4, column=1)
varXPosition=StringVar()
XPosition = Entry(root, textvariable = varXPosition,width=10)
XPosition.grid(row=4, column=2)

varYPosition=StringVar()
YPosition = Entry(root, textvariable = varYPosition,width=10)
YPosition.grid(row=4, column=3)

varZPosition=StringVar()
ZPosition = Entry(root, textvariable = varZPosition,width=10)
ZPosition.grid(row=4, column=4)

buttonGetPosition = Button(root, text='Get Position', command=GetPosition, width=15)
buttonGetPosition.grid(row=4, column=5)
buttonGetPosition.configure(state='disabled')
# ************************************************************************************#


root.mainloop()
