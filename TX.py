import enq
import serial

#ser = serial.Serial('/dev/ttyUSB1',9600)
ser = serial.Serial('/dev/pts/21',9600)

frame = enq.Enquadramento(ser)
frame.envia(b'hello')
