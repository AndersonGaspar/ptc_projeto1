import enq
import serial
ser = serial.Serial('/dev/pts/18',9600,timeout=20)
frame = enq.Enquadramento(ser)
frame.recebe()
