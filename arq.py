import serial
from enum import Enum

class eventos(Enum):
	OCIOSO = 0
	PAYLOAD = 1    
	ACK = 2
	DADO = 3
	TIMEOUT = 4


class ARQ:
	def __init__(self, enq):
		self.controle = b''
		self.proto = b''
		self.enq = enq(self, ser)
		self.timeout = eventos.TIMEOUT
		

	def envia(self, payload):

	def handle(self, ):
		if(estado == TX_pay):
			if(payload!=0):
				self.envia(payload)
				estado = TX_ack
			else:
				estado = TX_pay

		elif(estado == TX_ack):
			if(self.controle == ack):
				if(self.controle == b'\x88'):
					self.controle = b'\x80'				
				else:
					self.controle = b'\x88'
				estado = TX_pay
 
			elif(self.timeout):
				estado = TX_ack
			else:
				estado = RX
			
		else:#RX
			if(self.controle == ack):
				if(self.controle == b'\x88'):
					self.controle = b'\x80'				
				else:
					self.controle = b'\x88'
				estado = RX

			else:
				estado = RX
	
##payload = controle+Proto+data
##quadro (M_n) = payload+CRC
