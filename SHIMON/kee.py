from Cryptodome.Signature import PKCS1_PSS
from Cryptodome.Cipher import PKCS1_OAEP
from Cryptodome.PublicKey import RSA
from Cryptodome.Hash import SHA512

from .util import encode_anystr

from typing import Union, AnyStr

#allows proper padding with OAEP and signing via crypto signature
class kee():
	def __init__(self, bits: Union[int]=None) -> None:
		#if bits isnt set a blank key is made
		if bits:
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

	#returns a signed digest using signature obj
	def sign(self, msg: AnyStr) -> bytes:
		return self.SIG.sign(SHA512.new(
			encode_anystr(msg)
		))

	#encrypt and decrypt both use oaep obj for padding
	def encrypt(self, msg: AnyStr) -> bytes:
		return self.PAD.encrypt(
			encode_anystr(msg)
		)

	def decrypt(self, cipher: bytes) -> bytes:
		return self.PAD.decrypt(cipher)