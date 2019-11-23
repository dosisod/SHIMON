from ..renderer import render

from .error import error, error_400

from typing import Dict
from ..__init__ import Json

def send_msg(self, data: Dict) -> Json:
	message=data["send msg"]

	if type(message) is not dict:
		#message contains illegal characters if it was unable to be parsed
		return error_400()

	if "uname" in message and "msg" in message: #make sure data is set
		#make sure that the message is not only whitespace
		if not message["msg"].isspace():
			for friend in self.cache["friends"]:
				if message["uname"]==friend["id"]: #make sure friend is in friends list
					for i, hist in enumerate(self.cache["history"]):
						if hist["id"]==message["uname"]: #find friend in history
							self.cache["history"][i]["msgs"].append({
								"sending": True,
								"msg": message["msg"]
							})

							self.redraw=True
							return error(200, "OK", False, False)

	return error_400() #user didnt set something/made an invalid request
