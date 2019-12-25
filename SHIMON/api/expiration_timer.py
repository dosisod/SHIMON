from .error import error_202, error_400

from typing import Dict
from ..__init__ import Json

def expiration_timer(self, data: Dict) -> Json:
	num=data["expiration timer"]
	#timer was within acceptable range
	if num.isdigit():
		num=int(num)
		if num>=900 and num<=86400:
			self.session.expires=num
			self.cache["expiration"]=num

			return error_202()

	return error_400()
