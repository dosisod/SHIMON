from .external import api_friends
from .error import error_200, error_400

from typing import Union, Dict, Any, List
from ..__init__ import Page, Json

def friends(self, data: Dict) -> Json:
	if "friends" in data:
		return error_200(api_friends(self))

	return error_400()
