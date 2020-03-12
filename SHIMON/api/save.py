from SHIMON.api.error import error_200

from typing import Optional
from SHIMON.__init__ import HttpResponse

def save(self, pwd: str, redirect: bool) -> HttpResponse:
	storage_error=self.storage.save(pwd) # type: Optional[HttpResponse]

	if storage_error: return storage_error

	self.cache.mapper.update([
		"msg policy",
		"expiration",
		"developer"
	])

	return error_200()
