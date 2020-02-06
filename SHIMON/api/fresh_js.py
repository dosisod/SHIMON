import os

from .error import error_200

from ..__init__ import HttpResponse

def fresh_js(self, enable: bool, redirect: bool) -> HttpResponse:
	#check if there is a compiled js file (could be any .js file)
	if os.path.isfile("SHIMON/static/js/api.js"):
		self.cache.mapper["fresh js"]=enable

	else:
		self.cache.mapper["fresh js"]=False

	return error_200()
