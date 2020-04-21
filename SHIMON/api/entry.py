from flask import abort
import json

from SHIMON.api.api_calls import *

from typing import Union, Dict, List, Optional, TYPE_CHECKING
from SHIMON.__init__ import HttpResponse

if TYPE_CHECKING:
	from SHIMON.shimon import Shimon

def api_entry(self: "Shimon", data: Dict) -> HttpResponse:
	redirect=data.get("redirect", False)
	unlock_error=self.security.check_all() # type: Optional[HttpResponse]

	for apicall in apicalls:
		if apicall.callname in data:
			if apicall.unlock_required and unlock_error:
				return unlock_error

			return apicall.entry(
				self,
				data[apicall.callname],
				redirect
			)

	if unlock_error:
		return unlock_error

	return error_400(redirect=redirect)