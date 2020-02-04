import base64 as b64

from ..kee import Kee

from .error import error_400, error_401

from ..__init__ import HttpResponse

def new_key(self, pwd: str, redirect: bool) -> HttpResponse:
	if self.security.correct_pwd(pwd):
		self.cache["key"]=b64.b64encode(
			Kee(2048).private()
		).decode()

		#makes sure changes are saved
		self.storage.lock(pwd)

		return self.index()

	return error_401()
