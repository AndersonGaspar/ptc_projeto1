import serial
from PyCRC.CRC16 import CRC16

class Enquadramento:
	
	def __init__(self, ser):
		self.ser = ser
		self.buff = b''
		self.n_bytes = 0
		self.estado = 'ocioso'

	def envia(self, byt):        
		pacote = b'\x7E'

		for x in range(0, len(byt)):
		    if((byt[x]== int.from_bytes(b'\x7E', byteorder='big')) or (byt[x] == int.from_bytes(b'\x7D', byteorder='big'))):
		        pacote += b'\x7D'
		        pacote += (byt[x] ^ int.from_bytes(b'\x20', byteorder='big')).to_bytes(1, byteorder='big')
		    else:
		        pacote += byt[x].to_bytes(1,byteorder='big')

		pacote += self.gen_CRC(pacote[1:])
		pacote += b'\x7E'
		self.ser.write(pacote)
		print('mensagem enviada\n', pacote)
	
	def gen_CRC(self,input):
		crc = CRC16().calculate(input)
		return (crc.to_bytes(2,byteorder='big'))

	def check_CRC(self, data, crc_recv):
		crc_data = CRC16().calculate(data)
		return (crc_data.to_bytes(2,byteorder='big') == crc_recv)

	def handle(self, byte_recv):

		if(self.estado == 'ocioso'):
			if(byte_recv == b'\x7E'):
				self.buff = b''
				self.n_bytes = 0
				self.estado = 'recebe'
			else:
				self.estado = 'ocioso'

		elif(self.estado == 'recebe'):

			if(byte_recv == b'\x7D'):
				self.estado = 'esc'
			elif((byte_recv == b'\x7E') and (self.n_bytes==0)):
				self.estado = 'recebe'
			#elif(timeout): 
			#	self.n_bytes = 0
			#	self.estado = 'ocioso'
			#	return -1
			elif((byte_recv == b'\x7E') and (self.n_bytes>0)):	
				self.estado = 'ocioso'
				return 1
			else:#(by_comum)
				self.n_bytes += 1
				self.buff += byte_recv

		elif(self.estado == 'esc'):

			if((byte_recv == b'\x7D') or (byte_recv == b'\x7E')):# timeout
				self.buff = b''
				self.estado = 'ocioso'
				return -2 
			else:#(byte_com)
				self.n_bytes += 1
				self.buff += (int.from_bytes(byte_recv, 'big') ^ 0x20 ).to_bytes(1, 'big')
				self.estado = 'recebe'	

		return 0

	def recebe(self):
		while(True):
			byte = self.ser.read()
			#print(byte)
			
			if(byte == b''):
				self.estado = 'ocioso'
				return -1
			key = self.handle(byte)
			if(key):
				if(self.check_CRC(self.buff[0:len(self.buff)-2], self.buff[-2:])):
					break
				else:
					return -2
			elif(key < 0):
				return key
			else:
				pass
		print(self.buff[0:len(self.buff)-2])
		return self.buff[0:len(self.buff)-2]
		

