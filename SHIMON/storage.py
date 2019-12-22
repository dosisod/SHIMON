import pretty_bad_protocol as pbp
from hashlib import sha512
from flask import Response
import json
import os

from .renderer import render
from .api.error import error, error_401

from typing import Union
from .__init__ import Page

#fixes 'DECRYPTION_COMPLIANCE_MODE' '23' error
from pretty_bad_protocol import gnupg
import pretty_bad_protocol._parsers
gnupg._parsers.Verify.TRUST_LEVELS["DECRYPTION_COMPLIANCE_MODE"] = 23

gpg=pbp.GPG()

def unlock(pwd: str) -> str: #given password, try and return plaintext
	if os.path.isfile("data.gpg"): #check if data.gpg exists
		with open("data.gpg", "rb") as f:
			return gpg.decrypt_file(f, passphrase=pwd).data.decode()

	return "{}" #return blank if file doesnt exist

#encrypt data with password, send to "data.gpg"
def locker(data: str, pwd: str) -> None:
	gpg.encrypt(data, passphrase=pwd, symmetric=True, encrypt=False, output="data.gpg")

#tries and locks with given password
def attempt_lock(self, pwd: str) -> Union[Page]:
	if not self.cache or self.cache=={}:
		#go back to login if cache doesnt exist
		return error(
			400,
			render(
				self,
				"pages/login.html",
				msg="Please re-open cache"
			),
			False,
			True
		)

	if self.cache["sha512"]:
		if self.cache["sha512"]==sha512(pwd.encode()).hexdigest():
			#only lock if the pwd is the same as the cache
			locker(json.dumps(self.cache), pwd)
			return None

	#if sha512 doesnt exist or doesnt match passed pwd, 401
	return "fail"

def lock(self, pwd: str) -> Union[Page]:
	error_status=attempt_lock(self, pwd)

	if error_status=="fail":
		return error(
			401,
			render(
				self,
				"pages/account.html",
				error="Cache could not be locked"
			),
			True,
			False
		)

	if not error_status:
		return
	else:
		return error_status

def save(self, pwd: str) ->Union[Page]:
	error_status=attempt_lock(self, pwd)

	if error_status=="fail":
		return error_401()

	if not error_status:
		return
	else:
		return error_status