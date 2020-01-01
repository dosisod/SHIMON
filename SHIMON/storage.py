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

class Storage:
	def __init__(self, shimon_ref, filepath: str="data.gpg"):
		self.shimon=shimon_ref

		self.filepath=filepath
		self.gpg=pbp.GPG()

	def unlock(self, pwd: str) -> str:
		data=self.raw_unlock(self.filepath, pwd)

		if data==None:
			return "{}"

		if data=="":
			return

		return data

	def raw_unlock(self, filepath: str, pwd: str) -> str:
		if self.cache_file_exists(filepath):
			with open(filepath, "rb") as f:
				return self.gpg.decrypt_file(f, passphrase=pwd).data.decode()

		return None

	def cache_file_exists(self, filepath: str="") -> bool:
		if filepath=="":
			filepath=self.filepath

		return os.path.isfile(filepath)

	def lock(self, pwd: str) -> Union[Page]:
		error_status=self.attempt_lock(pwd)

		if error_status=="fail":
			return error(
				401,
				render(
					self.shimon,
					"pages/account.html",
					error="Cache could not be locked",
					version=self.shimon.VERSION
				),
				True,
				False
			)

		if not error_status:
			return
		else:
			return error_status

	def save(self, pwd: str) -> Union[Page, Json]:
		error_status=self.attempt_lock(pwd)

		if error_status=="fail":
			return error_401()

		if not error_status:
			return
		else:
			return error_status

	def attempt_lock(self, pwd: str) -> Union[Page]:
		if not self.shimon.cache or self.shimon.cache=={}:
			return error(
				400,
				render(
					self.shimon,
					"pages/login.html",
					msg="Please re-open cache"
				),
				False,
				True
			)

		if self.shimon.cache["sha512"]:
			if self.shimon.cache["sha512"]==sha512(pwd.encode()).hexdigest():
				self.raw_lock(self.filepath, json.dumps(self.shimon.cache), pwd)
				return None

		return "fail"

	def raw_lock(self, filepath: str, data: str, pwd: str) -> None:
		self.gpg.encrypt(
			data,
			passphrase=pwd,
			symmetric=True,
			encrypt=False,
			output=filepath
		)