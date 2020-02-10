#!/usr/bin/env python
# -*- coding: utf-8 -*-  

__version__ = 'v1.0.1'

# Changelog:
# 10/03/2019 v1.0.1: Initial release for new structure
# Author: Allen Huang (szulunhuang@google.com)

# libraries
from utils.common_library import *
from utils import connectedUSBdevices
from utils import fixture_control as fc
import test_spec

# test phases
from test_phases import *

# Clifford Configuration Declarations
conf.Declare('usb_ports', description='usb ports for DUTs')

# global variable
test_spec.sorted_sn = [None] * conf.num_unit
test_spec.sorted_wip_sn = [None] * conf.num_unit

def inittest(*args, **kwargs):
    print('{}: {} called'.format(datetime.now(), inspect.stack()[0][3]))
    # adb service
    os.system("adb start-server")

    # tester initialize
    """
    ret = fc.init_fixture()
    if ret:
        print("Can not connect to fixture, exiting")
        return False
    """

    # scan device
    i = 0
    while i <= test_spec.boot_wait_time:
        usb_map = connectedUSBdevices.ConnectedUSBDevices()
        usb_map.PopulateDeviceAndPortList()

        print("{0:>3} {1}".format(i, usb_map.Port_Device_Map))

        if len(usb_map.Port_Device_Map) == conf.num_unit:
            break
        else:
            i = i + 1
            time.sleep(1)

    # sort SN
    for index in range(0, conf.num_unit):
        sorted_port = conf.usb_ports[index]
        if sorted_port in usb_map.Port_Device_Map:
            test_spec.sorted_sn[index] = usb_map.Port_Device_Map[sorted_port]
            ret, err = adb(['shell', '/bin/fct/fct.sh', 'factory', 'serial', '-w'], dut_sn=test_spec.sorted_sn[index])
            #ret, err = adb(['shell', FCT_TOOL_PATH, 'get_serial', '-w'], dut_sn=als_spec.sorted_sn[index])
            if err:
                print("Can not get WIP SN on {}".format(test_spec.sorted_sn[index]))
                return False
            else:
                test_spec.sorted_wip_sn[index] = ret.decode().split()[0]
                #SORTED_WIP_SN[index] = ret.splitlines()[1]

    print("adb sn:", test_spec.sorted_sn)
    print("wip sn:", test_spec.sorted_wip_sn)

    if len(test_spec.sorted_sn) > 0:
        pass
        #fc.engage_fixture()

    return bool(len(test_spec.sorted_sn))


def test_start(index):
    return test_spec.sorted_wip_sn[index]


def teardown(test_data):
    print('{}: {} called'.format(datetime.now(), inspect.stack()[0][3]))
    test_data.logger.info('Test Finished !')
    print("teardown finished")


def cleanup(*args, **kwargs):
    print('{}: {} called'.format(datetime.now(), inspect.stack()[0][3]))
    # adb service
    os.system("adb kill-server")

    test_spec.sorted_sn = [None] * conf.num_unit
    test_spec.sorted_wip_sn = [None] * conf.num_unit

    #fc.reset_fixture()
    print("cleanup finished")


# test phases
test_phase = ["aux_initial", "pyd_basic",
              "aux_attach", "aux_environment", "aux_errorcode"]
test_list = []

for each_phase in test_phase:
    function_name = eval("{}.{}".format(each_phase, each_phase))
    print("Loading phase:", each_phase)
    test_list.append(function_name)

if __name__ == '__main__':
    test = clifford.Test(*test_list,
                         test_name=test_spec.test_name,
                         test_description='Touch test',
                         test_version=test_spec.__version__)

    # upload the test result to data server and keep a local copy
    # the local copy is at current_user_home/CliffordLog
    test.AddOutputCallback(UploadResultJSON)

    # add teardown function (destructor), which is guaranteed to be called at last.
    test.Configure(teardown_function=teardown, init_function=inittest, clean_function=cleanup)

    test.StartExecution(test_start=test_start)
