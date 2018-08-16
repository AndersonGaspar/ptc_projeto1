import enq
import serial
ser = serial.Serial('/dev/pts/19',9600,timeout=20)
frame = enq.Enquadramento(ser)
frame.envia(b'hello')
