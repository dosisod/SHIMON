from .external import api_friends, api_recent, api_allfor
from .error import error_200, error_400, error_200

from typing import Union, Dict, Any, List
from ..__init__ import Page, Json

def _data(self, data: Dict) -> Json:
	if data["data"]=="friends":
		return error_200(api_friends(self))

	elif data["data"]=="recent":
		return error_200(api_recent(self))

	elif type(data["data"]) is dict:
		if "allfor" in data["data"]:
			ret=api_allfor(self, data["data"]["allfor"])

			if ret==False:
				return error_400()

			elif ret or ret==[]:
				return error_200(ret)

	return error_400()
