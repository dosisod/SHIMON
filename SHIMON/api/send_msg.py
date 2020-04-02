from SHIMON.renderer import render

from SHIMON.api.error import error_200, error_400
from SHIMON.api.util import history_id

from typing import Dict, TYPE_CHECKING
from SHIMON.__init__ import HttpResponse

if TYPE_CHECKING:
	from SHIMON.shimon import Shimon

def send_msg(self: "Shimon", sending: Dict, redirect: bool) -> HttpResponse:
	if type(sending) is not dict:
		#message contains illegal characters if it was unable to be parsed
		return error_400()

	msg=sending.get("msg", None)
	uname=sending.get("uname", None)

	if not msg or not uname or msg.isspace():
		return error_400()

	index=history_id(self, uname)

	if index >= 0:
		self.cache["history"][index]["msgs"].append({
			"sending": True,
			"msg": msg
		})

		self.redraw=True
		return error_200()

	return error_400()
