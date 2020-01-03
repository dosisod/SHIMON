import os

from .error import error_200

from typing import Dict
from ..__init__ import Json

def fresh_css(self, data: Dict) -> Json:
	#check if there is a minifed css file (could be any .css file)
	if os.path.isfile("SHIMON/static/css/font.css"):
		self.cache_mapper["fresh css"]=(data["fresh css"]=="true")

	else:
		self.cache_mapper["fresh css"]=False

	return error_200()
