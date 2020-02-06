from .error import error_200

from ..__init__ import HttpResponse

def devmode(self, enable: bool, redirect: bool) -> HttpResponse:
	self.cache.mapper["developer"]=enable

	return error_200()
