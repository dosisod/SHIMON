from SHIMON.api.error import error_200
from SHIMON.api.api_base import ApiBase

from typing import TYPE_CHECKING
from SHIMON.__init__ import HttpResponse

if TYPE_CHECKING:
	from SHIMON.shimon import Shimon

class ApiPing(ApiBase):
	def __init__(self) -> None:
		super().__init__()

	def entry(_, self: "Shimon", __: None, redirect: bool) -> HttpResponse:
		return ping(self, __, redirect)

def ping(self: "Shimon", _: None, redirect: bool) -> HttpResponse:
	return error_200("pong", redirect)
