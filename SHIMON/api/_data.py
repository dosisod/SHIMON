from .external import api_friends, api_recent, api_allfor
from .error import error_200, error_400, error_200

from typing import Union, Dict, Any, List
from ..__init__ import Page, Json

def _data(self, data: Dict) -> Json:
	if data["data"]=="friends":
		return error_200(api_friends(self))

	elif data["data"]=="recent":

		return error_200(api_recent(self))

	#make sure that data is dict
	elif type(data["data"]) is dict:
		#returns all data for specified id
		if "allfor" in data["data"]:
			ret=api_allfor(self, data["data"]["allfor"])

			if ret or ret==[]:
				return error_200(ret)

	#if data is not set/other error happens, 400
	return error_400()
