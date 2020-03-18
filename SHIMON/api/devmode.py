from SHIMON.api.error import error_200

from typing import TYPE_CHECKING
from SHIMON.__init__ import HttpResponse

if TYPE_CHECKING:
	from SHIMON.shimon import Shimon

def devmode(self: "Shimon", enable: bool, redirect: bool) -> HttpResponse:
	self.cache.mapper["developer"]=enable

	return error_200()
