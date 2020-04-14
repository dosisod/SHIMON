from SHIMON.api.api_base import ApiBase
from SHIMON.api.error import error_200

from typing import Optional, TYPE_CHECKING
from SHIMON.__init__ import HttpResponse

if TYPE_CHECKING:
	from SHIMON.shimon import Shimon

class ApiSave(ApiBase):
	callname="save"

	def __init__(self) -> None:
		super().__init__()

	def entry(_, self: "Shimon", pwd: str, redirect: bool) -> HttpResponse:
		return save(self, pwd, redirect)

def save(self: "Shimon", pwd: str, redirect: bool) -> HttpResponse:
	storage_error=self.storage.save(pwd) # type: Optional[HttpResponse]

	if storage_error: return storage_error

	self.cache.mapper.update([
		"msg policy",
		"expiration",
		"developer"
	])

	return error_200()
