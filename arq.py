import serial
from enum import Enum

class estados(Enum):
    OCIOSO = 0
    ACK = 1

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
        self.payload = payload
        self.evento = eventos.PAYLOAD
        self.handle()

        while(self.estado != estados.OCIOSO):
            self.data = self.enq.recebe()
            if(timeout):
                self.evento = eventos.TIMEOUT
                self.handle()
            else:
                if(self.data[0] & 0x80):
                    self.evento = eventos.ACK
                else:
                    self.evento = eventos.DADO
                self.handle()

        return 1


    def recebe(self):
        self.evento = eventos.DADO
        self.handle()

        return self.data[2:]


    def envia_quadro(self):
        if(self.seq):
            self.controle = b'\x00'
        else:
            self.controle = b'\x08'
        self.seq = not(self.seq)
        self.enq.envia((self.controle + self.proto + self.payload))

    def envia_ack(self):
        # Checkar sitaxe.
        self.enq.envia((data[0] + 0x80)+data[1])

    def handle(self):
        if(self.estado == estado.OCIOSO):
            if(self.evento == eventos.PAYLOAD):
                self.envia_quadro()
                self.estado = estados.ACK
                
            elif(self.evento == eventos.DADO):
                self.envia_ack()

        else:#ACK
            if(self.evento == eventos.ACK):
                if((self.data[0] & 0x08) and (self.seq)):
                    self.estado = estados.OCIOSO
                else:
                    pass
            elif(self.evento == eventos.DADO):
                self.envia_ack()
