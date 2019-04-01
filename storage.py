import pretty_bad_protocol as pbp

#fixes 'DECRYPTION_COMPLIANCE_MODE' '23' error
from pretty_bad_protocol import gnupg
import pretty_bad_protocol._parsers
gnupg._parsers.Verify.TRUST_LEVELS["DECRYPTION_COMPLIANCE_MODE"] = 23

gpg=pbp.GPG()

def unlock(pwd):
	with open("data.gpg", "rb") as f:
		return gpg.decrypt_file(f, passphrase=pwd)

def lock(data, pwd):
	cipher=gpg.encrypt(data, passphrase=pwd, symmetric=True, encrypt=False, output="data.gpg")