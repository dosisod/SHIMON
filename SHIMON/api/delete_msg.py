from copy import deepcopy

from .error import error_200, error_400, error_401

from typing import Dict
from ..__init__ import HttpResponse

def delete_msg(self, data: Dict, redirect: bool) -> HttpResponse:
	if type(data) is not dict:
		#message contains illegal characters if it was unable to be parsed
		return error_400()

	if "id" in data and "index" in data:
		#verify password if msg policy requires password
		if "pwd" in data and self.msg_policy==1:
			if not self.security.correct_pwd(data["pwd"]):
				return error_401()

		index=0
		if type(data["index"]) is int:
			index=data["index"]

		elif type(data["index"]) is str:
			if data["index"].isdigit():
				index=int(data["index"])
			else:
				return error_400("Index is not a valid integer")

		else:
			return error_400("Index is not a valid integer")

		if index < 0:
			return error_400("Index is out of bounds")

		for friend in self.cache["friends"]:
			if friend["id"]==data["id"]:
				for history_id, current in enumerate(self.cache["history"]):
					if current["id"]==data["id"]:
						if index >= len(current["msgs"]):
							return error_400("Index is not a valid integer")

						else:
							self.cache["history"][history_id]["msgs"].pop(index)

							self.redraw=True
							return error_200("Message deleted")

	return error_400()
