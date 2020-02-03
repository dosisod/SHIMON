from .error import error_200

from typing import Dict
from ..__init__ import Json

def status(self, _: None, redirect: bool) -> Json:
	return error_200({
		"version": self.VERSION,
		"unlocked": not self.cache.is_empty(),
		"developer": self.developer,
		"msg policy": self.msg_policy
	}, redirect)
