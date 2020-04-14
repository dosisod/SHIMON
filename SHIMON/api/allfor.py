from SHIMON.api.error import error_200, error_400
from SHIMON.api.external import api_allfor
from SHIMON.api.api_base import ApiBase

from typing import TYPE_CHECKING
from SHIMON.__init__ import HttpResponse

if TYPE_CHECKING:
	from SHIMON.shimon import Shimon

class ApiAllfor(ApiBase):
	callname="allfor"

	def __init__(self) -> None:
		super().__init__()

	def entry(_, self: "Shimon", user: str, redirect: bool) -> HttpResponse:
		return allfor(self, user, redirect)

def allfor(self: "Shimon", user: str, redirect: bool) -> HttpResponse:
	raw=api_allfor(self, user)

	if raw==False:
		return error_400()

	return error_200(raw)
