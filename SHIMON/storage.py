from flask import Response
import gnupg as gpg # type: ignore
import json
import os

from .api.error import error, error_401
from .renderer import render

from typing import Union, Optional, cast
from .__init__ import Page, HttpResponse

class Storage:
	def __init__(self, shimon_ref, filepath: str="data.gpg"):
		self.shimon=shimon_ref

		self.filepath=filepath
		self._gpg=gpg.GPG()

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
					self._gpg.decrypt_file(
						f,
						passphrase=pwd
					).data.decode()
				)

		return None

	def cache_file_exists(self, filepath: str="") -> bool:
		if filepath=="":
			filepath=self.filepath

		return os.path.isfile(filepath)

	def lock(self, pwd: str) -> Optional[HttpResponse]:
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
			return error_status # type: ignore

	def save(self, pwd: str) -> Optional[HttpResponse]:
		error_status=self.attempt_lock(pwd)

		if error_status=="fail":
			return error_401()

		if not error_status:
			return None

		else:
			return error_status # type: ignore

	def attempt_lock(self, pwd: str) -> Union[HttpResponse, str, None]:
		if not self.shimon.cache or self.shimon.cache.is_empty():
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
					json.dumps(self.shimon.cache.export()),
					pwd
				)

				return None

		return "fail"

	def raw_lock(self, filepath: str, data: str, pwd: str) -> None:
		self._gpg.encrypt(
			data,
			recipients=None,
			passphrase=pwd,
			symmetric=True,
			output=filepath
		)

		#ensure only the current user can access the file
		os.chmod(filepath, 0o600)