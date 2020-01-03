from .error import error_200

from typing import Dict
from ..__init__ import Json

def devmode(self, data: Dict) -> Json:
	self.cache_mapper["developer"]=(data["devmode"]=="true")

	return error_200()
