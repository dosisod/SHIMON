from SHIMON.api.error import error_200
from SHIMON.api.api_base import ApiBase

from typing import TYPE_CHECKING
from SHIMON.__init__ import HttpResponse

if TYPE_CHECKING:
	from SHIMON.shimon import Shimon

class ApiDevmode(ApiBase):
	callname="devmode"

	def __init__(self) -> None:
		super().__init__()

	@ApiBase.bool_required
	def entry(_, self: "Shimon", enable: bool, redirect: bool) -> HttpResponse:
		return devmode(self, enable, redirect)

def devmode(self: "Shimon", enable: bool, redirect: bool) -> HttpResponse:
	self.cache.mapper["developer"]=enable

	return error_200()
