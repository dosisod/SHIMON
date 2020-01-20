from Cryptodome.Signature import PKCS1_PSS
from Cryptodome.Cipher import PKCS1_OAEP
from Cryptodome.PublicKey import RSA
from Cryptodome.Hash import SHA512

from .util import encode_anystr

from typing import Union, AnyStr, Optional

class kee():
	def __init__(self, bits: Optional[int]) -> None:
		if bits:
			self.key=RSA.generate(bits)
			self._handle_key()

	def importKey(self, key: AnyStr) -> None:
		self.key=RSA.importKey(encode_anystr(key))
		self._handle_key()

	def _handle_key(self) -> None:
		self.signer=PKCS1_PSS.new(self.key)
		self.oaep=PKCS1_OAEP.new(
			self.key,
			hashAlgo=SHA512 # type: ignore
		)

	def pub(self) -> bytes:
		return self.key.publickey().exportKey(format="DER")

	def private(self) -> bytes:
		return self.key.exportKey(format="DER")

	def sign(self, msg: AnyStr) -> bytes:
		return self.signer.sign(SHA512.new(
			encode_anystr(msg)
		))

	def encrypt(self, msg: AnyStr) -> bytes:
		return self.oaep.encrypt(
			encode_anystr(msg)
		)

	def decrypt(self, cipher: bytes) -> bytes:
		return self.oaep.decrypt(cipher)