from SHIMON.api.external import api_friends
from SHIMON.api.error import error_200, error_400

from SHIMON.__init__ import HttpResponse

def friends(self, _: None, redirect: bool) -> HttpResponse:
	return error_200(api_friends(self))
