from .external import api_allfor
from .error import error_200, error_400

from ..__init__ import HttpResponse

def allfor(self, user: str, redirect: bool) -> HttpResponse:
	raw=api_allfor(self, user)

	if raw==False:
		return error_400()

	return error_200(raw) # type: ignore
