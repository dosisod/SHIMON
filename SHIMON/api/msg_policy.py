from SHIMON.api.error import error_202, error_400

from SHIMON.__init__ import HttpResponse

def msg_policy(self, data: str, redirect: bool) -> HttpResponse:
	if data.isdigit():
		policy=int(data)
		if 0 <= policy <= 2:
			self.cache.mapper["msg policy"]=policy

			return error_202()

	return error_400()
