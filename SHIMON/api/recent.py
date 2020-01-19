from .external import api_recent
from .error import error_200, error_400

from typing import Union, Dict, Any, List
from ..__init__ import Page, Json

def recent(self, _: None, redirect: bool) -> Json:
	return error_200(api_recent(self))
