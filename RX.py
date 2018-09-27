import enq
import serial
import arq	

#ser = serial.Serial('/dev/ttyUSB0',9600)
ser = serial.Serial('/dev/pts/3',9600)
frame = enq.Enquadramento(ser)
data = arq.ARQ(frame, 0, 0)
msg = data.recebe()
print(msg[1])
msg = data.recebe()
print(msg[1])
msg = data.recebe()
print(msg[1])
data.envia(b'No!')
