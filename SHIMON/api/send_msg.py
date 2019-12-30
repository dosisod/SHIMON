from ..renderer import render

from .error import error_200, error_400

from typing import Dict
from ..__init__ import Json

def send_msg(self, data: Dict) -> Json:
	message=data["send msg"]

	if type(message) is not dict:
		#message contains illegal characters if it was unable to be parsed
		return error_400()

	if "uname" not in message or "msg" not in message:
		return error_400()

	if message["msg"].isspace():
		return error_400()

	for friend in self.cache["friends"]:
		if message["uname"]==friend["id"]:
			for index, current in enumerate(self.cache["history"]):
				if current["id"]==message["uname"]:
					self.cache["history"][index]["msgs"].append({
						"sending": True,
						"msg": message["msg"]
					})

					self.redraw=True
					return error_200()

	return error_400()
