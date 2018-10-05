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
print(' +++ PROTOCOLO DE ENLACE 3000 +++ \n')
time.sleep(1)

while(True):
    print(' +++ Menu: \n')
    print(' +++ 1 - Enviar mensagem \n')
    print(' +++ 2 - Sair\n')
    
    option = input('Escolha uma opção: \n')
    
    if(option == '1'):
        msg = intup('Digite sua mensagem: \n')
        quadro.envia(b'msg')
        print('Mensagem enviada com sucesso!\n')
        input('\nPrecione Enter para continuar\n\n')
    elif(option == '2'):
        break
        
    else:
        print('Opção inválida!\n')
        input('\nPrecione Enter para continuar\n\n')

quadro.disconnect()
