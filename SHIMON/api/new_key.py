import base64 as b64

from ..kee import Kee

from .error import error_400, error_401

from typing import Union, Dict, Any, List
from ..__init__ import Page, Json

def new_key(self, pwd: str, redirect: bool) -> Union[Page, Json]:
	if self.security.correct_pwd(pwd):
		self.cache["key"]=b64.b64encode(
			Kee(2048).private()
		).decode()

		#makes sure changes are saved
		self.storage.lock(pwd)

		return self.index(), 200

	return error_401()
