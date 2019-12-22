from .error import error

from typing import Dict
from ..__init__ import Json

def ping(self, data: Dict) -> Json:
	return error(200, "pong", data["redirect"], False)
