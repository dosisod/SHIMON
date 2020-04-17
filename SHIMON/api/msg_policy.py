from SHIMON.api.error import error_202, error_400
from SHIMON.api.api_base import ApiBase

from typing import TYPE_CHECKING
from SHIMON.__init__ import HttpResponse

if TYPE_CHECKING:
	from SHIMON.shimon import Shimon

class ApiMsgPolicy(ApiBase):
	callname="msg policy"

	def __init__(self) -> None:
		super().__init__()

	@ApiBase.int_str_required
	def entry(_, self: "Shimon", data: str, redirect: bool) -> HttpResponse:
		return msg_policy(self, data, redirect)

def msg_policy(self: "Shimon", data: str, redirect: bool) -> HttpResponse:
	policy=int(data)
	if 0 <= policy <= 2:
		self.cache.mapper["msg policy"]=policy

		return error_202()

	return error_400()
