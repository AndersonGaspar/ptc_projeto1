import enq
import serial
import arq
import Sessao
ser = serial.Serial('/dev/ttyUSB1',9600)
#ser = serial.Serial('/dev/pts/2',9600)
frame = enq.Enquadramento(ser)
data = arq.ARQ(frame, 0)
quadro = Sessao.Sessao(data,0)
quadro.connect()
<<<<<<< Updated upstream
=======
<<<<<<< HEAD
quadro.envia(b'hello\n')
quadro.envia(b'How are you\n')
quadro.envia(b'Say something\n')
quadro.disconnect()
=======
>>>>>>> Stashed changes
print(' +++ PROTOCOLO DE ENLACE 3000 +++ \n')
time.sleep(1)

while(True):
<<<<<<< Updated upstream
    print(' +++ Menu: \n')
    print(' +++ 1 - Enviar mensagem \n')
    print(' +++ 2 - Sair\n')
=======
    print('\n\n''Menu: \n')
    print('   1 - Enviar mensagem \n')
    print('   2 - Sair\n')
>>>>>>> Stashed changes
    
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
<<<<<<< Updated upstream
=======
>>>>>>> parent of f1fde91... Update TX.py
>>>>>>> Stashed changes
