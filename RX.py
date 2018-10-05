import enq
import serial
import arq	
import Sessao
import time

ser = serial.Serial('/dev/ttyUSB0',9600)
#ser = serial.Serial('/dev/pts/3',9600)
frame = enq.Enquadramento(ser)
data = arq.ARQ(frame, 0)
quadro = Sessao.Sessao(data,data.session)
print(" +++ PROTOCOLO DE ENLACE 3000 +++ ")
time.sleep(1)
print("Aguardando mensagem...")
while(True):
    msg = quadro.recebe()
    print(msg[1])
