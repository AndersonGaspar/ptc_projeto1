import arq
from enum import Enum

class estados(Enum):
    DISC = 0
    HAND1 = 1
	HAND2 = 2
	CON = 3
	CHECK = 4
	HALF1 = 5
	HALF2 = 6
class eventos(Enum):
	TIMEOUT = 0
	CR = 1   
    CC = 2
    DR = 3
	_DR = 4
    DC = 5
	KR = 6
	KC = 7
	ERROR = 8
	DATA = 9

class Sessao:
	
	def __init__(self, arq, id_sessao):
		self.estado = estados.DISC
		self.evento = None
		self.arq = arq
		self.id_proto = b''
		self.payload = b''
		self.id_sessao = id_sessao
		self.buffer = b''



    def connect(self):
    	self.evento = eventos.CR
    	self.handle()
    	while(True):
    		self.data = self.arq.recebe()
    		if (self.data[1][0] == b'\xFF'):
				if (self.data[1][1] == b'\x01'):
					self.evento = eventos.CC
					self.handle()

	def envia(self, payload):
    	self.payload = payload
    	self.evento = eventos.DATA
    	self.handle()

    def disconnect(self):
    	self.evento = eventos.DR
    	self.handle()
    	while (True):
   			self.data = self.arq.recebe()
    		if (self.data[1][0] == b'\xFF'):
    			if(self.data[1][1] == b'\x04'):
    				self.evento = eventos._DR
    				self.handle()

	def recebe(self):
		while (self.estado != estados.CON):
			self.data = self.arq.recebe()
			if((self.data[1][0] == b'\xFF') and (self.data[1][0] == b'\x00')):
				self.eveto = eventos.CC
				self.handle()

			elif(self.data[1][0] == self.id_proto):
				self.buffer += self.data[1][1:]
				self.handle()



	def handle():

		if(self.estado == estados.DISC):
			if(self.evento == eventos.CR):
				self.estado = estados.HAND1
				self.arq.envia(b'\xFF'+b'\x00')

			elif(self.evento == eventos.CC):
				self.estado = estados.HAND2
				self.arq.envia(b'\xFF\x01')

		elif(self.estado == estados.HAND1):
			if(self.evento == eventos.CC):
				self.estado = estados.CON
				self.arq.envia(self.id_proto + self.payload)

			elif(self.evento == eventos.ERROR):
				self.estado = estados.DISC
			
			elif(self.evento == eventos.TIMEOUT):
				self.estado = estados.HAND1

		elif(self.estado == estados.HAND2):
			if(self.evento == eventos.DATA):
				self.estado = estados.CON

			elif(self.evento == eventos.TIMEOUT):
				self.estado = estados.DISC

		elif(self.estado == estados.CON):
			if(self.evento == eventos.KR):
				self.estado = estados.CHECK

			elif(self.evento == eventos.DR):
				self.estado = estados.HALF1
				self.arq.envia(b'\xFF\x04')

			elif(self.evento == eventos._DR):
				self.estado = estados.HALF2

			elif((self.evento == eventos.DATA) or (self.evento == eventos.KR)):
				self.estado = estados.CON
				if (self.evento == eventos.DATA):
					self.arq.envia(self.id_proto + self.payload)
				else:
					self.arq.envia(b'\xFF\x02')

		elif(self.estado == estados.CHECK):
			if((self.evento == eventos.KC) or (self.evento == eventos.DATA)):
				self.estado = estados.CON

			elif(self.evento == eventos.ERROR):
				self.estado = estados.DISC

			elif((self.evento == eventos.TIMEOUT) or (self.evento == eventos.DATA) or (self.evento == eventos.KR)):
				self.estado = estados.CHECK

		elif(self.estado == estados.HALF1):
			if((self.evento == eventos._DR) or (self.evento == eventos.ERROR)):
				if (self.evento == eventos._DR):
					self.arq.envia(b'\xFF\x05')

				self.estado = estados.DISC

			elif((self.evento == eventos.TIMEOUT) or (self.evento == eventos.DATA)):
				self.estado = estados.HALF1

		elif(self.estado == estados.HALF2):
			if((self.evento == eventos.DC) or (self.evento == eventos.TIMEOUT)):
				self.estado = estados.DISC

			elif(self.evento == eventos.DR):
				self.estado = estados.HALF2

