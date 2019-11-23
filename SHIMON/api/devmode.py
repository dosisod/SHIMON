from .error import error_200

from typing import Dict
from ..__init__ import Json

def devmode(self, data: Dict) -> Json:
	#if devmode is true, enable devmode, else disable
	self.cache["developer"]=(data["devmode"]=="true")
	self.developer=self.cache["developer"]

	return error_200()
