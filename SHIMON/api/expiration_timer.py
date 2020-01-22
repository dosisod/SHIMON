from .error import error_202, error_400

from typing import Dict
from ..__init__ import Json

def expiration_timer(self, data: str, redirect: bool) -> Json:
	if data.isdigit():
		seconds=int(data)
		if 900 <= seconds <= 86400:
			self.cache_mapper["expiration"]=seconds

			return error_202()

	return error_400()
