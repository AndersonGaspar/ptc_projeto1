import enq
import serial
import arq

ser = serial.Serial('/dev/ttyUSB1',9600)
#ser = serial.Serial('/dev/pts/4',9600)
frame = enq.Enquadramento(ser)
data = arq.ARQ(frame, 3)
data.envia(b'hello')
data.envia(b'How are you')
data.envia(b'Say something')
msg = data.recebe()
print(msg[1])
