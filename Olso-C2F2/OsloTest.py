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

# Author: Deepak Agarwal (deepakag@google.com) / Lin Gao (gaolin@google.com)

#--------------------------------------------------------------------------
#Script change history
#--------------------------------------------------------------------------
#Version:xxx
#Change desciption:
# - xxxxxxxxxxxxxxx
#--------------------------------------------------------------------------
#Version: C2F2_Oslo_20190523_04
#- Update to implement impulse test
#--------------------------------------------------------------------------
#Version: C2F2_Oslo_20190518_03
#- Update Oslo data tunneling address for DVT
#- Update oslo module information data recording base on the new role
#-   new-role >> C2: remove directly, F2: use LC and DC, not Oslo Board anymore
#--------------------------------------------------------------------------
#Version: C2F2_Oslo_20190514_02
# - Update the device_type auto generate base on new role (G5 is for C2 and G6 is for F2)
# - Implement one more command before data tunelling base on Software Kris's recommendation
#--------------------------------------------------------------------------
#Version: C2F2_Oslo_20190508_01
# - Rebase for DVT build of C2F2, clear some useless code
#--------------------------------------------------------------------------

__ver__ = 'C2F2_Oslo_20190523_04'

import os, csv
import subprocess as sub
import logging, shutil
import time
from datetime import datetime
from clifford.names import *
import config
from measurement_limits import MeasurementLimitsCollection
import FP_DutSWControl
import StationTestControl
import re
from os.path import expanduser

"""
C2F2 Oslo control Test Station Clifford SW Code for factory manufacturing.
Usage: python OsloTest.py --config-file Production_OsloTest.yaml
"""

global homedir
homedir = expanduser("~")

