from SHIMON.api.error import error_200
from SHIMON.api.api_base import ApiBase

from typing import TYPE_CHECKING
from SHIMON.__init__ import HttpResponse

if TYPE_CHECKING:
	from SHIMON.shimon import Shimon

class ApiStatus(ApiBase):
	callname="status"

	def __init__(self) -> None:
		super().__init__()

	def entry(_, self: "Shimon", __: None, redirect: bool) -> HttpResponse:
		return status(self, __, redirect)


def status(self: "Shimon", _: None, redirect: bool) -> HttpResponse:
	return error_200({
		"version": self.VERSION,
		"unlocked": not self.cache.is_empty(),
		"developer": self.developer,
		"msg policy": self.msg_policy
	}, redirect)
