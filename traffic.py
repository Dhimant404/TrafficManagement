import serial
import time
from distlib.compat import raw_input

ArduinoUnoSerial = serial.Serial('com5',9600)
print(ArduinoUnoSerial.readline())
print("You have new message from Arduino")


def traffic(var):
    #while 1:
        # var = raw_input()
        if var == '1':
            ArduinoUnoSerial.write(str.encode('1'))
            #time.sleep(1)

        if var == '2':
            ArduinoUnoSerial.write(str.encode('2'))
            #time.sleep(1)

        if var == '3':
            ArduinoUnoSerial.write(str.encode('3'))
            #time.sleep(1)


#traffic(1)