time_stamp = (datetime.now().strftime('_%m-%d-%Y_%H-%M-%S').strip())
log_filename = '.Oslo_test' + time_stamp + '.log'
logging.basicConfig(filename = log_filename, filemode='w')
logger = logging.getLogger("OsloTest.log")
handler = logging.StreamHandler()
formatter = logging.Formatter('[%(asctime)s] %(name)-5s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

# Misc settings from config file
conf.Declare('ports', description='device_ports')
conf.Declare('output_path', description='output folder path for data')
conf.Declare('limit_file', description='limit file for Oslo')

mode = conf.test_mode.strip().lower()

list_serial = []
list_usb = []
list_channel = []

def get_device_type():
    device_type = ''
    station_define_file = os.path.join(homedir, config.station_id_define)
    try:
        with open(station_define_file, 'r') as file:
            file_content = file.readlines()
            for line in file_content:
                item_content = line.strip().split('=')
                if item_content[0] == 'PROJECT_ID':
                    product_name = item_content[1].strip()
                    logger.debug('product_name %s' % product_name)
                if item_content[0] == 'STATION_ID':
                    station_id = item_content[1].strip()
                    logger.debug('station_id %s' % station_id)
                else:
                    continue
    except Exception:
        logger.error('Fail to find station_id')
        device_type = ''
        return device_type

    logger.info('station_id: %s, product_name:%s' % (station_id, product_name))

    if config.c2_station_id in station_id:
        if product_name == 'C2':
            device_type = 'coral'
        else:
            logger.warning('Project ID mismatch with station_id')
            device_type = ''
    elif config.f2_station_id in station_id:
        if product_name == 'F2':
            device_type = 'flame'
        else:
            logger.warning('Project ID mismatch with station_id')
            device_type = ''
    else:
        logger.error('unknown station_id!!!')
        device_type = ''

    logger.info('device_type: %s' % device_type)
    return device_type

def check_channel():
    """ Check connected USB devices port ID"""
    global list_serial, list_usb, list_channel
    # restart adb as root
    adb_out = sub.call(['adb', 'root'])
    logger.debug('adb root output: %s' % adb_out)
    # read in device serial numbers for later assignment
    startTime = time.time()
    while time.time() - startTime < 10:
        p = sub.Popen("adb devices -l|awk '{print $1,$3}'", shell=True, stdout=sub.PIPE,
                      stderr=sub.PIPE)
        data, err = p.communicate()
        sns = data.splitlines()[1:]
        logger.debug(sns, err)
        for item in sns:
            lines = item.split("usb:")
            if lines[0].strip() != "":
                list_serial.append(lines[0].strip())
                list_usb.append(lines[1].strip())
        if "no devices/emulators found" not in err:
            break
    return bool(list_serial) and bool(list_usb) and bool(list_channel)


def inittest(reason):
    """ Initialize test phase
    :param
    reason: return Clifford reason if inittest fail
    :return: True
    """
    global output, output_usb_port
    output = []
    output_usb_port = []
    logger.debug("inittest() called.")
    reason['reason'] = 'Init start!'
    cmd = 'adb devices -l'
    p = sub.Popen(cmd, shell=True, stdout=sub.PIPE, stderr=sub.PIPE)
    stdout, stderr = p.communicate()
    result = stdout.split('\n')
    result = result[1:-2]
    logger.debug('adb devices connected list: %s%s' % (stdout, stderr))
    for x in result:
        x = x.split()
        output.append(x[0])
        output_usb_port.append(x[2].split("usb:")[1])
    failure_code = None
    return True


def getsn(index):
    """ Read device SN from USB port list"""
    try:
        sn = ''
        dut_index = 'dut_' + str(index + 1)
        print '******************', conf.ports[dut_index]
        for i in range(len(output_usb_port)):
            logger.debug(output_usb_port[i])
            print conf.ports[dut_index]
            if output_usb_port[i] == conf.ports[dut_index]:
                sn = output[i]
                # logger.info('sn is: %s' % sn)
        for i in range(len(output_usb_port)):
            if output_usb_port[i] == conf.ports[dut_index]:
                sn = output[i]
        return sn
    except IndexError:
        err_msg = "getsn: No serial number found for thread %d." % index
        logger.error(err_msg)
        return None


def dummyvalidator(value):
    return True


def passfailvalidator(value):
    """ dummy pass/fail validator"""
    result = False
    if value:
        result = True
    return result


class AdbConnectionException(Exception):
    """ raise exception when adb connection fails"""

global device_type
device_type = get_device_type()

@TestPhase(timeout_s=50)
@measures(Measurement('device_sw').Doc('device sw version').WithValidator(dummyvalidator),
          Measurement('dut_slot_num').Doc('DUT slot number on the fixture').InRange(0,2),
          Measurement('device_config').Doc('Device build config').WithValidator(dummyvalidator),
          Measurement('oslo_module_config').Doc('Oslo module information').WithValidator(dummyvalidator))
def get_initial_status(test_data):
    """ Initial phase, get initial values. """
    # Create output folder    
    curr_time = (datetime.now().strftime('_%m-%d-%Y_%H-%M-%S').strip())
    test_data.logger.info('initial status test phase start time: %s' % curr_time)
    test_data.state['curr_time'] = curr_time
    test_data.state['source_dir'] = os.path.join(homedir, config.src_path)

    test_data.state['dut_folder'] = test_data.state['dut_id'] + test_data.state['curr_time']
    test_data.state['output_folder'] = os.path.join(homedir, config.data_path, test_data.state['dut_folder'])
    if not os.path.exists(test_data.state['output_folder']):
        origmask = os.umask(0)
        os.makedirs((test_data.state['output_folder']), 0775)
        os.umask(origmask)
    test_data.logger.info('Output folder: %s' % test_data.state['output_folder'])

    test_data.state['channel'] = 0
    test_data.logger.info('SN: %s Channel: %s' % (test_data.state['dut_id'], test_data.state['channel']))

    # device initial
    test_data.logger.info('Sending device initial command..')
    adb_out = sub.call(['adb', '-s', test_data.state['dut_id'], 'root'])
    adb_out = sub.call(['adb', '-s', test_data.state['dut_id'], 'remount'])
    adb_out = sub.call(['adb', '-s', test_data.state['dut_id'], 'shell', 'device_initial'])
    test_data.logger.debug(adb_out)
    time.sleep(0.5)
    # Read battery level
    battery_lvl = sub.check_output(['adb', '-s', test_data.state['dut_id'], 'shell', 'battery',
                              'getcapacity', '|', 'grep', 'Capacity']).split('=')[1].strip()
    test_data.logger.info('battery level is: %s' % battery_lvl)

    device_sw = sub.check_output(['adb', '-s', test_data.state['dut_id'], 'shell', 'getprop', 'ro.build.id'])
    test_data.logger.debug('device SW ver is: %s' % str(device_sw))
    test_data.UpdateSoftwareVersion(fw_ver=device_sw.strip())

    test_data.measurements.device_sw = str(device_sw.strip())           #update 04032019 for SFC system cannot parsing \n
    test_data.measurements.dut_slot_num = 0

    # Query Device config from Shop floor
    if (mode == 'production'):
        result, message = test_data.GetDUTData(test_data.state['dut_id'])
        test_data.logger.info(result)
        test_data.logger.info(message)
        if result == 'PASS':
            device_config = message['DEVICE_CONFIG'].encode('ascii')
            test_data.measurements.device_config = device_config
            global device_type
            test_data.logger.info('device type %s' % device_type)
            if device_type.strip() == 'coral':
                #oslo_module = message['P-Sensor'].encode('ascii')         
                oslo_module = 'None'                                         #DVT updates since C2 do not have that kind of Oslo information
            elif device_type.strip() == 'flame':
                oslo_module = message['OSLO Board'].encode('ascii')
                #oslo_module_dc = message['DC'].encode('ascii')
                #oslo_module_lc = message['LC'].encode('ascii')
                #oslo_module = str(oslo_module_dc) + '_' + str(oslo_module_lc)
            else:
                oslo_module = 'N/A'
            test_data.logger.debug('oslo module config %s' % oslo_module)
            test_data.measurements.oslo_module_config = oslo_module
        else:
            test_data.logger.info('Query device information from SFC fail, set device_config to N/A')
            test_data.measurements.device_config = 'N/A'
    else:
        test_data.logger.info("Test runs under debug, reliability or others, no need SFC query!!")
        test_data.measurements.oslo_module_config = 'None'
        test_data.measurements.device_config = 'None'


    test_data.logger.info('get_initial_status() complete.')

@TestPhase(timeout_s=10)
@measures(Measurement('oslo_ping_test').Doc('Oslo ping alive test').WithValidator(passfailvalidator))
def oslo_ping_test(test_data):
    """ Oslo Ping Test phase """
    ping_test = sub.check_output(['adb', '-s', test_data.state['dut_id'], 'shell', 'oslo_config_test', '-p', '3'])
    test_data.logger.debug('Oslo ping test result: %s' % ping_test)
    if 'PASS' in ping_test:
        test_data.measurements.oslo_ping_test = True
    else:
        test_data.measurements.oslo_ping_test = False
        raise ValueError("Oslo Ping test failed!!")

    ### find Oslo spi port number ###
    test_data.state['spi_port'] = ''
    spi = sub.check_output(['adb', '-s', test_data.state['dut_id'], 'shell', 'ls', '/d/iaxxx'])
    test_data.logger.info('found spi bus port id: %s' % spi)
    spi_portlist = re.findall(r'[spi]\w+[\.]\d+', spi)

    if len(spi_portlist) == 1:
        test_data.state['spi_port'] = spi_portlist[0]
    else:
        raise ValueError('Oslo spi bus port not found! Exiting..')

    ### wait for Athletico to start ###
    cmd = "adb -s {0} shell 'echo 0x0d000008 > /d/iaxxx/{1}/address'".format(test_data.state['dut_id'],
                                                                             test_data.state['spi_port'])
    os.system(cmd)
    cmd = "adb -s {0} shell 'echo 1 > /d/iaxxx/{1}/count'".format(test_data.state['dut_id'],
                                                                  test_data.state['spi_port'])
    os.system(cmd)
    curr_time = time.time()
    sensor_status = False
    while (time.time() - curr_time < 3):
        value = sub.check_output(['adb', '-s', test_data.state['dut_id'], 'shell', 'cat',
                                  '/d/iaxxx/{}/data'.format(test_data.state['spi_port'])])
        test_data.logger.debug('sensor spi bus data is: %s' % value)
        if value.strip() == "0D000000: -------- -------- 00000001":
            sensor_status = True
            break
        else:
            time.sleep(0.1)
            test_data.logger.debug('retrying the cmd: %s' % cmd)
            cmd = 'adb -s {} shell oslo_config_test -r 1'.format(test_data.state['dut_id'])
            os.system(cmd)
    if not sensor_status:
        test_data.logger.error('Sensor fail to start..Exiting!!')
        raise ValueError('Sensor fail to start..Exiting!!')

    config_command = "adb -s {0} shell oslo_config_test -s plugin_set_host -v 1".format(test_data.state['dut_id'])
    test_data.logger.debug('config command %s' % config_command)
    os.system(config_command)
    cmd = "adb -s {0} shell oslo_config_test -s plugin_mode -v 3".format(test_data.state['dut_id'])
    test_data.logger.debug('config command %s' % cmd)
    os.system(cmd)
    #new command from DVT, the command that will turn off slpy automatic config switching
    slpy_config_command = "adb -s {0} shell oslo_config_test -s plugin_slpy_state -v 0".format(test_data.state['dut_id'])
    test_data.logger.debug('config command %s' % slpy_config_command)
    os.system(slpy_config_command)


def build_measurements(phasename):
    """ Build list of Measurements for Functional Test.
    Args:
      phasename: phasename of the the measurements
    Return:
      meas_list: List of Clifford test measurements
    """
    meas_list = []
    product = ''
    global device_type
    logger.debug(device_type)
    if device_type.strip() == 'flame':
        product = 'F2'
    elif device_type.strip() == 'coral':
        product = 'C2'
    limits_collection = MeasurementLimitsCollection(
        selector_columns=['product', 'sku', 'test_mode', "phase_name", "measurement_name"],
        selection_rules=[['product', 'sku', 'test_mode', 'phase_name', 'measurement_name'],
                         ['product', 'sku', 'phase_name', 'measurement_name'],
                         ['test_mode', 'phase_name', 'measurement_name'],
                         ['phase_name', 'measurement_name'],
                         ['test_mode', 'phase_name', 'measurement_name'],
                         ['phase_name', 'measurement_name']])
    logger.debug(os.path.join(homedir, config.src_path, config.limit_file))
    limits_collection.load(os.path.join(homedir, config.src_path, config.limit_file))
    print("Limits file version = {0}".format(limits_collection.get_version()))
    global __specsVer__
    __specsVer__ = limits_collection.get_version()
    phase_limits = limits_collection.get(phase_name=phasename, product=product, test_mode=mode)

    for limits in phase_limits:
        meas_list.append(Measurement(limits.measurement_name).InRange(limits.low_limit, limits.high_limit))
    limits_collection.destroy()
    return meas_list

@TestPhase(timeout_s=1000)
@measures(*build_measurements('oslo_test'))
def oslo_test(test_data):
    """ Oslo Test Phase
        Rotates DUT, Moves target Motor, Trigger sensor and data capture, Analyze data
        Calls StationTestControl, FP_DutSWControl, oslo_apk_control
    """
    try:
        #### Bojay controller initialize ####
        test_data.logger.info("Iniitial Fixture motor controller...")
        bojay_controllerPort = config.portID['fixture_controllerPort']
        test_data.logger.debug(bojay_controllerPort)
        test_obj = test_data.state['test']
        StationTestControl.initialize(bojay_controllerPort)

        test_data.logger.info("Calling StationTestControl moveDUTHolder")
        test_data.logger.info("######## Test in running..... #######")
        
        StationTestControl.moveDUTHolder(config.dut_test_loc['dut_traj'], config.target_test_loc['target_traj'],
                                         config.motors_id['dut_motor2'], config.dut_pos['90deg'],
                                         config.motors_id['target_motor'],
                                         config.motors_id['dut_motor1'], config.dut_pos['angle'],
                                         test_data.state['output_folder'])
      
        test_data.logger.info("Parsing the data")
        parsed_data, calibration_data = FP_DutSWControl.parsedata(test_data.state['output_folder'])
        test_data.logger.debug("output data: %s" % str(parsed_data))
        test_data.logger.debug("calibration data: %s" % str(calibration_data))
        test_data.logger.info('writing the measurements')

        for metric, value in parsed_data.items():
            for position, data in value.items():
                for channel in range(len(data)):
                    test_data.measurements[position + '_' + metric + '_Rx' + str(channel)] = parsed_data[metric][position][channel]
        test_data.state['parse_data'] = parsed_data

        for metric, value in calibration_data.items():
            for position, data in value.items():
                for channel, (Ival, Qval) in enumerate(zip(data, data[1:])[::2]):
                    test_data.measurements[position + '_' + metric + '_Rx' + str(channel) + '_Ival'] = Ival
                    test_data.measurements[position + '_' + metric + '_Rx' + str(channel) + '_Qval'] = Qval
        test_data.state['cal_data'] = calibration_data
        test_data.logger.info('oslo_test() complete.')

    except Exception, e:
        test_data.logger.error('Exception in oslo_test phase: %s' % str(e))

@TestPhase(timeout_s=100)
@measures(Measurement('cal_file_check').WithValidator(dummyvalidator))
def oslo_cal_write(test_data):
    """ Test phase to write calibration data to the device """
    MODE_PRESENCE = config.device_calibration_config['presence_mode']
    MODE_REACH = config.device_calibration_config['reach_mode']
    VERSION = config.device_calibration_config['version']                                  #Add version record from EVT1.1 build, change from bugnizer#126888604

    calibration_data = test_data.state['cal_data']
    if mode != 'reliability':
        presence_cal_data = ' '.join(str(x) for x in (calibration_data['cal_coeffs']['ele_Target_1.0_Angle_Boresight']))
        reach_cal_data = ' '.join(str(x) for x in (calibration_data['cal_coeffs']['ele_Target_0.4_Angle_Boresight']))

        presence_cal_cmd = 'adb shell "oslo_config_test -c \'V:{} M:{} {}\'"'.format(VERSION, MODE_PRESENCE, presence_cal_data)
        reach_cal_cmd = 'adb shell "oslo_config_test -c \'V:{} M:{} {}\'"'.format(VERSION, MODE_REACH, reach_cal_data)
        test_data.logger.info('presence_cal_cmd : {}'.format(presence_cal_cmd))
        test_data.logger.info('reach_cal_cmd : {}'.format(reach_cal_cmd))
        os.system(presence_cal_cmd)
        os.system(reach_cal_cmd)

    # Post cal Check file exists in device /persist folder
    test_data.logger.debug('Checking post cal file..')
    adb_out = sub.check_output(['adb', '-s', test_data.state['dut_id'], 'shell', 'cat', '/persist/oslo/oslo.cal']).strip()
    if not 'Mode:' in adb_out:
        test_data.measurements.cal_file_check = False
    else:
        test_data.measurements.cal_file_check = True

#Implement from EVT1.1 build
@TestPhase(timeout_s=300)
@measures(*build_measurements('oslo_saturation_test'))
def oslo_saturation_test(test_data):
    """ Oslo Saturation Test Phase
        Check the saturation of Boresight only for both presence and reach mode
    """
    test_data.logger.info("Parsing Saturation the data")
    try:
        saturation_data = FP_DutSWControl.parse_saturation_data(test_data.state['output_folder'])
        test_data.logger.info("output data: %s" % str(saturation_data))

        for metric, value in saturation_data.items():
            for position, data in value.items():
                for channel in range(len(data)):
                    test_data.measurements[position + '_' + metric + '_Rx' + str(channel)] = saturation_data[metric][position][channel]

        test_data.logger.info('oslo_saturation_test() complete.')

    except Exception, e:
        test_data.logger.error('Exception in oslo_saturation_test phase: %s' % str(e))

#Implement from DVT build
@TestPhase(timeout_s=300)
@measures(*build_measurements('oslo_impulse_test'))
def oslo_impulse_test(test_data):
    """ Oslo Impulse Test Phase
        Check the impulse for all positions
    """
    test_data.logger.info("Parsing Impulse the data")
    try:
        impulse_data, chirps_data = FP_DutSWControl.parse_impulse_data(test_data.state['output_folder'])
        test_data.logger.info("output data: %s" % str(impulse_data))
        test_data.logger.info("output data: %s" % str(chirps_data))

        for metric, value in impulse_data.items():
            for position, data in value.items():
                for channel in range(len(data)):
                    test_data.measurements[position + '_' + metric + '_Rx' + str(channel)] = impulse_data[metric][position][channel]

        for metric, value in chirps_data.items():
            for position, data in value.items():
                for channel in range(len(data)):
                    test_data.measurements[position + '_' + metric] = chirps_data[metric][position][0]

        test_data.logger.info('oslo_impulse_test() complete.')

    except Exception, e:
        test_data.logger.error('Exception in oslo_impulse_test phase: %s' % str(e))

@TestPhase(timeout_s=100)
@measures(*build_measurements('oslo_validate_test'))
def oslo_validate_test(test_data):
    # Calibration coefficients validation, new test items implemented from EVT1.1 
    data = test_data.state['parse_data']
    Boresight_Target_500_channel0 = data['phase']['ele_Target_0.4_Angle_Boresight'][0]
    Boresight_Target_500_channel3 = data['phase']['ele_Target_0.4_Angle_Boresight'][2]
    test_data.logger.info('500 channel0 %f' % Boresight_Target_500_channel0)
    test_data.logger.info('500 channel3 %f' % Boresight_Target_500_channel3)
    #Lin add for angle delta correction
    diff_500 = (Boresight_Target_500_channel0 - Boresight_Target_500_channel3) % 360
    if (diff_500 >= 180):
        diff_500 = 360 - diff_500
    delta_target_500 = diff_500
    #end of angle correction 04032019
    test_data.measurements['Angle_Delta_Boresight_Target_500'] = delta_target_500
    test_data.logger.info('Angle Delta at 500mm %d' % delta_target_500)

    Boresight_Target_600_channel0 = data['phase']['ele_Target_0.6_Angle_Boresight'][0]
    Boresight_Target_600_channel3 = data['phase']['ele_Target_0.6_Angle_Boresight'][2]
    test_data.logger.info('600 channel0 %f' % Boresight_Target_600_channel0)
    test_data.logger.info('600 channel3 %f' % Boresight_Target_600_channel3)
    #angle correction
    diff_600 = (Boresight_Target_600_channel0 - Boresight_Target_600_channel3) % 360
    if (diff_600 >= 180):
        diff_600 = 360 - diff_600
    delta_target_600 = diff_600
    #end angle correction 04032019
    test_data.measurements['Angle_Delta_Boresight_Target_600'] = delta_target_600
    test_data.logger.info('Angle Delta at 600mm %d' % delta_target_600)

    #angle_delta = abs(delta_target_600) - abs(delta_target_500)
    angle_delta = max(delta_target_600, delta_target_500) - min(delta_target_600, delta_target_500)
    test_data.measurements['Calibration_Boresight_Angle_Delta'] = angle_delta
    test_data.logger.info('Calibration Boresight Angle Delta  %d' % angle_delta)
    #end Calibration coefficients validation

def csv_fwrite(dutfolder, filename_prefix, data):
    """ Function to write the raw data into a csv file 
    Args:
      dutfolder: folder name to write csv file
      filename_prefix: Test metric as filename
      data: raw data values to write
    """
    rawdatafile = os.path.join(config.data_path, dutfolder, filename_prefix + '.csv')
    # test_data.logger.info("output csv filename: %s" % rawdatafile)
    if not os.path.isfile(rawdatafile):
      csv_datafile = csv.writer(open(rawdatafile, 'a+'))
      csv_datafile.writerow(data.keys())
    csv_datafile = csv.writer(open(rawdatafile, 'a+'))
    # csv_datafile.writerow(data.keys())
    csv_datafile.writerows(zip(*data.values()))


def teardown(test_data):
    """ Teardown at end of test """
    teardown_starttime = time.time()
    global failure_code
    failure_code = None
    test_data.logger.info('Running teardown.')
    attachments(test_data)
    test_obj = test_data.state['test']
    num = test_obj.GetNumTestingDUT()
    test_data.logger.info('Number of DUTs: %s' % str(num))
    testphases_results = test_data.GetTestResult()
    test_data.logger.info(testphases_results)                   # display phase result at GUI
    adb_out = sub.call(['adb', '-s', test_data.state['dut_id'], 'shell', 'device_initial'])

    #remark off due to SFC do not support error code analysis, report from bug#125128974
    '''
    if failure_code is None:
        for item in test_data.test_record.phases:
            if testphases_results[item.name] != 'PASS':
                failure_code = item.name
                test_data.logger.debug("failure code: %s" % failure_code)
                test_data.SetFailureCode(failure_code)
                break
            else:
                test_data.SetFailureCode('NOERR')
    '''
    #Start station_bits write
    test_obj = test_data.state['test']
    Station_id = test_obj.station_id
    all_phase_results = test_data.GetTestFinalResult()
    command_string = '/vendor/bin/station_bits --station ' + Station_id + ' --setresult ' + all_phase_results + ' --timestamp ' + str(int(time.time()))
    stationbits_command = 'adb shell ' + command_string
    test_data.logger.debug(stationbits_command)
    os.system(stationbits_command)
    os.system('adb shell sync')
    # end of the station_bits write
    # Lin Gao add on 0411 for oslo ping fail bugreport auto capture
    test_data.logger.debug ('oslo ping result %s' % testphases_results['oslo_ping_test'])
    if (testphases_results['oslo_ping_test'] != 'PASS'):
        test_data.logger.info('Oslo ping test fail, need save bugreport')
        bugreport = 'adb bugreport ' + test_data.state['output_folder']
        test_data.logger.info(bugreport)
        os.system(bugreport)
    #end auto bugreport capture
    failure_code = None
    test_data.logger.info('teardown test phase exec time: %s\n' % (time.time() - teardown_starttime))

def cleanup():
    """ Delete files"""
        
def attachments(test_data):
    """Attachment phase.
  Arg:
    test_data: passed in by Clifford
  """
    try:
        test_data.logger.info('Zipping results.')
        cmd = 'mv ' + os.path.join(homedir, config.src_path, 'OsloTestLog.log') + ' ' + test_data.state['output_folder']
        os.system(cmd)
        # get name of output zip file, including path
        output_zip_name = test_data.state['output_folder']
        # make output zip
        test_data.state['output_zip'] = shutil.make_archive(output_zip_name, 'zip', test_data.state['output_folder'])
        test_data.logger.info('Output zip created: %s' % test_data.state['output_zip'])

        # if not local, upload to database
        if conf.test_mode != 'local':
            test_data.logger.info('Uploading zip to database.')
            test_data.AttachFromFile(test_data.state['output_zip'])
            os.remove(test_data.state['output_zip'])

    except KeyError:
        test_data.logger.error('Can not find output zip to attach!')
    except Exception, e:
        test_data.logger.error('Exception in attachment phase: %s' % e)


if __name__ == '__main__':
    test = clifford.Test(
        get_initial_status,
        oslo_ping_test,
        oslo_test,
        #oslo_validate_test,
        oslo_saturation_test,
        oslo_impulse_test,
        oslo_cal_write,
        attachments,
        test_name = 'OSLO',
        test_description = 'Oslo Test Station',
        test_version = __ver__,
        specs_version = __specsVer__)

    """ upload the test  result to data server and keep a local copy"""
    test.AddOutputCallback(UploadResultJSON)

    test.Configure(teardown_function=teardown, init_function=inittest, clean_function=cleanup)

    test.StartExecution(test_start=getsn)
