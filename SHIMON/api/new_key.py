import base64 as b64

from SHIMON.kee import Kee

from SHIMON.api.error import error_400, error_401
from SHIMON.api.api_base import ApiBase

from typing import TYPE_CHECKING
from SHIMON.__init__ import HttpResponse

if TYPE_CHECKING:
	from SHIMON.shimon import Shimon

class ApiNewKey(ApiBase):
	callname="new key"

	def __init__(self) -> None:
		super().__init__()

	def entry(_, self: "Shimon", pwd: str, redirect: bool) -> HttpResponse:
		return new_key(self, pwd, redirect)

def new_key(self: "Shimon", pwd: str, redirect: bool) -> HttpResponse:
	if not self.security.correct_pwd(pwd):
		return self.index(error="Invalid Password", code=401)

	self.cache["key"]=b64.b64encode(
		Kee(2048).private()
	).decode()

	#makes sure changes are saved
	self.storage.lock(pwd)

	return self.index()
