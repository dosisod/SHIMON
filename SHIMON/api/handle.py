from contextlib import suppress
from flask import abort
import json

from .api_calls import *

from typing import Union, Dict, List, cast
from ..__init__ import AnyResponse

def handler(self, data: Dict) -> AnyResponse:
	for attr in data:
		data[attr]=try_json_convert(data[attr])

	if "unlock" in data:
		if self.cache==self.empty_cache:
			return unlock(self, data["unlock"], True)

		else:
			return self.index(error="Already logged in"), 301

	ret=self.security.check_all()
	if ret: return ret

	for callname, func in calls.items():
		if callname in data:
			return func(
				self,
				data[callname],
				data["redirect"]=="true"
			)

	redirect="false"
	if "redirect" in data:
		redirect=data["redirect"]

	return error_400(redirect=redirect)

def try_json_convert(string: str) -> Union[Dict, List, str]:
	if string.startswith("[") or string.startswith("{"):
		with suppress(json.decoder.JSONDecodeError):
			return cast(
				Union[Dict, List],
				json.loads(string)
			)

	return string