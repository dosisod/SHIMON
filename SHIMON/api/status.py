from SHIMON.api.error import error_200

from typing import TYPE_CHECKING
from SHIMON.__init__ import HttpResponse

if TYPE_CHECKING:
	from SHIMON.shimon import Shimon

def status(self: "Shimon", _: None, redirect: bool) -> HttpResponse:
	return error_200({
		"version": self.VERSION,
		"unlocked": not self.cache.is_empty(),
		"developer": self.developer,
		"msg policy": self.msg_policy
	}, redirect)
