import pretty_bad_protocol as pbp
from flask.json import jsonify
from hashlib import sha512
import json
import os

from error import api_error
from renderer import render

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

def lock(self, pwd): #tries and locks with given password
	if self.cache or self.cache=={}:
		if self.cache["sha512"]:
			if self.cache["sha512"]==sha512(pwd.encode()).hexdigest():
				#only lock if the pwd is the same as the cache
				locker(json.dumps(self.cache), pwd)
				return

		#if sha512 doesnt exist or doesnt match passed pwd, 401
		return api_error(401, "Cache could not be locked", False, False)

	else:
		#go back to login if cache doesnt exist
		return api_error(
			400,
			render(self, "login.html", msg="Please re-open cache"),
			False,
			True
		)