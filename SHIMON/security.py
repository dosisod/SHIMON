from flask import request, abort, Response
from hashlib import sha512

from typing import Union, Dict
from .__init__ import Stringish, Page

class Security:
	def __init__(self):
		pass

	def check_all(self, external_self) -> Union[Page]:
		self.check_local()
		self.check_allowed(external_self.cache)
		return self.check_session(external_self)

	def check_session(self, external_self) -> Union[Page]:
		session=""
		if "session" in request.cookies:
			session=request.cookies["session"]

		return external_self.session.check(external_self, {
			"session": session,
			"redirect": True
		})

	def check_local(self) -> None:
		if not request.remote_addr=="127.0.0.1":
			abort(403)

	def check_allowed(self, cache: Union[Dict]) -> None:
		if cache=={} or not cache:
			abort(401)

	def correct_pwd(self, external_self, plain: Stringish) -> bool:
		if type(plain) is str:
			plain=plain.encode()

		return external_self.cache["sha512"]==sha512(plain).hexdigest()

	#updates hash to new if old is correct, else return false
	def update_pwd(self, external_self, plain: Stringish, new: Stringish) -> bool:
		if self.correct_pwd(external_self, plain):
			if type(new) is str:
				new=new.encode()

			external_self.cache["sha512"]=sha512(new).hexdigest()
			return True

		return False