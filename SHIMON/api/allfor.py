from .external import api_allfor
from .error import error_200, error_400

from typing import Union, Dict, Any, List
from ..__init__ import Page, Json

def allfor(self, data: Dict) -> Json:
	if "allfor" in data:
		raw=api_allfor(self, data["allfor"])

		if raw!=False:
			return error_200(raw)

	return error_400()
