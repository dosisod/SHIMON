import json

from ..renderer import render

from ..__init__ import HttpResponse

def unlock(self, pwd: str, redirect: bool) -> HttpResponse:
	plain=self.storage.unlock(pwd)

	if not self.login_limiter.in_cooldown() and plain not in [None, "{}"]:
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
			return self.session.create(target="pages/warn.html")

		else:
			self.cache["version"]=self.VERSION
			return self.session.create()

	else:
		self.login_limiter.attempts+=1

		if self.login_limiter.in_cooldown():
			return render(
				self,
				"pages/login.html",
				error="Try again in " + str(self.login_limiter.time_to_wait()) + " seconds"
			), 401

		else:
			self.login_limiter.stop_cooldown()

		if self.login_limiter.exceeded_max():
			self.login_limiter.start_cooldown()

			return render(
				self,
				"pages/login.html",
				error="Try again in " + str(self.login_limiter.cooldown_duration) + " seconds"
			), 401

		elif plain=="{}":
			self.login_limiter.reset()
			return self.session.create(fresh=True)

		else:
			return render(
				self,
				"pages/login.html",
				error="Incorrect password"
			), 401
