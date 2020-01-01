import json

from ..renderer import render

from typing import Dict
from ..__init__ import Page

def unlock(self, data: Dict) -> Page:
	plain=self.storage.unlock(data["unlock"])

	if not self.login_limiter.in_cooldown() and plain:
		self.cache=json.loads(plain) #cache decrypted, save to shimon

		cache_to_self(self, "msg policy", "msg_policy")
		cache_to_self(self, "developer")
		cache_to_self(self, "theme")
		cache_to_self(self, "fresh js", "fresh_js")
		cache_to_self(self, "fresh css", "fresh_css")

		if "expiration" in self.cache:
			self.session.expires=self.cache["expiration"]
		else:
			self.cache["expiration"]=self.session.expires

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

def cache_to_self(self, cached: str, stored: str=None) -> None:
	#use same name if there is no 3rd param
	if stored is None:
		stored=cached

	#replace each setting with default if not set, replace current with cache if it is set
	if cached in self.cache:
		self.__dict__[stored]=self.cache[cached]
	else:
		self.cache[cached]=self.__dict__[stored]
