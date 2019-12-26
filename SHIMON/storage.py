import pretty_bad_protocol as pbp
from hashlib import sha512
from flask import Response
import json
import os

from .renderer import render
from .api.error import error, error_401

from typing import Union
from .__init__ import Page, Json

#fixes 'DECRYPTION_COMPLIANCE_MODE' '23' error
from pretty_bad_protocol import gnupg
import pretty_bad_protocol._parsers
gnupg._parsers.Verify.TRUST_LEVELS["DECRYPTION_COMPLIANCE_MODE"] = 23

gpg=pbp.GPG()

def unlock(pwd: str) -> str:
	data=raw_unlock("data.gpg", pwd)

	if data==None:
		return "{}"

	if data=="":
		return

	return data

def raw_unlock(filepath: str, pwd: str) -> str:
	if os.path.isfile(filepath):
		with open(filepath, "rb") as f:
			return gpg.decrypt_file(f, passphrase=pwd).data.decode()

	return None

def lock(self, pwd: str) -> Union[Page]:
	error_status=attempt_lock(self, pwd)

	if error_status=="fail":
		return error(
			401,
			render(
				self,
				"pages/account.html",
				error="Cache could not be locked",
				version=self.VERSION
			),
			True,
			False
		)

	if not error_status:
		return
	else:
		return error_status

def save(self, pwd: str) -> Union[Page, Json]:
	error_status=attempt_lock(self, pwd)

	if error_status=="fail":
		return error_401()

	if not error_status:
		return
	else:
		return error_status

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
			raw_lock("data.gpg", json.dumps(self.cache), pwd)
			return None

	#if sha512 doesnt exist or doesnt match passed pwd, 401
	return "fail"

def raw_lock(filepath: str, data: str, pwd: str) -> None:
	gpg.encrypt(
		data,
		passphrase=pwd,
		symmetric=True,
		encrypt=False,
		output=filepath
	)