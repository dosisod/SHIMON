from copy import deepcopy

from .error import error_200, error_400, error_401

from typing import Dict
from ..__init__ import Page, Json

def delete_msg(self, data: Dict) -> Json:
	if type(data["delete msg"]) is not dict:
		#message contains illegal characters if it was unable to be parsed
		return error_400()

	if "id" in data["delete msg"] and "index" in data["delete msg"]:
		#verify password if msg policy requires password
		if "pwd" in data["delete msg"] and self.msg_policy==1:
			if self.security.correct_pwd(self, data["delete msg"]["pwd"]):
				pass

			else:
				#user typed in wrong password
				return error_401()

		index=0
		if type(data["delete msg"]["index"]) is int:
			index=data["delete msg"]["index"]

		elif type(data["delete msg"]["index"]) is str:
			if data["delete msg"]["index"].isdigit():
				index=int(data["delete msg"]["index"])

		else:
			return error_400("Index is not an integer")

		for friend in self.cache["friends"]:
			if friend["id"]==data["delete msg"]["id"]:
				for i, hist in enumerate(self.cache["history"]):
					if hist["id"]==data["delete msg"]["id"]:
						if index<0 or index>=len(hist["msgs"]):
							return error_400("Index is out of bounds")

						else:
							self.cache["history"][i]["msgs"].pop(index)

							self.redraw=True
							return error_200("Message deleted")

	return error_400()
