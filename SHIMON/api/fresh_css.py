import os

from .error import error_200

from ..__init__ import HttpResponse

def fresh_css(self, enable: bool, redirect: bool) -> HttpResponse:
	#check if there is a minifed css file (could be any .css file)
	if os.path.isfile("SHIMON/static/css/font.css"):
		self.cache.mapper["fresh css"]=enable

	else:
		self.cache.mapper["fresh css"]=False

	return error_200()
