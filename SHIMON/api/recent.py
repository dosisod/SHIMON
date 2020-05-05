from SHIMON.api.external import api_recent
from SHIMON.api.error import error_200, error_400
from SHIMON.api.api_base import ApiBase

from typing import TYPE_CHECKING
from SHIMON import HttpResponse

if TYPE_CHECKING:
	from SHIMON.shimon import Shimon

class ApiRecent(ApiBase):
	callname="recent"

	def __init__(self) -> None:
		super().__init__()

	def entry(_, self: "Shimon", __: None, redirect: bool) -> HttpResponse:
		return recent(self, __, redirect)

def recent(self: "Shimon", _: None, redirect: bool) -> HttpResponse:
	return error_200(api_recent(self))
