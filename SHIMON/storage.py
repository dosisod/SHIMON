import pretty_bad_protocol as pbp
from hashlib import sha512
from flask import Response
import json
import os

from .api.error import error, error_401
from .renderer import render

from typing import Union, Optional, cast
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

	def unlock(self, pwd: str) -> Optional[str]:
		data=self.raw_unlock(self.filepath, pwd)

		if data==None:
			return "{}"

		if data=="":
			return None

		return data

	def raw_unlock(self, filepath: str, pwd: str) -> Optional[str]:
		if self.cache_file_exists(filepath):
			with open(filepath, "rb") as f:
				return cast(
					str,
					self.gpg.decrypt_file(
						f,
						passphrase=pwd
					).data.decode()
				)

		return None

	def cache_file_exists(self, filepath: str="") -> bool:
		if filepath=="":
			filepath=self.filepath

		return os.path.isfile(filepath)

	def lock(self, pwd: str) -> Optional[Page]:
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
			return None

		else:
			return error_status

	def save(self, pwd: str) -> Union[Page, Json, None]:
		error_status=self.attempt_lock(pwd)

		if error_status=="fail":
			return error_401()

		if not error_status:
			return None

		else:
			return error_status

	def attempt_lock(self, pwd: str) -> Optional[Page]:
		if not self.shimon.cache or self.shimon.cache=={"": None}:
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
			if self.shimon.security.correct_pwd(pwd):
				self.raw_lock(
					self.filepath,
					json.dumps(self.shimon.cache),
					pwd
				)

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