#-*-coding:utf-8-*-
'''
Author shaojun_yang@zhbojay.com && tony_dong@zhbojay.com
V1.0   2019/9/9
for zebra device
'''
import clr
import re
import time
import binascii
import platform

#**********Interop.CoreScanner.dll****************#
# Zebradll = ctypes.cdll.LoadLibrary
# Zebradll("CoreScanner.dll")
# from CoreScanner import *
# instance = CCoreScannerClass()
# print dir(instance)
#**********Interop.CoreScanner.dll****************#
clr.FindAssembly('BojayScanner.dll')
from BojayScanner import *
instance = CoreScannerClass()

# auto get python interpreter
Interpreter = platform.python_version()[0]
print(Interpreter)

class BojayScannerClass:

    # open scanner device
    def OpenDevice(self):
        instance.OpenScanner()

    # close scaner device
    def CloseDevice(self):
        instance.CloseScanner()

    # pull trigger and get data
    def PullTriggerAndGetData(self,timeout = 10):
        content = instance.PullTrigger(timeout)
        if content == 'Register event for barcode fail' or content == 'timeout':
            return -1
        print(content)
        pattern = re.compile(r'<datalabel>(.*?)</datalabel>', re.S)
        results = re.findall(pattern, content)
        if Interpreter == '3':
            results = re.sub('\'|\[|]', '', str(results))
        else:
            results = re.sub('\'|\[u|]' , '',str(results))
        results = results.split(' ')
        data = b''
        for index in range(len(results)):
            strTemp = (results[index].strip())[2:]
            if Interpreter == '3':
                data = data + binascii.unhexlify(strTemp)
            else:
                data = data + binascii.unhexlify(strTemp)
        if Interpreter == '3':
            data = data.decode()
            # add some check for QCMC
            strData = str(data)
            strData.upper()
            if len(strData) < 17:
                return 'error: sn is too short'
            elif len(strData) == 17 and strData[0] == 'W' and strData[0] == 'I' and strData[0] == 'P':
                strData = strData + '\r\n'
                return strData
            elif len(strData) == 18 and strData[1] == 'W' and strData[2] == 'I' and strData[3] == 'P' and strData[0] == 'B':
                strData = strData + '\r\n'
                return strData
            else:
                return 'error:sn is not correct'
        return data

    # release trigger
    def ReleaseTrigger(self):
        ret = instance.ReleaseTrigger()
        if ret != 0:
            return -1
        return 0

if __name__ == '__main__':
    api = BojayScannerClass()
    api.OpenDevice()
    print(api.PullTriggerAndGetData(10))
    print(api.ReleaseTrigger())
    api.CloseDevice()