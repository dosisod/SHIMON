import base64 as b64

from SHIMON.kee import Kee

from SHIMON.api.error import error_400, error_401

from SHIMON.__init__ import HttpResponse

def new_key(self, pwd: str, redirect: bool) -> HttpResponse:
	if self.security.correct_pwd(pwd):
		self.cache["key"]=b64.b64encode(
			Kee(2048).private()
		).decode()

		#makes sure changes are saved
		self.storage.lock(pwd)

		return self.index()

	return self.index(error="Invalid Password", code=401)
