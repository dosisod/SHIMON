from SHIMON.renderer import render

from SHIMON.api.error import error_200, error_400
from SHIMON.api.api_base import ApiBase
from SHIMON.api.msg import history_id

from typing import Dict, TYPE_CHECKING
from SHIMON import HttpResponse

if TYPE_CHECKING:
	from SHIMON.shimon import Shimon

class ApiSendMsg(ApiBase):
	callname="send msg"

	def __init__(self) -> None:
		super().__init__()

	@ApiBase.dict_required
	def entry(_, self: "Shimon", sending: Dict, redirect: bool) -> HttpResponse:
		return send_msg(self, sending, redirect)

def send_msg(self: "Shimon", sending: Dict, redirect: bool) -> HttpResponse:
	msg=sending.get("msg")
	uname=sending.get("uname")

	if not msg or not uname or msg.isspace():
		return error_400()

	index=history_id(self, uname)

	if index < 0:
		return error_400()

	self.cache["history"][index]["msgs"].append({
		"sending": True,
		"msg": msg
	})

	self.redraw=True
	return error_200()
