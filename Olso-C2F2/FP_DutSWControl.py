''' Test script to control and trigger Oslo capture on FP '''

import os, glob
from collections import defaultdict
import matplotlib.pyplot as plt
import numpy as np
import itertools
import time
import logging
import config
import subprocess as sub
from os.path import expanduser

logger = logging.getLogger("DutSWControl.log")
handler = logging.StreamHandler()
formatter = logging.Formatter(
        '%(asctime)s %(name)-5s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

oslo_device_dir = '/data/data/'

global homedir
homedir = expanduser("~")

LOCAL_DATA_DIR = os.path.join(homedir, config.data_path)
LOCAL_SRC_DIR = os.path.join(homedir, config.src_path)
analysis_dir = LOCAL_DATA_DIR

if not os.path.exists(LOCAL_DATA_DIR):
    origmask = os.umask(0)
    os.makedirs((LOCAL_DATA_DIR), 0775)
    os.umask(origmask)

def capturerecord(filename, foldername, fileext = '.pcm'):
    """ capture record data in the device """
    oslo_device_file = oslo_device_dir + filename
    logger.debug(oslo_device_file)
    osloCommand = 'adb shell tunneling_hal_test 0 1 {} 0x3260 1 0 -f '.format(config.capture_duration) + filename + \
                  fileext
    logger.debug(osloCommand)
    os.system(osloCommand)
    synccommand = 'adb shell sync'
    logger.debug(synccommand)
    os.system(synccommand)

    temp = os.path.join(foldername, filename.split(fileext)[0])
    logger.info(temp)
    if not os.path.exists(temp):
        os.makedirs(temp)
    
    try:
        cmd = 'adb pull {0} {1}'.format(oslo_device_file + fileext, temp)
        out = sub.Popen(cmd,shell = True,stdout=sub.PIPE, stderr=sub.PIPE)
        stdout,stderr = out.communicate()
        logger.info(cmd) 
        logger.info(stdout)
        logger.info(stderr)
        if 'No such file or directory' in stdout:
            logger.error('Device .pcm file not found!')
            raise ValueError('Device .pcm file not found')
        os.system('adb shell rm {0}'.format(oslo_device_file + fileext))
        logger.debug('device file deleted..')
    except Exception, e:
        logger.error('Exception in pulling device file: %s' % str(e))

def impulse_DataAnalysis(filename, datafolder, fp=False):
    """ Impulse Data analysis on each data file """

    fileext = '.pcm'
    filename = filename + fileext
    logger.debug(filename)
    subdir = filename.split(fileext)[0]

    # copying the data file to a temp folder for analysis. current analysis script has a limitation on file path
    temp_dir = os.path.join(LOCAL_DATA_DIR, 'temp')
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
    cp_cmd = 'cp ' + os.path.join(datafolder, subdir, filename) + " " + temp_dir
    logger.info(cp_cmd)
    os.system(cp_cmd)

    if (filename == 'ele_Target_1.0_Angle_Boresight.pcm'):
        cmd = 'cat ' + os.path.join(temp_dir, filename) + ' | ' + os.path.join(LOCAL_SRC_DIR, 'AnalysisTool/demux_jaws') + ' 2> ' + '/dev/null' + ' | ' + os.path.join(LOCAL_SRC_DIR, 'AnalysisTool/impulse_detector_256') + ' 2> ' + '/dev/null' + ' > ' + os.path.join(temp_dir, 'impulse_results.txt')
    else:
        cmd = 'cat ' + os.path.join(temp_dir, filename) + ' | ' + os.path.join(LOCAL_SRC_DIR, 'AnalysisTool/demux_jaws') + ' 2> ' + '/dev/null' + ' | ' + os.path.join(LOCAL_SRC_DIR, 'AnalysisTool/impulse_detector_128') + ' 2> ' + '/dev/null' + ' > ' + os.path.join(temp_dir, 'impulse_results.txt')

    logger.info('Impulse data analysis command is: %s' % cmd)
    os.system(cmd)
    time.sleep(0.1)
    mv_cmd = 'mv ' + os.path.join(temp_dir, 'impulse_results.txt') + " " + os.path.join(datafolder, subdir + '/')
    os.system(mv_cmd)
    del_cmd = 'rm ' + os.path.join(temp_dir + '/*')
    os.system(del_cmd)

def saturation_DataAnalysis(filename, datafolder, fp=False):
    """ Saturation Data analysis on each data file """

    fileext = '.pcm'
    filename = filename + fileext
    logger.debug(filename)
    subdir = filename.split(fileext)[0]

    # copying the data file to a temp folder for analysis. current analysis script has a limitation on file path
    temp_dir = os.path.join(LOCAL_DATA_DIR, 'temp')
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
    cp_cmd = 'cp ' + os.path.join(datafolder, subdir, filename) + " " + temp_dir
    logger.info(cp_cmd)
    os.system(cp_cmd)

    cmd = os.path.join(LOCAL_SRC_DIR, 'AnalysisTool/p19_saturation_ver1 ') + os.path.join(temp_dir, filename) + " " + temp_dir

    logger.info('Saturation data analysis command is: %s' % cmd)
    os.system(cmd)
    time.sleep(0.1)
    mv_cmd = 'mv ' + os.path.join(temp_dir, 'results_2.txt') + " " + os.path.join(datafolder, subdir + '/')
    os.system(mv_cmd)
    del_cmd = 'rm ' + os.path.join(temp_dir + '/*')
    os.system(del_cmd)

def rawDataAnalysis(filename, datafolder, fp=False, binsize = 6, phase1=0, phase2=0, phase3=0):
    """ Data analysis on each data file """

    fileext = '.pcm'
    filename = filename + fileext
    logger.debug(filename)
    subdir = filename.split(fileext)[0]

    # 0 0 0 --> change to phase values from deg 0 (home position)

    # copying the data file to a temp folder for analysis. current analysis script has a limitation on file path
    temp_dir = os.path.join(LOCAL_DATA_DIR, 'temp')
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
    cp_cmd = 'cp ' + os.path.join(datafolder, subdir, filename) + " " + temp_dir
    logger.info(cp_cmd)
    os.system(cp_cmd)

    cmd = os.path.join(LOCAL_SRC_DIR, 'AnalysisTool/p19_linux_ver6 ') + os.path.join(temp_dir, filename) \
      + " " + temp_dir + " " + "{0} {1} {2} {3} 60.5 1 &".format(binsize, phase1, phase2, phase3)

    logger.info('data analysis command is: %s' % cmd)
    os.system(cmd)
    time.sleep(0.1)
    mv_cmd = 'mv ' + os.path.join(temp_dir, 'results.txt') + " " + os.path.join(datafolder, subdir + '/')
    os.system(mv_cmd)
    del_cmd = 'rm ' + os.path.join(temp_dir + '/*')
    os.system(del_cmd)

def parsedata(foldername):
    """ parse the results.txt files to return dictionary with measurements """
    logger.debug('parse data in folder: %s' % foldername) 
    deg_angle = sig_pow = noise_pow = snr = cc_ratio = temperature = phase = azi_angle = ele_angle = None
    data = defaultdict(dict)
    cal_data = defaultdict(dict)
    for rootdir, subdirs, fileList in os.walk(foldername):
        #logger.debug('parse data in rootdir: %s' % rootdir ) 
        for subdir in subdirs:
            head, tail = os.path.split(subdir)
            deg_angle = subdir #tail.split('_')[0].strip()
            datafiles = glob.glob(os.path.join(foldername, subdir, 'results.txt'))
            for filename in datafiles:
                #logger.debug('filename %s' % filename)
                with open(filename, 'r') as file_in:
                    lines = file_in.readlines()
                for line in lines:
                    #if 'signal_power' in line:
                    #    data['sig_power'][deg_angle] = map(float, line.split('=')[1].strip().split(','))
                    #if 'noise_power' in line:
                    #    data['noise_power'][deg_angle] = map(float, line.split('=')[1].strip().split(','))
                    if 'signal to noise ratio' in line:
                        data['snr'][deg_angle] = map(float, line.split('=')[1].strip().split(','))
                    #if 'cc_ratio' in line:
                    #    data['cc_ratio'][deg_angle] = map(float, line.split('=')[1].strip().split(','))
                    #if 'Temperature' in line:
                    #    data['temperature'][deg_angle] = map(float, line.split('=')[1].strip().split(','))
                    #if 'phase for each channel' in line:
                    #    data['phase'][deg_angle] = map(float, line.split('=')[1].strip().split(','))
                    #if 'azimuth angle' in line:
                    #    data['azi_angle'][deg_angle] = map(float, line.split('=')[1].strip().split(','))
                    #if 'elevation angle' in line:
                    #    data['ele_angle'][deg_angle] = map(float, line.split('=')[1].strip().split(','))
                    if 'calibration Coeffs' in line:
                        cal_data['cal_coeffs'][deg_angle] = map(float, line.split('=')[1].strip().split(','))
    logger.info('parsed data: %s' % data)
    logger.info('parsed data: %s' % cal_data)
    return data, cal_data

def parse_impulse_data(foldername):
    """ parse the impulse_results.txt files to return dictionary with measurements """
    logger.debug('parse data in folder: %s' % foldername)
    deg_angle = impulse = chirps = None
    chirps_data = defaultdict(dict)
    impulse_data = defaultdict(dict)
    for rootdir, subdirs, fileList in os.walk(foldername):
        for subdir in subdirs:
            head, tail = os.path.split(subdir)
            deg_angle = subdir #tail.split('_')[0].strip()
            datafiles = glob.glob(os.path.join(foldername, subdir, 'impulse_results.txt'))
            for filename in datafiles:
                #logger.debug('filename %s' % filename)
                with open(filename, 'r') as file_in:
                    lines = file_in.readlines()
                for line in lines:
                    if 'impulses' in line:
                        impulse_data['impulse'][deg_angle] = map(float, line.split(':')[1].strip().split(' '))
                    if 'chirps' in line:
                        chirps_data['chirps'][deg_angle] = map(int, line.split(':')[1].strip().split(' '))
    logger.info('parsed data: %s' % impulse_data)
    logger.info('parsed data: %s' % chirps_data)
    return impulse_data, chirps_data

def parse_saturation_data(foldername):
    """ parse the results_2.txt files to return dictionary with measurements """
    logger.debug('parse data in folder: %s' % foldername)
    deg_angle = None
    saturation_data = defaultdict(dict)
    for rootdir, subdirs, fileList in os.walk(foldername):
        for subdir in subdirs:
            head, tail = os.path.split(subdir)
            deg_angle = subdir #tail.split('_')[0].strip()
            if (deg_angle == 'ele_Target_0.4_Angle_Boresight' or deg_angle == 'ele_Target_1.0_Angle_Boresight'):
                datafiles = glob.glob(os.path.join(foldername, subdir, 'results_2.txt'))
                for filename in datafiles:
                    with open(filename, 'r') as file_in:
                        lines = file_in.readlines()
                        for line in lines:
                            if 'saturation percentage % ' in line:
                                saturation_data['saturation'][deg_angle] = map(float, line.split('=')[1].strip().split(','))
    logger.info('parsed data: %s' % saturation_data)
    return saturation_data

def plotdata(data, datalabel, output_folder):
    """ Plot the raw data for each metric"""
    ax = plt.subplot(111)
    plt.title(datalabel, fontsize=20)
    plt.xticks(np.arange(-100, 110, 20))
    plt.xlabel('Dut_angle', fontsize=15)
    plt.ylabel('Power(dB)', fontsize=15)
    ax.autoscale(enable=True, axis=u'both', tight=False)
    ax.grid(True)
    marker = itertools.cycle(('o', '^', '+', '*', 'v', "<"))
    colors = itertools.cycle(('r', 'g', 'b', 'k', 'c', 'm'))
    label = []
    target_pos = ''
    for key, value in data.iteritems():
        dut_pos = key.split('_')[0]
        xval = key.split('_')[-1]
        target_pos = key.split('_')
        target_pos = "_" + "_".join([target_pos[1], target_pos[2]]) + "_"
        for x in range(len(value)):
                legend = key.split('_')[0] + '_Rx' + str(x)
                # if len(value) <2:
                #     colors = itertools.cycle(('r', 'g'))
                plt.scatter([xval], value[x], marker=marker.next(),  c=colors.next(), s=25, label=key)
                if legend not in label:
                    label.append(legend)

    plt.legend(label,shadow = True,
        bbox_to_anchor=(1.1,1), loc="upper right", fontsize=10, scatterpoints=1)
    plt.savefig(os.path.join(output_folder, datalabel + target_pos + '.png'))
    
    plt.clf()


if __name__ == "__main__":
    filename = 'ele_Target_0.4_Angle_Boresight' 
    datafolder = '/oslo_test/EVT/data/91KBA01710_03-21-2019_11-24-33/'
    foldername = '/home/bojay/oslo_test/EVT/data/91KBA01710_03-21-2019_11-24-33/'
    #saturation_DataAnalysis(filename, datafolder, fp=False)
    #rawDataAnalysis(filename, datafolder, fp=False, binsize = 6, phase1=0, phase2=0, phase3=0)
    parsedata(foldername)
    parse_saturation_data(foldername)
