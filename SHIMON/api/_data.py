from .external import api_friends, api_recent, api_allfor
from .error import error, error_400

from typing import Union, Dict, Any, List
from ..__init__ import Page, Json

def _data(self, data: Dict) -> Json:
	if data["data"]=="friends":
		return error(200, api_friends(self), False, False)

	elif data["data"]=="recent":

		return error(200, api_recent(self), False, False)

	#make sure that data is dict
	elif type(data["data"]) is dict:
		#returns all data for specified id
		if "allfor" in data["data"]:
			ret=api_allfor(self, data["data"]["allfor"])

			if ret or ret==[]:
				return error(200, ret, False, False)

	#if data is not set/other error happens, 400
	return error_400()
