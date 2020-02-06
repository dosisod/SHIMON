from contextlib import suppress
from flask import abort
import json

from .api_calls import *

from typing import Union, Dict, List, cast
from ..__init__ import AnyResponse

def handler(self, data: Dict) -> AnyResponse:
	if "unlock" in data:
		if self.cache.is_empty():
			return unlock(self, data["unlock"], True)

		else:
			return self.index(error="Already logged in", code=301)

	ret=self.security.check_all()
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