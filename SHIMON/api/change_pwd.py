from SHIMON.api.error import error_202, error_400, error_401
from SHIMON.api.api_base import ApiBase

from typing import Dict, TYPE_CHECKING
from SHIMON.__init__ import HttpResponse

if TYPE_CHECKING:
	from SHIMON.shimon import Shimon

class ApiChangePwd(ApiBase):
	callname="change pwd"

	def __init__(self) -> None:
		super().__init__()

	def entry(_, self: "Shimon", pwds: Dict, redirect: bool) -> HttpResponse:
		return change_pwd(self, pwds, redirect)

def change_pwd(self: "Shimon", pwds: Dict, redirect: bool) -> HttpResponse:
	if type(pwds) is not dict:
		#message contains illegal characters if it was unable to be parsed
		return error_400()

	old=pwds.get("old", "")
	new=pwds.get("new", "")

	if old and new:
		success=self.security.update_pwd(old, new)
		if not success:
			return error_401("Password could not be updated", redirect)

		return error_202()

	else:
		return error_400()
