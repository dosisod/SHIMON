from SHIMON.api.error import error_202, error_400

from typing import TYPE_CHECKING
from SHIMON.__init__ import HttpResponse

if TYPE_CHECKING:
	from SHIMON.shimon import Shimon

def msg_policy(self: "Shimon", data: str, redirect: bool) -> HttpResponse:
	if data.isdigit():
		policy=int(data)
		if 0 <= policy <= 2:
			self.cache.mapper["msg policy"]=policy

			return error_202()

	return error_400()
