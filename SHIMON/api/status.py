from SHIMON.api.error import error_200

from SHIMON.__init__ import HttpResponse

def status(self, _: None, redirect: bool) -> HttpResponse:
	return error_200({
		"version": self.VERSION,
		"unlocked": not self.cache.is_empty(),
		"developer": self.developer,
		"msg policy": self.msg_policy
	}, redirect)
