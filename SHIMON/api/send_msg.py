from ..renderer import render

from .error import error_200, error_400

from typing import Dict
from ..__init__ import HttpResponse

def send_msg(self, sending: Dict, redirect: bool) -> HttpResponse:
	if type(sending) is not dict:
		#message contains illegal characters if it was unable to be parsed
		return error_400()

	if "uname" not in sending or "msg" not in sending:
		return error_400()

	if sending["msg"].isspace():
		return error_400()

	for friend in self.cache["friends"]:
		if sending["uname"]==friend["id"]:
			for index, current in enumerate(self.cache["history"]):
				if current["id"]==sending["uname"]:
					self.cache["history"][index]["msgs"].append({
						"sending": True,
						"msg": sending["msg"]
					})

					self.redraw=True
					return error_200()

	return error_400()
