import enq
import serial

#ser = serial.Serial('/dev/ttyUSB0',9600)
ser = serial.Serial('/dev/pts/20',9600)
frame = enq.Enquadramento(ser)
frame.recebe()
