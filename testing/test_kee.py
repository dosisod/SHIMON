from SHIMON.kee import kee

from testing.base import BaseTest

class TestKee(BaseTest):
	def test_creating_key_with_bits_sets_up_class(self):
		key=kee(1024)

		self.assert_setup(key)

	def test_importing_key_sets_up_class(self):
		exported=kee(1024).private()

		new_key=kee()
		new_key.importKey(exported)

		self.assert_setup(new_key)

	def test_public_key_returns_non_empty_string(self):
		key=kee(1024)

		assert key.pub()

	def  test_private_key_returns_non_empty_string(self):
		key=kee(1024)

		assert key.private()

	def test_signing_returns_ciphertext(self):
		cipher=kee(2048).sign("HELLO!")

		self.assert_is_cipher(cipher)

	def test_encrypting_returns_ciphertext(self):
		cipher=kee(2048).encrypt("HELLO!")

		self.assert_is_cipher(cipher)

	def test_decrypting_encrypted_msg(self):
		key=kee(2048)

		plain=key.decrypt(key.encrypt("HELLO!"))

		assert plain==b'HELLO!'

	def assert_is_cipher(self, cipher):
		assert cipher!="HELLO!"
		assert cipher
		assert type(cipher) is bytes

	def assert_setup(self, key):
		assert key.key
		assert key.signer
		assert key.oaep