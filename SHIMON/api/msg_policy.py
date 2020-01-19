from .error import error_202, error_400

from typing import Union, Dict, Any, List
from ..__init__ import Page, Json

def msg_policy(self, data: str, redirect: bool) -> Json:
	if data.isdigit():
		policy=int(data)
		if 0 <= policy and policy <= 2:
			self.cache_mapper["msg policy"]=policy

			return error_202()

	return error_400()
