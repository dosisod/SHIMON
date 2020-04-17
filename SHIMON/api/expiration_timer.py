from SHIMON.api.error import error_202, error_400
from SHIMON.api.api_base import ApiBase

from typing import TYPE_CHECKING
from SHIMON.__init__ import HttpResponse

if TYPE_CHECKING:
	from SHIMON.shimon import Shimon

class ApiExpirationTimer(ApiBase):
	callname="expiration timer"

	def __init__(self) -> None:
		super().__init__()

	@ApiBase.int_str_required
	def entry(_, self: "Shimon", data: str, redirect: bool) -> HttpResponse:
		return expiration_timer(self, data, redirect)

def expiration_timer(self: "Shimon", data: str, redirect: bool) -> HttpResponse:
	seconds=int(data)
	if 900 <= seconds <= 86400:
		self.cache.mapper["expiration"]=seconds

		return error_202()

	return error_400()
