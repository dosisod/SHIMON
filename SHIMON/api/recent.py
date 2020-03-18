from SHIMON.api.external import api_recent
from SHIMON.api.error import error_200, error_400

from typing import TYPE_CHECKING
from SHIMON.__init__ import HttpResponse

if TYPE_CHECKING:
	from SHIMON.shimon import Shimon

def recent(self: "Shimon", _: None, redirect: bool) -> HttpResponse:
	return error_200(api_recent(self))
