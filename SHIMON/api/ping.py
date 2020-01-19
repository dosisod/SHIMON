from .error import error_200

from typing import Dict
from ..__init__ import Json

def ping(self, _: None, redirect: bool) -> Json:
	return error_200("pong", redirect)
