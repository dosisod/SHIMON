from SHIMON.api.error import error_200

from SHIMON.__init__ import HttpResponse

def ping(self, _: None, redirect: bool) -> HttpResponse:
	return error_200("pong", redirect)
