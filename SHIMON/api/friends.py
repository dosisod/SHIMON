from SHIMON.api.external import api_friends
from SHIMON.api.error import error_200, error_400

from typing import TYPE_CHECKING
from SHIMON.__init__ import HttpResponse

if TYPE_CHECKING:
	from SHIMON.shimon import Shimon

def friends(self: "Shimon", _: None, redirect: bool) -> HttpResponse:
	return error_200(api_friends(self))
