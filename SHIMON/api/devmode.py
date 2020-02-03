from .error import error_200

from typing import Dict
from ..__init__ import Json

def devmode(self, enable: str, redirect: bool) -> Json:
	self.cache.mapper["developer"]=(enable=="true")

	return error_200()
