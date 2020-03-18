from copy import deepcopy

from SHIMON.api.error import error_200, error_400, error_401
from SHIMON.api.util import history_id

from typing import Dict, TYPE_CHECKING
from SHIMON.__init__ import HttpResponse

if TYPE_CHECKING:
	from SHIMON.shimon import Shimon

def delete_msg(self: "Shimon", data: Dict, redirect: bool) -> HttpResponse:
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

		hist_id=history_id(self, data["id"])

		if hist_id >= 0:
			msgs=self.cache["history"][hist_id]["msgs"]

			if index >= len(msgs):
				return error_400("Index is not a valid integer")

			else:
				msgs.pop(index)

				self.redraw=True
				return error_200("Message deleted")

	return error_400()
