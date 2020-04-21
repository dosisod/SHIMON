import json

from SHIMON.api.api_base import ApiBase

from SHIMON.renderer import render

from typing import TYPE_CHECKING
from SHIMON.__init__ import HttpResponse

if TYPE_CHECKING:
	from SHIMON.shimon import Shimon

class ApiUnlock(ApiBase):
	callname="unlock"

	def __init__(self) -> None:
		super().__init__()

	@ApiBase.str_required
	def entry(_, self: "Shimon", pwd: str, redirect: bool) -> HttpResponse:
		if self.cache.is_empty():
			return unlock(self, pwd, redirect)

		return self.index(error="Already logged in", code=301)

def unlock(self: "Shimon", pwd: str, redirect: bool) -> HttpResponse:
	plain=self.storage.unlock(pwd)

	if not self.login_limiter.in_cooldown() and plain and plain!="{}":
		self.cache.load(json.loads(plain))

		self.cache.mapper.update([
			"msg policy",
			"developer",
			"theme",
			"fresh js",
			"fresh css",
			"expiration"
		])

		if self.cache["version"]!=self.VERSION:
			self.cache["version"]=self.VERSION
			return self.session.create(target="pages/warn.jinja")

		else:
			self.cache["version"]=self.VERSION
			return self.session.create()

	self.login_limiter.attempts+=1

	if self.login_limiter.in_cooldown():
		return render(
			self,
			"pages/login.jinja",
			error=f"Try again in {self.login_limiter.time_to_wait()} seconds"
		), 401

	else:
		self.login_limiter.stop_cooldown()

	if self.login_limiter.exceeded_max():
		self.login_limiter.start_cooldown()

		return render(
			self,
			"pages/login.jinja",
			error=f"Try again in {self.login_limiter.cooldown_duration} seconds"
		), 401

	elif plain=="{}":
		self.login_limiter.reset()
		self.storage.resetCache()
		return self.session.create()

	return render(
		self,
		"pages/login.jinja",
		error="Incorrect password"
	), 401
