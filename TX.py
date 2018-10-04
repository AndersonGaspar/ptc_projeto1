import enq
import serial
import arq

#ser = serial.Serial('/dev/ttyUSB1',9600)
ser = serial.Serial('/dev/pts/2',9600)
frame = enq.Enquadramento(ser)
data = arq.ARQ(frame, 0)
data.envia(b'hello\n')
data.envia(b'How are you\n')
data.envia(b'Say something\n')