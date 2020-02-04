from .error import error_200

from ..__init__ import HttpResponse

def save(self, pwd: str, redirect: bool) -> HttpResponse:
	storage_error=self.storage.save(pwd)

	if storage_error: return storage_error

	self.cache.mapper.update([
		"msg policy",
		"expiration",
		"developer"
	])

	return error_200()
