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

	pwd=data.get("pwd", "")
	if pwd and self.msg_policy==1:
		if not self.security.correct_pwd(pwd):
			return error_401()

	index=data.get("index", None)
	if isinstance(index, str):
		try:
			index=int(index)
		except ValueError:
			return error_400("Index is not a valid integer")

	elif not isinstance(index, int):
		return error_400("Index is not a valid integer")

	if index < 0:
		return error_400("Index is out of bounds")

	hist_id=history_id(self, data.get("id", ""))

	if hist_id >= 0:
		msgs=self.cache["history"][hist_id]["msgs"]

		if index >= len(msgs):
			return error_400("Index is not a valid integer")

		msgs.pop(index)

		self.redraw=True
		return error_200("Message deleted")

	return error_400()
