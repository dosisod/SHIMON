from flask import request, abort, Response
from hashlib import sha512

from SHIMON.encoding import encode_anystr

from typing import AnyStr, Optional, cast, TYPE_CHECKING
from SHIMON.__init__ import HttpResponse

if TYPE_CHECKING:
	from SHIMON.shimon import Shimon

class Security:
	def __init__(self, shimon_ref: "Shimon"):
		self.shimon=shimon_ref

		self._testing=False

	def check_all(self) -> Optional[HttpResponse]:
		self.check_local()
		self.check_allowed()
		return self.check_session()

	def check_session(self) -> Optional[HttpResponse]:
		return self.shimon.session.check({
			"session": request.cookies.get("session", ""),
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

	def correct_pwd(self, pwd: AnyStr) -> bool:
		return cast(str, self.shimon.cache["sha512"])==sha512hex(pwd)

	#updates hash to new if old is correct, else return false
	def update_pwd(self, plain: AnyStr, new_pwd: AnyStr) -> bool:
		if self.correct_pwd(plain):
			self.shimon.cache["sha512"]=sha512hex(new_pwd)

			return True

		return False

def sha512hex(pwd: AnyStr) -> str:
	return sha512(encode_anystr(pwd)).hexdigest()