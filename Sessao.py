import arq
from enum import Enum
import time

# Half1 ?Data
# Keep ALive

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
	_DATA = 10

class Sessao:
	
	def __init__(self, arq, id_proto):
		self.estado = estados.DISC
		self.evento = None
		self.arq = arq
		self.id_proto = id_proto.to_bytes(1, byteorder='big')
		self.payload = b''
		self.buffer = b''
		self.n_tentativas = 0
		self.timeouts = {	'CC' : 2, 
							'KC' : 2,
							'DR' : 2,
							'DATA' : 2,
							'DC' : 3}

	def connect(self):
		self.evento = eventos.CR
		self.handle()
		while(self.estado != estados.CON):
			self.arq.set_Timeout(self.timeouts['CC'])
			self.data = self.arq.recebe()
			#print("Sessão", self.data)
			if(self.data[0] == -3): # Timeout CC
				self.evento = eventos.TIMEOUT
				#print("Timeout")
				response = self.handle()
				if(response == -3):
					self.n_tentativas = 0
					self.evento = eventos.ERROR
					self.handle()
					return -3

			else:
				self.n_tentativas = 0
				if (self.data[1][0].to_bytes(1, byteorder='big') == b'\xFF'):
					if (self.data[1][1].to_bytes(1, byteorder='big') == b'\x01'):
						self.evento = eventos.CC
						self.handle()
		
		return 1

	def envia(self, payload):
		self.payload = payload
		self.evento = eventos.DATA
		self.handle()

	def disconnect(self):
		self.evento = eventos.DR
		self.handle()
		while(self.estado != estados.DISC):
			self.arq.set_Timeout(self.timeouts['DR'])
			self.data = self.arq.recebe()
			if(self.data[0] == -3): # Timeout DR
				self.evento = eventos.TIMEOUT
				response = self.handle()
				if(response == -3):
					self.n_tentativas = 0
					self.evento = eventos.ERROR
					self.handle()
					return -3
			else:
				if (self.data[1][0].to_bytes(1, byteorder='big') == b'\xFF'):
					if(self.data[1][1].to_bytes(1, byteorder='big') == b'\x04'):
						self.evento = eventos._DR
						self.handle()
						return 1

	def recebe(self):
		#print('recebe')
		self.buffer = b''
		#print('Buffer', self.buffer)
		while(True):
			while (self.estado != estados.HAND2):
				self.data = self.arq.recebe()
				if((self.data[1][0].to_bytes(1, byteorder='big') == b'\xFF')  and 
					(self.data[1][1].to_bytes(1, byteorder='big')  == b'\x00')):
					self.evento = eventos.CC
					self.handle()

			while (self.estado != estados.CON):
				#print('Here')
				self.arq.set_Timeout(self.timeouts['CC'])
				self.data = self.arq.recebe()
				#print('Sessão', self.data)
				if(self.data[0] == -3): # Timeout CC
					self.evento = eventos.TIMEOUT
					self.handle()
					if(self.estado == estados.DISC):
						return -3
				elif(self.data[1][0].to_bytes(1, byteorder='big') == self.id_proto):
					self.buffer += self.data[1][1:]
					self.evento = eventos.DATA
					self.handle()

			while(self.estado != estados.DISC):
				if(self.estado == estados.CON):
					self.arq.set_Timeout(self.timeouts['DATA'])
				else:
					self.arq.set_Timeout(self.timeouts['DC'])
			
				self.data = self.arq.recebe()
				if(self.data[0] == -3):
					self.evento = eventos.TIMEOUT
					self.handle()
					if(self.estado == estados.DISC):
						return(-3, None)
				else:
					if(self.data[1][0].to_bytes(1, byteorder='big') == self.id_proto):
						self.buffer += self.data[1][1:]
						self.evento = eventos._DATA
						self.handle()

					elif((self.data[1][0].to_bytes(1, byteorder='big') == b'\xFF') and 
							(self.data[1][1].to_bytes(1, byteorder='big') == b'\x04')):
						self.evento = eventos._DR
						self.handle()
					
					elif((self.data[1][0].to_bytes(1, byteorder='big') == b'\xFF') and 
							(self.data[1][1].to_bytes(1, byteorder='big') == b'\x05')):
						self.evento = eventos.DC
						self.handle()
						self.arq.reset()
						#print('Sessao',  self.buffer)
						return((1, self.buffer))
						




	def handle(self):

		if(self.estado == estados.DISC):
			if(self.evento == eventos.CR):
				self.estado = estados.HAND1
				self.arq.envia(b'\xFF\x00')

			elif(self.evento == eventos.CC):
				self.estado = estados.HAND2
				#time.sleep(25)
				self.arq.envia(b'\xFF\x01')

		elif(self.estado == estados.HAND1):
			if(self.evento == eventos.CC):
				self.estado = estados.CON
				self.arq.envia(self.id_proto + self.payload)

			elif(self.evento == eventos.ERROR):
				self.estado = estados.DISC
			
			elif(self.evento == eventos.TIMEOUT):
				self.arq.envia(b'\xFF\x00')
				self.estado = estados.HAND1
				self.n_tentativas += 1
				if(self.n_tentativas >= 3):
					return -3

		elif(self.estado == estados.HAND2):
			if(self.evento == eventos.DATA):
				self.estado = estados.CON

			elif(self.evento == eventos.TIMEOUT):
				self.estado = estados.DISC
				return -3

		elif(self.estado == estados.CON):
			if(self.evento == eventos.KR):
				self.estado = estados.CHECK

			elif(self.evento == eventos.DR):
				self.estado = estados.HALF1
				self.arq.envia(b'\xFF\x04')

			elif(self.evento == eventos._DR):
				self.arq.envia(b'\xFF\x04')
				self.estado = estados.HALF2

			elif((self.evento == eventos.DATA) or (self.evento == eventos.KR)):
				self.estado = estados.CON
				if (self.evento == eventos.DATA):
					self.arq.envia(self.id_proto + self.payload)
				else:
					self.arq.envia(b'\xFF\x02')
			
			elif(self.evento == eventos._DATA):
				self.estado = estados.CON

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
				if(self.evento == eventos.TIMEOUT):
					self.arq.envia(b'\xFF\x04')
					self.n_tentativas += 1
					if(self.n_tentativas >= 3):
						return -3

				self.estado = estados.HALF1

		elif(self.estado == estados.HALF2):
			if((self.evento == eventos.DC) or (self.evento == eventos.TIMEOUT)):
				self.estado = estados.DISC

			elif(self.evento == eventos._DR):
				self.arq.envia(b'\xFF\x04')
				self.estado = estados.HALF2

