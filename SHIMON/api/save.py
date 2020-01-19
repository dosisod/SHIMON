from .error import error_200

from typing import Union, Dict
from ..__init__ import Json, Page

def save(self, pwd: str, redirect: bool) -> Union[Json, Page]:
	storage_error=self.storage.save(pwd)

	if storage_error: return storage_error

	self.cache_mapper.update([
		"msg policy",
		"expiration",
		"developer"
	])

	return error_200()
