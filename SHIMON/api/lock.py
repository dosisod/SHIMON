from SHIMON.renderer import render, make_response
from SHIMON.api.error import error_400

from typing import Optional, TYPE_CHECKING
from SHIMON.__init__ import HttpResponse

if TYPE_CHECKING:
	from SHIMON.shimon import Shimon

def lock(self: "Shimon", pwd: str, redirect: bool) -> HttpResponse:
	#dont kill session unless user will be directed to login
	if redirect:
		returned_error=self.storage.lock(pwd) # type: Optional[HttpResponse]

		if returned_error: return returned_error

		#clean up object states
		self.cache.wipe()
		self.session.kill()

		res=make_response(render(
			self,
			"pages/login.html",
			error="Cache has been locked"
		))

		res.set_cookie("uname", "", expires=0)
		res.set_cookie("session", "", expires=0)

		return res, 200

	else:
		return error_400()
