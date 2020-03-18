from SHIMON.api.error import error_200

from typing import TYPE_CHECKING
from SHIMON.__init__ import HttpResponse

if TYPE_CHECKING:
	from SHIMON.shimon import Shimon

def ping(self: "Shimon", _: None, redirect: bool) -> HttpResponse:
	return error_200("pong", redirect)
