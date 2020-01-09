from .error import error_200

from typing import Dict
from ..__init__ import Json

def ping(self, data: Dict) -> Json:
	return error_200("pong", data["redirect"])
