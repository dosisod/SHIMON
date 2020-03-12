from SHIMON.api.error import error_202, error_400

from SHIMON.__init__ import HttpResponse

def expiration_timer(self, data: str, redirect: bool) -> HttpResponse:
	if data.isdigit():
		seconds=int(data)
		if 900 <= seconds <= 86400:
			self.cache.mapper["expiration"]=seconds

			return error_202()

	return error_400()
