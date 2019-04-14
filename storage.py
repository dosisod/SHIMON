import pretty_bad_protocol as pbp
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

def lock(data, pwd): #encrypt data with password, send to "data.gpg"
	gpg.encrypt(data, passphrase=pwd, symmetric=True, encrypt=False, output="data.gpg")