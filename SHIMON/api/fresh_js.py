import os

from .error import error_200

from typing import Dict
from ..__init__ import Json

def fresh_js(self, data: Dict) -> Json:
	#check if there is a compiled js file (could be any .js file)
	if os.path.isfile("SHIMON/static/js/api.js"):
		self.fresh_js=self.cache["fresh js"]=(data["fresh js"]=="true")

	else:
		self.fresh_js=self.cache["fresh js"]=False

	return error_200()