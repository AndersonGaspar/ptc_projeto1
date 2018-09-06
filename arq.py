import serial
from enum import Enum

class eventos(Enum):
    PAYLOAD = 1    
    ACK = 2
    DADO = 3
    TIMEOUT = 4


class ARQ:
	def __init__(self, enq):
		self.controle = b''
		self.proto = b''
		self.enq = enq(self, ser)
		self.estado = 'ocioso'

	def handle(self, ):