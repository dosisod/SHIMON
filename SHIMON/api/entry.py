from flask import abort
import json

from SHIMON.api.api_calls import *

from typing import Union, Dict, List, Optional
from SHIMON.__init__ import HttpResponse

def api_entry(self, data: Dict) -> HttpResponse:
	if "unlock" in data:
		if self.cache.is_empty():
			return unlock(self, data["unlock"], True)

		else:
			return self.index(error="Already logged in", code=301)

	ret=self.security.check_all() # type: Optional[HttpResponse]
	if ret: return ret

	for callname, func in calls.items():
		if callname in data:
			return func(
				self,
				data[callname],
				data["redirect"]
			)

	redirect=False
	if "redirect" in data:
		redirect=data["redirect"]

	return error_400(redirect=redirect)