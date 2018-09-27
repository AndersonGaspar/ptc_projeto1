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
		self.id_sessao = id_sessao

	def handle():

		if(self.estado == estados.DISC):
			if(self.evento == eventos.CR):
				self.estado = estados.HAND1

			elif(self.evento == eventos.CC):
				self.estado = estados.HAND2

		elif(self.estado == estados.HAND1):
			if(self.evento == eventos.CC):
				self.estado = estados.CON

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

			elif(self.evento == eventos._DR):
				self.estado = estados.HALF2

			elif((self.evento == eventos.DATA) or (self.evento == eventos.KR)):
				self.estado = estados.CON

		elif(self.estado == estados.CHECK):
			if((self.evento == eventos.KC) or (self.evento == eventos.DATA)):
				self.estado = estados.CON

			elif(self.evento == eventos.ERROR):
				self.estado = estados.DISC

			elif((self.evento == eventos.TIMEOUT) or (self.evento == eventos.DATA) 7
						or (self.evento == eventos.KR)):
				self.estado = estados.CHECK

		elif(self.estado == estados.HALF1):
			if((self.evento == eventos.DR) or (self.evento == eventos.ERROR)):
				self.estado = estados.DISC

			elif((self.evento == eventos.TIMEOUT) or (self.evento == eventos.DATA)):
				self.estado = estados.HALF1

		elif(self.estado == estados.HALF2):
			if((self.evento == eventos.DC) or (self.evento == eventos.TIMEOUT)):
				self.estado = estados.DISC

			elif(self.evento == eventos.DR):
				self.estado = estados.HALF2