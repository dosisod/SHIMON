from .error import error_200

from ..__init__ import HttpResponse

def devmode(self, enable: str, redirect: bool) -> HttpResponse:
	self.cache.mapper["developer"]=(enable=="true")

	return error_200()
