from SHIMON.api.error import error_401

from typing import TYPE_CHECKING
from SHIMON.__init__ import HttpResponse

if TYPE_CHECKING:
	from SHIMON.shimon import Shimon

def nuke(self: "Shimon", pwd: str, redirect: bool) -> HttpResponse:
	if self.security.correct_pwd(pwd):
		return self.session.create(fresh=True)

	return error_401()
