# Copyright 2019 Google Inc. All Rights Reserved.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# !/usr/bin/python

import signal
import subprocess
import time
import os
import config
import FP_DutSWControl
import oslo_apk_control
import logging
from bojay_motor_control import GOEControlClass       #PLC controller CLASS for EVT Bojay fixture

""" P19 EVT Oslo Test station SW code """
""" Bojay motor, not Zebra motor """

logger = logging.getLogger("StationTestControl")
handler = logging.StreamHandler()
formatter = logging.Formatter(
        '%(asctime)s %(name)-5s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

def initialize(bojay_controllerPort):
    ''' Setting Home position for target motor 
    Args:
    bojay_controllerPort: bojay controller serial port
    '''
    global controllerPort
    logger.debug("Initializing Bojay controller serial port")
    controllerPort = GOEControlClass()                                              #new PLC controllder need open the serial port by separtely
    temp_result = controllerPort.OpenSerial(bojay_controllerPort)                   #open serial port, bojay_controllerPort is config at config.py
    if (temp_result == 0):
        logger.debug("Open serial port success")
        controllerPort.SetDoorSensor(config.doorsensor['ON'])         #turn on the fixture door sensor, make sure the door is closed before test start
        temp_result = controllerPort.GetDoorSensor()                  #add this check, making sure the fixture door closed before test
        if (temp_result == 0):
            raise ValueError("Fixture door is still open, test stop")
        temp_result_motor1 = controllerPort.SetSpeed(config.motors_id['dut_motor1'], 90)                #Set motor speed
        temp_result_motor2 = controllerPort.SetSpeed(config.motors_id['dut_motor2'], 90)                #max speed value for x, y is 500
        temp_result_targetmotor = controllerPort.SetSpeed(config.motors_id['target_motor'], 250)         #max speed value for z is 250
        if ((temp_result_motor1 or temp_result_motor2 or temp_result_targetmotor)):
            raise ValueError("Fail to set the motor speed.....x-Axis:%d, y-Axis:%d, z-Axis:%d" % temp_result_motor1, temp_result_motor2, temp_result_targetmotor)
        home_result_motor1 = controllerPort.MoveToCoordinates(config.motors_id['dut_motor1'], 0)
        home_result_motor2 = controllerPort.MoveToCoordinates(config.motors_id['dut_motor2'], 0)
        home_result_targetmotor = controllerPort.MoveToCoordinates(config.motors_id['target_motor'], 0)
        if ((home_result_motor1 or home_result_motor2 or home_result_targetmotor)):
            logger.debug('Fixture cannot move to home position, need soft reset...')
            reset_to_home = controllerPort.SignalReset()                                #reset the fixture to original positation, default timeout is 30s
            if (reset_to_home == 0):
                logger.debug("Fixture reset to home pos, done as success")
            else:
                raise ValueError("Fail to reset the fixture to home......x-Axis:%d, y-Axis:%d, z-Axis:%d" % home_result_motor1, home_result_motor2, home_result_targetmotor)
        logger.debug('Fixture initilize success, return to main thread....................')
    else:
        raise ValueError("Fail to open serial port %s" % bojay_controllerPort)

def ElevationPlaneMove(motor, motion_angle, target_pos, dut_pos, foldername, direction, binsize=6, phase1=0, phase2=0, phase3=0):
	""" Move DUT motor1 in elevation plane
	Args:
                motor: x/y/z axis for new PLC controller (Axis_x:1, Axis_y:2, Axis_z:3)
		motion_angle: angle motor need move to
		target_pos: position of target from DUT
		dut_pos: position of dut - azimuth or elevation
		foldername: file folder path
		direction: motor clockwise or anti-clockwise rotation
	"""
	logger.debug("ElevationPlaneMove function start")
	if motion_angle <= 50:
            if (direction == -1):
                start_angle = direction*motion_angle                    #-50 degree
                end_angle = motion_angle + 1                            #51 degree
            elif (direction == 1):
                start_angle = motion_angle                              #50 degree
                end_angle = -1*(motion_angle + 1)                       #-51 degree
            logger.debug("Start angle %s" % str(start_angle))
            logger.debug("End angle %s" % str(end_angle))
            for angle_in_test in range(start_angle, end_angle, direction*(-50)):                        # the loop value in range is -50, -30, -10, 10, 30, 50
                if (angle_in_test == -10):
                    logger.debug('Continue to next cycle.')            #remove -10 from loop
                    continue
                if (angle_in_test == 10):                                                               #correct the angle to 0
                    angle_in_test = 0
                logger.debug('angle in test after correction %d' % angle_in_test)

                if (angle_in_test == 0):
                    if (direction == -1):
                        filename = ('{}' + '_Target_{}_Angle_Boresight').format(dut_pos, target_pos)        #Here collect the calibration data at 0.4M
                    else:
                        logger.debug("Do nothing since Boresight do not need collect data twice......")
                        continue
                else:
                    filename = ('{}' + '_Target_{}_Angle_' + str(angle_in_test)).format(dut_pos, target_pos)
                #logger.debug("Output filename: %s" % filename)
                #logger.debug("motor %s debug here....." % motor)
                #logger.debug("angle %s debug here....." % angle_in_test)
                motor_action_result = controllerPort.MoveToCoordinates(motor, angle_in_test, timeout=10)     #default timeout is 10s, here the motor should be Axis_x
                if (motor_action_result == 0):
                    time.sleep(0.3)
                    FP_DutSWControl.capturerecord(filename, foldername)
                    FP_DutSWControl.rawDataAnalysis(filename, foldername, binsize=binsize, phase1=phase1, phase2=phase2, phase3=phase3)
                    FP_DutSWControl.impulse_DataAnalysis(filename, foldername)
                    if (filename == 'ele_Target_0.4_Angle_Boresight'):
                        FP_DutSWControl.saturation_DataAnalysis(filename, foldername)
                else:
                    raise ValueError("Motor:%s fail to control the fixture move to the correct position:%s, raise a error and test stop..." % motor, angle_in_test)

def AzimuthPlaneMove(motor, motion_angle):
    """ Rotate DUT in Azimuth plane
    Args:
	motor: motor2 serial port
	motion_angle: rotation motion angle
    """
    plan_move_result = controllerPort.MoveToCoordinates(motor, motion_angle)                        #the motion_angle for Oslo EVT test is 90 degree
    if (plan_move_result == 0):
        logger.debug("Azi plan move to correct position, success")
    else:
        raise ValueError("Azi(Y) motor move fail in %s, raise error and test stop...." % motion_angle)

def move_to_validate(dut_motor1, dut_motor1_pos, dut_motor2, dut_motor2_pos, target_motor, foldername):
    """
    Move the fixture to some position required by parameter
    Args:
        dut_motor1,2 and target_motor: the motor id
        dut_motor1_pos, dut_motor2_pos and target_pos: abs position for fixture
        foldername: the folder where store the output data
    """
    devicesn = os.path.split(foldername)[1].split('_')[0]
    phase1 = phase2 = phase3 = 0
    target_pos = 0.6          #hardcode the target pos here for pos-calibration validate test only
    dut_pos = 'ele'
    test_config = 'reach'
    if dut_motor2_pos == 90:
        dut_pos = 'azi'
    if target_pos >= 0.7:
        test_config = 'presence'

    logger.debug('Target motor pos %s' % target_pos)
    logger.debug('Target motor abs pos %s' % config.target_abs_pos[str(target_pos)])
    oslo_apk_control.config_load(devicesn, configname=test_config)
    targetmotor_move_result = controllerPort.MoveToCoordinates(target_motor, config.target_abs_pos[str(target_pos)])
    motor1_move_result = controllerPort.MoveToCoordinates(dut_motor1, dut_motor1_pos)
    motor2_move_result = controllerPort.MoveToCoordinates(dut_motor2, dut_motor2_pos)
    #logger.debug(motor1_move_result)
    #logger.debug(motor2_move_result)
    #logger.debug(targetmotor_move_result)

    if (not (motor1_move_result or motor2_move_result or targetmotor_move_result)):
        logger.debug("Move to correct position, success")
        filename = ('{}' + '_Target_{}_Angle_Boresight').format(dut_pos, target_pos)
        logger.debug('filename %s' % filename)
        time.sleep(0.3)
        FP_DutSWControl.capturerecord(filename, foldername)
        FP_DutSWControl.rawDataAnalysis(filename, foldername, binsize=config.binsize['validate'], phase1=phase1, phase2=phase2, phase3=phase3)
    else:
        raise ValueError("Motor move fail, error report from motor, test stopped!! x-Axis:%d, y-Axis:%d, z-Axis:%d" % motor1_move_result, motor2_move_result, targetmotor_move_result)

def moveDUTHolder(dut_traj, target_traj, dut_motor2, dut_Azi_angle, target_motor, dut_motor1, dut_Ele_angle, foldername):
	""" Move DUT holder Azimuth and Elevation positions """

	devicesn = os.path.split(foldername)[1].split('_')[0]
	logger.debug("moveDUTHolder: device sn is: %s" % devicesn)
	dutmotor_direction = -1

	for target_pos in target_traj:
            test_config = 'presence'
            target_motor_abs_pos = config.target_abs_pos[str(target_pos)]
            if target_pos == 0.4:
                test_config = 'reach'
            logger.debug('loading config--> %s' % test_config)
            oslo_apk_control.config_load(devicesn, configname=test_config)

            logger.debug("target_motor %s" % target_motor)
            logger.debug("target pos %s" % target_pos)
            logger.debug("target abs pos %s" % target_motor_abs_pos)

            target_move_result = controllerPort.MoveToCoordinates(target_motor, target_motor_abs_pos)  #directly move to the target pos
            if (target_move_result != 0):
                raise ValueError('Target(Z) Motor fail to move the target to the correct position %d, raise error and test stop...' % target_motor_abs_pos)

            time.sleep(0.5)                                   # per the real test on the fixture, Z Axis moved a little slow, add a sleep help making sure the Z Axis move the the correct position and stable

            phase1 = phase2 = phase3 = 0
            for dut_pos in dut_traj:
                logger.debug("dut_pos %s" % dut_pos)
                if (test_config == 'reach'):
                    if dut_pos == 'azi':
                        AzimuthPlaneMove(dut_motor2, dut_Azi_angle)
                        #time.sleep(2)
                    logger.debug('X motor rotational direction: %s' % str(dutmotor_direction))
                    ElevationPlaneMove(dut_motor1, dut_Ele_angle, target_pos, dut_pos, foldername, dutmotor_direction, config.binsize[test_config], phase1, phase2, phase3)
                    dutmotor_direction = -1 * dutmotor_direction # rotate the DUT Motor 1 in opposite direction (clockwise/anti clockwise)
                else:
                    if (dut_pos == 'ele'):
                        temp_result_motor1 = controllerPort.MoveToCoordinates(dut_motor1, 0)
                        temp_result_motor2 = controllerPort.MoveToCoordinates(dut_motor2, 0)
                        if (temp_result_motor1 or temp_result_motor2):
                            raise ValueError("Failed to move motor1:%d or motor2:%d to home position" % temp_result_motor1, temp_result_motor2)
                        logger.debug("Collect the calibration data at Target %s, dut position %s......" % (target_pos, dut_pos))
                        filename = ('{}' + '_Target_{}_Angle_Boresight').format(dut_pos, target_pos)
                        logger.debug('filename %s' % filename)
                        time.sleep(0.3)
                        FP_DutSWControl.capturerecord(filename, foldername)
                        FP_DutSWControl.rawDataAnalysis(filename, foldername, binsize=config.binsize[test_config], phase1=phase1, phase2=phase2, phase3=phase3)
                        FP_DutSWControl.impulse_DataAnalysis(filename, foldername)
                        FP_DutSWControl.saturation_DataAnalysis(filename, foldername)
        
        controllerPort.MoveToCoordinates(dut_motor1, 0)
        controllerPort.MoveToCoordinates(dut_motor2, 0)
        #remark **** Adding calibration cofficient at 0.6m after done Azi test ****
        #move_to_validate(config.motors_id['dut_motor1'], config.dut_pos['deg0'], config.motors_id['dut_motor2'], config.dut_pos['deg0'], config.motors_id['target_motor'], foldername)
        controllerPort.MoveToCoordinates(target_motor, 0)
        controllerPort.CloseSerial()                            #close serial port need remove to the last to the test if add validate test

if __name__ == '__main__':
    ElevationPlaneMove(2, 2, 50, 400, 0, '/home/gaolin', 1)
