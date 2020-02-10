# config file for soli test fixture motors controls and serial connection

data_path = 'oslo_test/data'
src_path = 'oslo_test/source'
station_id_define = '.clifford_station.txt'
c2_station_id = 'G5'
f2_station_id = 'G6'

capture_duration = 1.5

limit_file = 'FATP_OsloTestSpecs.csv'

target_test_loc = {
    'target_traj': [1.0, 0.4]
}

dut_test_loc = {
    'dut_traj': ['ele', 'azi']
}

measurements = {
    # measurement metrics and list of metrics values length (Tx1, Tx2, Tx3)
    'metrics': {'sig_power':3, 'noise_power':3, 'snr':3, 'cc_ratio':3, 'phase':3, 'azi_angle':1, 'ele_angle':1, 'temperature':1, 'saturation':3}
}

portID = {
    'fixture_controllerPort': '/dev/ttyS1',
}

motors_id = {
    'target_motor': 3,
    'dut_motor1': 1,
    'dut_motor2': 2,
}

#special for Bojay z Axis design, when set to 0, the Z move to hight value as 810 far away from target
target_abs_pos = {
    '1.0': 0,                   #the max height between dut and target 800~810mm
    '0.4': 300,                 #actually the height between target and dut is 500mm = 800-300
    '0.6': 200,
   #'value_between_dut_target': abs_value_need_set_in_script
}

dut_pos = {
    'deg0': 0,
    '45deg': 45,
    '50deg': 50,
    '60deg': 60,
    '90deg': 90,
    '135deg': 135,
    '180deg': 180,
    'angle': 50,
}

binsize = {
    'presence': 26,
    'reach': 17,
    'validate': 20,             #height between target and dut is 600cm
}

device_calibration_config = {
    'presence_mode': 4,
    'reach_mode': 5,
    'version': 1.1,
}

doorsensor = {
    'ON': 25,
    'OFF': 26,
}

