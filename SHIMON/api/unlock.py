import json

from ..renderer import render

from typing import Dict
from ..__init__ import Page

def unlock(self, data: Dict) -> Page:
	plain=self.storage.unlock(data["unlock"])

	if not self.login_limiter.in_cooldown() and plain:
		self.cache=json.loads(plain) #cache decrypted, save to shimon

		self.cache_mapper.update("msg policy")
		self.cache_mapper.update("developer")
		self.cache_mapper.update("theme")
		self.cache_mapper.update("fresh js")
		self.cache_mapper.update("fresh css")
		self.cache_mapper.update("expiration")

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
				error="Try again in "+str(self.login_limiter.time_to_wait())+" seconds"
			)

		else:
			self.login_limiter.stop_cooldown()

		if self.login_limiter.exceeded_max():
			self.login_limiter.start_cooldown()

			return render(
				self,
				"pages/login.html",
				error="Try again in "+str(self.login_limiter.cooldown_duration)+" seconds"
			)

		elif plain=="{}":
			return self.session.create(fresh=True)

		else:
			return render(self, "pages/login.html", error="Incorrect password")
