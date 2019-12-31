from .external import api_recent
from .error import error_200, error_400

from typing import Union, Dict, Any, List
from ..__init__ import Page, Json

def recent(self, data: Dict) -> Json:
	if "recent" in data:
		return error_200(api_recent(self))

	return error_400()
