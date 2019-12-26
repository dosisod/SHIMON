from flask import abort
import json

from .api_calls import *

from typing import Union, Dict
from ..__init__ import Page, Json

def handler(self, data: Dict) -> Union[Page, Json]: #handles all api requests
	for attr in data: #loop through and convert to json
		data[attr]=api_decode(data[attr])

	if "unlock" in data and not self.cache: #try and unlock cache (if cache is not unlocked)
		return unlock(self, data)

	ret=self.security.check_all()
	if ret: return ret

	for callname, func in calls.items():
		if callname in data:
			return func(self, data)

	#if anything above exits and gets to here, make sure the user knows of the error
	abort(500)

def api_decode(s: str) -> Union[Dict, str]: #decodes json if possible
	if s.startswith("[") or s.startswith("{"):
		try:
			return json.loads(s) #potentialy json, try to parse
		except:
			pass

	return s #return if not json or if the json was malformed