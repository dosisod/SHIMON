from Cryptodome.Signature import PKCS1_PSS
from Cryptodome.Cipher import PKCS1_OAEP
from Cryptodome.PublicKey import RSA
from Cryptodome.Hash import SHA512

class kee(): #allows proper padding with OAEP and signing via crypto signature
	def __init__(self, bits=None):
		if bits: #if bits isnt set a blank key is made
			self.RSA=RSA.generate(bits) #normal RSA key
			self.SIG=PKCS1_PSS.new(self.RSA) #signing obj
			self.PAD=PKCS1_OAEP.new(self.RSA, hashAlgo=SHA512) #oaep obj

	def pub(self): #returns public key
		return self.RSA.publickey().exportKey(format="DER")

	def private(self): #returns private key
		return self.RSA.exportKey(format="DER")

	def importKey(self, k):
		self.RSA=RSA.importKey(k) #normal RSA key
		self.SIG=PKCS1_PSS.new(self.RSA) #signing obj
		self.PAD=PKCS1_OAEP.new(self.RSA, hashAlgo=SHA512) #oaep obj

	def sign(self, m): #returns a signed digest using signature obj
		if type(m) is str:
			m=m.encode()
		return self.SIG.sign(SHA512.new(m))

	def encrypt(self, m): #encrypt and decrypt both use oaep obj for padding
		if type(m) is str:
			m=m.encode()
		return self.PAD.encrypt(m)

	def decrypt(self, c):
		return self.PAD.decrypt(c)