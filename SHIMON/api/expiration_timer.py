from .error import error_202, error_400

from typing import Dict
from ..__init__ import Json

def expiration_timer(self, data: Dict) -> Json:
	seconds=data["expiration timer"]

	if seconds.isdigit():
		seconds=int(seconds)
		if seconds>=900 and seconds<=86400:
			self.cache_mapper["expiration"]=seconds

			return error_202()

	return error_400()
