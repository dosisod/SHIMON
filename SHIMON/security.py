from flask import request, abort, Response
from hashlib import sha512

from .util import encode_stringish

from typing import Union, Dict, cast
from .__init__ import Stringish, Page

class Security:
	def __init__(self, shimon_ref):
		self.shimon=shimon_ref

		self._testing=False

	def check_all(self) -> Union[Page]:
		self.check_local()
		self.check_allowed()
		return self.check_session()

	def check_session(self) -> Union[Page]:
		session=""
		if "session" in request.cookies:
			session=request.cookies["session"]

		return self.shimon.session.check({
			"session": session,
			"redirect": True
		})

	def check_local(self) -> None:
		if self._testing:
			return

		if not request.remote_addr=="127.0.0.1":
			abort(403)

	def check_allowed(self) -> None:
		if self.shimon.cache=={} or not self.shimon.cache:
			abort(401)

	def correct_pwd(self, pwd: Stringish) -> bool:
		return self.shimon.cache["sha512"]== \
			sha512(encode_stringish(pwd)).hexdigest()

	#updates hash to new if old is correct, else return false
	def update_pwd(self, plain: Stringish, new_pwd: Stringish) -> bool:
		if self.correct_pwd(plain):
			self.shimon.cache["sha512"]= \
				sha512(encode_stringish(new_pwd)).hexdigest()

			return True

		return False