import serial
import crc
 

class Enquadramento:
	
	def __init__(self, ser):
		self.ser = ser
		self.buff = b''
		self.n_bytes = 0
		self.estado = 'ocioso'
		self.controle = b''
		self.proto = b''

	def envia(self, byt):        
		pacote = b'\x7E'
		msg = crc.CRC16(byt).gen_crc()

		for x in range(0, len(msg)):
		    if((msg[x]== int.from_bytes(b'\x7E', byteorder='big')) or (msg[x] == int.from_bytes(b'\x7D', byteorder='big'))):
		        pacote += b'\x7D'
		        pacote += (msg[x] ^ int.from_bytes(b'\x20', byteorder='big')).to_bytes(1, byteorder='big')
		    else:
		        pacote += msg[x].to_bytes(1,byteorder='big')

		pacote += b'\x7E'
		self.ser.write(pacote)
		print('mensagem enviada\n', pacote)

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
				print(self.buff)
				if(crc.CRC16(self.buff[0:len(self.buff)-2]).check_crc()):
					break
				else:
					return -2
			elif(key < 0):
				return key
			else:
				pass
		print(self.buff)
		return self.buff