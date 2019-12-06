from datetime import datetime
import json

from ..renderer import render
from ..session import session_start
from .. import storage

from typing import Dict
from ..__init__ import Page

def unlock(self, data: Dict) -> Page:
	plain=storage.unlock(data["unlock"])
	if not time()-self.start<self.cooldown and plain: #if not in cooldown and the cache was decrypted
		self.cache=json.loads(plain) #cache decrypted, save to shimon

		cache_to_self(self, "expiration", "expires")
		cache_to_self(self, "msg policy", "msg_policy")
		cache_to_self(self, "developer")
		cache_to_self(self, "theme")
		cache_to_self(self, "fresh js", "fresh_js")

		#versions dont match, warn user of possible quirks
		if self.cache["version"]!=self.VERSION:
			self.cache["version"]=self.VERSION
			return session_start(self, target="warn.html")

		#if not, procceed like normal
		else:
			self.cache["version"]=self.VERSION
			return session_start(self)

	else:
		self.attempts+=1 #if there is an error, add one to attempts

		if time()-self.start<self.cooldown: #if user hasnt waited long enough let them know
			return render(self, "login.html", error="Try again in "+str(round(self.start-time()+self.cooldown, 1))+" seconds")

		else: #restart timer if user has waited long enough
			self.start=0

		if self.attempts>=self.maxtries: #if the user has attempted too many times
			self.start=time() #start cooldown timer
			self.attempts=0 #reset attempt timer

			return render(self, "login.html", error="Try again in "+str(self.cooldown)+" seconds")

		elif plain=="{}":
			return session_start(self, True)

		else:
			return render(self, "login.html", error="Incorrect password")

def time() -> int:
	return round(datetime.today().timestamp(), 1)

def cache_to_self(self, cached: str, stored: str=None) -> None:
	#use same name if there is no 3rd param
	if stored is None:
		stored=cached

	#replace each setting with default if not set, replace current with cache if it is set
	if cached in self.cache:
		self.__dict__[stored]=self.cache[cached]
	else:
		self.cache[cached]=self.__dict__[stored]
