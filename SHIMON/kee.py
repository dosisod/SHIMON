from Cryptodome.Signature import PKCS1_PSS
from Cryptodome.Cipher import PKCS1_OAEP
from Cryptodome.PublicKey import RSA
from Cryptodome.Hash import SHA512

from typing import Union
from .__init__ import Stringish

class kee(): #allows proper padding with OAEP and signing via crypto signature
	def __init__(self, bits: Union[int]=None) -> None:
		if bits: #if bits isnt set a blank key is made
			self.RSA=RSA.generate(bits) #normal RSA key
			self.SIG=PKCS1_PSS.new(self.RSA) #signing obj
			self.PAD=PKCS1_OAEP.new(self.RSA, hashAlgo=SHA512) #oaep obj

	def pub(self) -> bytes: #returns public key
		return self.RSA.publickey().exportKey(format="DER")

	def private(self) -> bytes: #returns private key
		return self.RSA.exportKey(format="DER")

	def importKey(self, key: RSA) -> None:
		self.RSA=RSA.importKey(key) #normal RSA key
		self.SIG=PKCS1_PSS.new(self.RSA) #signing obj
		self.PAD=PKCS1_OAEP.new(self.RSA, hashAlgo=SHA512) #oaep obj

	def sign(self, msg: Stringish) -> bytes: #returns a signed digest using signature obj
		if type(msg) is str:
			msg=msg.encode()
		return self.SIG.sign(SHA512.new(msg))

	def encrypt(self, msg: Stringish) -> bytes: #encrypt and decrypt both use oaep obj for padding
		if type(msg) is str:
			msg=msg.encode()
		return self.PAD.encrypt(msg)

	def decrypt(self, cipher: bytes) -> bytes:
		return self.PAD.decrypt(cipher)