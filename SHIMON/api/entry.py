from flask import abort
import json

from SHIMON.api.api_calls import *

from typing import Union, Dict, List, Optional, TYPE_CHECKING
from SHIMON.__init__ import HttpResponse

if TYPE_CHECKING:
	from SHIMON.shimon import Shimon

def api_entry(self: "Shimon", data: Dict) -> HttpResponse:
	unlock_pwd=data.get("unlock")
	if unlock_pwd is not None:
		if self.cache.is_empty():
			return ApiUnlock().entry(self, unlock_pwd, True)

		return self.index(error="Already logged in", code=301)

	ret=self.security.check_all() # type: Optional[HttpResponse]
	if ret: return ret

	redirect=data.get("redirect", False)

	for apicall in apicalls:
		if apicall.callname in data:
			return apicall.entry(
				self,
				data[apicall.callname],
				redirect
			)

	return error_400(redirect=redirect)