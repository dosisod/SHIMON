from SHIMON.api.external import api_recent
from SHIMON.api.error import error_200, error_400

from SHIMON.__init__ import HttpResponse

def recent(self, _: None, redirect: bool) -> HttpResponse:
	return error_200(api_recent(self))
