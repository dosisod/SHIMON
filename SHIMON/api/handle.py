from flask import abort
import json

from .api_calls import *

from typing import Union, Dict
from ..__init__ import Page, Json

def handler(self, data: Dict) -> Union[Page, Json]:
	for attr in data:
		data[attr]=try_json_convert(data[attr])

	if "unlock" in data:
		if not self.cache:
			return unlock(self, data)

		else:
			return self.index(error="Already logged in"), 301

	ret=self.security.check_all()
	if ret: return ret

	for callname, func in calls.items():
		if callname in data:
			return func(self, data)

	redirect="false"
	if "redirect" in data:
		redirect=data["redirect"]

	return error_400(redirect=redirect)

def try_json_convert(string: str) -> Union[Dict, str]:
	if string.startswith("[") or string.startswith("{"):
		try:
			return json.loads(string)
		except:
			pass

	return string