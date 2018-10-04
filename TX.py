import enq
import serial
import arq
import Sessao
ser = serial.Serial('/dev/ttyUSB1',9600)
#ser = serial.Serial('/dev/pts/2',9600)
frame = enq.Enquadramento(ser)
data = arq.ARQ(frame, 0)
quadro = Sessao.Sessao(data,data.session)
quadro.connect()
quadro.envia(b'hello\n')
quadro.envia(b'How are you\n')
quadro.envia(b'Say something\n')
quadro.disconnect()