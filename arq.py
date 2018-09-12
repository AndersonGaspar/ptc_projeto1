import serial
from enum import Enum

class estados(Enum):
    OCIOSO = 1
    TX_pay = 2
    TX_ack = 3
    RX = 4

class eventos(Enum):
    PAYLOAD = 1   
    ACK = 2
    DADO = 3
    TIMEOUT = 4


class ARQ:
    def __init__(self, enq, id):
        self.controle = b'' # byte de controle
        self.seq = True # bit de sequencia
        self.proto = id #id definido pela aplicação ou pela arquitetura;
        self.payload = b'' # mensagem a ser enviado
        self.data = b'' # pacote recebido
        self.estado = estados.OCIOSO # estado inicial
        self.evento = None # evento nulo
        self.enq = enq # objeto da classe enquadramento
       

    def envia(self, payload):
        key = True
        self.evento = eventos.PAYLOAD
        self.handle()

        self.payload = payload
        if(seq):
            self.controle = b'\x00'
        else:
            self.controle = b'\x08'

        self.handle()

        while(key)
            self.data = self.enq.recebe()
            if(self.data[0] & 0x80):
                self.evento = eventos.ACK
                self.handle()
                if((self.data[0] & 0x08) == (self.controle & 0x08)):
                    self.evento = eventos.PAYLOAD
                    key = False
                else:
                    self.evento = eventos.ACK
                self.handle()
            else:
                self.evento = eventos.DADO
                self.handle()
        
        self.estado = estados.OCIOSO
        return 1


    def recebe(self):
        key = True
        self.evento = eventos.DADO
        self.handle()

        while(key)
            self.data = self.enq.recebe()
            if(self.data < 0):
                self.estado = estados.OCIOSO
                return self.data 
            else:
                if(self.data[0] & 0x80):
                    self.evento = eventos.ACK
                    self.handle()
                else:
                    self.evento = eventos.DADO
                    self.handle()
                    key = False
        
        self.estado = estados.OCIOSO
        return 1



    def handle(self):
        if(self.estado == estado.OCIOSO):
            if(self.evento == eventos.PAYLOAD):
                self.estado = estados.TX_pay
            elif(self.evento == eventos.DADO):
                self.estado = estados.RX

        elif(estado == estados.TX_pay):
            self.enq.envia((self.controle + self.proto + self.payload))
            if(self.evento == eventos.ACK):
                self.estado = estados.TX_ack
            elif(self.evento == eventos.DADO):
                self.estado = estados.RX
            else:
                estado = estados.TX_pay
    
        elif(estado == estados.TX_ack):
            if(self.evento == eventos.PAYLOAD):
                self.estado = estados.TX_pay
            elif(self.evento == eventos.DADO):
                self.estado = estados.RX
            else:
                estado = estados.TX_ack
           
        else:#RX
            if(self.evento == eventos.PAYLOAD):
                self.estado = estados.TX_pay
            elif(self.evento == eventos.ACK):
                self.estado = estados.TX_ack
            else:
                self.enq.envia(((self.data[0] | 0x80) + self.data[1]))
                estado = estados.RX
   
##payload = controle+Proto+data
##quadro (M_n) = payload+CRC
