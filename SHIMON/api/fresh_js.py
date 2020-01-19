import os

from .error import error_200

from typing import Dict
from ..__init__ import Json

def fresh_js(self, enable: str, redirect: bool) -> Json:
	#check if there is a compiled js file (could be any .js file)
	if os.path.isfile("SHIMON/static/js/api.js"):
		self.cache_mapper["fresh js"]=(enable=="true")

	else:
		self.cache_mapper["fresh js"]=False

	return error_200()
