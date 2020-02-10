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

import serial
import time
import re
import os
import subprocess as sub
import logging

logger = logging.getLogger("oslo_apk_control")
handler = logging.StreamHandler()
formatter = logging.Formatter(
        '%(asctime)s %(name)-5s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

def apk_binary_version(devicesn, spi_port='spi4.0'):
  """ Read and return Oslo apk FW version """
  spi_portID = spi_port.split('.')[0]
  fw_version = sub.check_output(['adb', '-s', devicesn, 'shell', 'cat', '/sys/devices/platform/soc/a8c000.spi/spi_master/{0}/{1}/iaxxx/fw_version'.format(spi_portID,spi_port)])
  logger.debug('apk fw version is: %s' % str(fw_version))
  return fw_version

def config_load(devicesn, configname = 'presence'):
  """ Load config in apk and restart oslo_control to load config
  Args:
    devicesn: device serial number
    configname: presence or reach configs to load
  """
  mode = 'presence_v1'   #adding a _v1 comparing with EVT1.0 base on device software change
  if configname == 'reach':
      mode = 'reach_v1'
  #cmd = 'adb -s {} shell oslo_config_test -s plugin_slpy_state -v {}'.format(devicesn, mode)
  cmd = 'adb -s {} shell oslo_config_test -s config_factory_{} -v 1'.format(devicesn, mode)
  os.system(cmd)
  logger.debug(cmd)

def apk_start(devicesn):
  """ Start apk on the device using touch coordinates """
  logger.debug("Starting apk intent on the device")
  adb_out = sub.call(['adb', '-s', devicesn, 'root'])
  adb_out = sub.call(['adb', '-s', devicesn, 'shell',  'input dpad keyevent 4'])
  # dismiss Android system popup if it's there
  # adb_out = sub.call(['adb', '-s', devicesn, 'shell', 'input touchscreen tap 1214 1650'])
  # swipe to unlock
  adb_out = sub.call(['adb', '-s', devicesn, 'shell', 'input touchscreen swipe 815 2500 815 1000'])
  time.sleep(0.5)
  # start the apk
  adb_out = sub.call(['adb', '-s', devicesn, 'shell', 'am start -n com.android.test.soundtrigger/com.android.test.soundtrigger.SoundTriggerTestActivity'])
  time.sleep(0.5)
  logger.debug(adb_out)


def apk_load_start(devicesn):
  """ press load and press Start in apk """
  logger.debug("Press apk Load and start")
  # press load on apk
  adb_out = sub.call(['adb', '-s', devicesn, 'shell', 'input touchscreen tap 213 300'])
  time.sleep(2)
  # press start on apk
  adb_out = sub.call(['adb', '-s', devicesn, 'shell', 'input touchscreen tap 513 300'])
  time.sleep(0.5)

def apk_record_stop(devicesn):
  """ Press stop in apk to stop recording """
  logger.debug("press stop in apk to stop recording")
  adb_out = sub.call(['adb', '-s', devicesn, 'shell', 'input touchscreen tap 813 300'])
  time.sleep(0.5)

def apk_kill(devicesn):
  """ Kill apk at the end of test """
  logger.debug("kill apk at the end of test")
  adb_out = sub.call(['adb', '-s', devicesn, 'shell', 'am force-stop com.android.test.soundtrigger'])
  time.sleep(0.5)


# if __name__ == '__main__':
#   apk_binary_version('G000A50E1A6354817')
#   apk_config_load('G000A50E1A6354817')
#   apk_start('G000A50E1A6354817')
#   pk_kill('G000A50E1A6354817')
