import serial
import time
import sys
import platform
FILENAME = sys.argv[0]
Command = FILENAME.split(".")[0]+"\n"
print(Command)
PyVersion =  int(platform.python_version()[0])
if PyVersion == 3:
	COMMAND = Command.encode('utf-8')
print(COMMAND)

ser = serial.Serial("COM8",115200)
ret = ser.write(COMMAND)
timeout = 30
while(timeout):
	ret = ser.read_all()
	if PyVersion == 3:
		ret = ret.decode()
	if len(ret) > 2 and ret[0] == 'O' and ret[1] == 'K':
		print(ret)
		break
	if Command.strip("\n") in ret:
		print(ret)
		break
	else:
		timeout=timeout - 1
		time.sleep(1)