import serial
import select
import crc
 

class Enquadramento:
	
	def __init__(self, ser, maxbytes=256):
		self.ser = ser
		self.buff = b''
		self.timeout = 0
		self.maxbytes = maxbytes
		self.n_bytes = 0
		self.estado = 'ocioso'
		self.controle = b''
		self.proto = b''

	def set_Timeout(self, timeout):
		self.timeout = timeout

	def envia(self, byt):        
		if(len(byt) > self.maxbytes):
			return -1

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
		#print('mensagem enviada\n', pacote)
		return 1

	def handle(self, byte_recv):

		if(self.estado == 'ocioso'):
			if(byte_recv == b'\x7E'):
				self.buff = b''
				self.n_bytes = 0
				self.estado = 'recebe'
			elif(byte_recv == None): 
				self.n_bytes = 0
				self.estado = 'ocioso'
				return -3
			else:
				self.estado = 'ocioso'

		elif(self.estado == 'recebe'):

			if(byte_recv == b'\x7D'):
				self.estado = 'esc'
			elif((byte_recv == b'\x7E') and (self.n_bytes==0)):
				self.estado = 'recebe'
			elif(byte_recv == None): 
				self.n_bytes = 0
				self.estado = 'ocioso'
				return -3
			elif((byte_recv == b'\x7E') and (self.n_bytes>0)):	
				self.estado = 'ocioso'
				return 1
			else:#(by_comum)
				self.n_bytes += 1
				self.buff += byte_recv

		elif(self.estado == 'esc'):

			if((byte_recv == b'\x7D') or (byte_recv == b'\x7E') or (byte_recv == None)):# timeout
				self.buff = b''
				self.estado = 'ocioso'
				if(byte_recv == None):
					return -3
				else:
					return -2 
			else:#(byte_com)
				self.n_bytes += 1
				self.buff += (int.from_bytes(byte_recv, 'big') ^ 0x20 ).to_bytes(1, 'big')
				self.estado = 'recebe'	

		return 0

	def timeout_rx(self, timeout):
		(r,w,e) = select.select([self.ser], [], [], timeout)
		if(not(r)):
			byte = None
		else:
			byte = r[0].read()

		return(byte)

	def recebe(self):
		while(True):
			if(self.estado == 'ocioso' and self.timeout):
				byte = self.timeout_rx(self.timeout)
			elif(self.estado != 'ocioso'):
				byte = self.timeout_rx(0.05)
			elif(not(self.timeout)):
				byte = self.ser.read()
			
			key = self.handle(byte)
			if(self.n_bytes > self.maxbytes):
				self.handle(None)
				key = -1
			
			if(key == 1):		
				if(crc.CRC16(self.buff[0:]).check_crc()):
					#print(self.buff[0:len(self.buff)-2])
					return (1, self.buff[0:len(self.buff)-2])
				else:
					return (-2, [None, None])
			elif(key < 0):
				return (key, [None, None])
			else:
				pass
		return (1, self.buff[0:len(self.buff)-2])