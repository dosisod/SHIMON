from .error import error_202, error_400

from typing import Union, Dict, Any, List
from ..__init__ import Page, Json

def msg_policy(self, data: Dict) -> Json:
	if data["msg policy"].isdigit():
		tmp=int(data["msg policy"])
		if 0 <= tmp and tmp <= 2:
			self.cache_mapper["msg policy"]=tmp

			return error_202()

	return error_400()
