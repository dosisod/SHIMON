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
		self.expires=self.cache["expiration"]

		#replace each setting with default if not set, replace current with cache if it is set
		if "msg policy" in self.cache:
			self.msg_policy=self.cache["msg policy"]
		else:
			self.cache["msg policy"]=self.msg_policy

		if "developer" in self.cache:
			self.developer=self.cache["developer"]
		else:
			self.cache["developer"]=self.developer

		if "theme" in self.cache:
			self.theme=self.cache["theme"]
		else:
			self.cache["theme"]=self.theme

		if "fresh js" in self.cache:
			self.fresh_js=self.cache["fresh js"]
		else:
			self.cache["fresh js"]=self.fresh_js

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
