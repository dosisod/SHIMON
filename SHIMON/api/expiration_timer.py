from SHIMON.api.error import error_202, error_400

from typing import TYPE_CHECKING
from SHIMON.__init__ import HttpResponse

if TYPE_CHECKING:
	from SHIMON.shimon import Shimon

def expiration_timer(self: "Shimon", data: str, redirect: bool) -> HttpResponse:
	if data.isdigit():
		seconds=int(data)
		if 900 <= seconds <= 86400:
			self.cache.mapper["expiration"]=seconds

			return error_202()

	return error_400()
