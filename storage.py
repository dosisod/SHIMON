import pretty_bad_protocol as pbp
from hashlib import sha512
import os

#fixes 'DECRYPTION_COMPLIANCE_MODE' '23' error
from pretty_bad_protocol import gnupg
import pretty_bad_protocol._parsers
gnupg._parsers.Verify.TRUST_LEVELS["DECRYPTION_COMPLIANCE_MODE"] = 23

gpg=pbp.GPG()

def unlock(pwd): #given password, try and return plaintext
	if os.path.isfile("data.gpg"): #check if data.gpg exists
		with open("data.gpg", "rb") as f:
			return gpg.decrypt_file(f, passphrase=pwd).data.decode()

	return "{}" #return blank if file doesnt exist

def locker(data, pwd): #encrypt data with password, send to "data.gpg"
	gpg.encrypt(data, passphrase=pwd, symmetric=True, encrypt=False, output="data.gpg")

def lock(self, data, pwd): #tries and locks with given password
	if self.cache["sha512"]:
		if self.cache["sha512"]==sha512(pwd.encode()).hexdigest():
			#only lock if the pwd is the same as the cahce
			locker(data, pwd)
			return True

	return False #error if cache was not locked