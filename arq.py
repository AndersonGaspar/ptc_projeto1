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
        self.controle = b''
        self.seq = False
        self.proto = id
        self.payload = b''
        self.data = b''
        self.estado = estados.OCIOSO
        self.evento = None
        self.enq = enq
       

    def envia(self, payload):
        self.evento = eventos.PAYLOAD
        handle()

        self.payload = payload
        if(seq):
            self.controle = b'\x00'
        else:
            self.controle = b'\x08'

        self.evento = eventos.ACK
        handle()
        
        self.data = self.enq.recebe()
        if():





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
            if(self.evento == eventos.ACK):
                self.estado = estados.TX_ack
            else:
                estado = estados.RX
   
##payload = controle+Proto+data
##quadro (M_n) = payload+CRC
