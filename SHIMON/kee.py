from Cryptodome.Signature import PKCS1_PSS
from Cryptodome.Cipher import PKCS1_OAEP
from Cryptodome.PublicKey import RSA
from Cryptodome.Hash import SHA512

from .util import encode_stringish

from typing import Union
from .__init__ import Stringish

class kee(): #allows proper padding with OAEP and signing via crypto signature
	def __init__(self, bits: Union[int]=None) -> None:
		if bits: #if bits isnt set a blank key is made
			self.RSA=RSA.generate(bits)
			self.SIG=PKCS1_PSS.new(self.RSA)
			self.PAD=PKCS1_OAEP.new(self.RSA, hashAlgo=SHA512)

	def pub(self) -> bytes:
		return self.RSA.publickey().exportKey(format="DER")

	def private(self) -> bytes:
		return self.RSA.exportKey(format="DER")

	def importKey(self, key: RSA) -> None:
		self.RSA=RSA.importKey(key)
		self.SIG=PKCS1_PSS.new(self.RSA)
		self.PAD=PKCS1_OAEP.new(self.RSA, hashAlgo=SHA512)

	def sign(self, msg: Stringish) -> bytes: #returns a signed digest using signature obj
		encoded=encode_stringish(msg)

		return self.SIG.sign(SHA512.new(encoded))

	def encrypt(self, msg: Stringish) -> bytes: #encrypt and decrypt both use oaep obj for padding
		encoded=encode_stringish(msg)

		return self.PAD.encrypt(encoded)

	def decrypt(self, cipher: bytes) -> bytes:
		return self.PAD.decrypt(cipher)