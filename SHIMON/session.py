from datetime import datetime, timedelta
from flask import Response
import base64 as b64
import json
import os

from SHIMON.api.external import api_friends, api_recent
from SHIMON.renderer import render, make_response
from SHIMON.api.error import error
from SHIMON.kee import Kee

from typing import Optional, Dict
from SHIMON.__init__ import HttpResponse

class Session:
	def __init__(self, shimon_ref):
		self.shimon=shimon_ref

		self.session=""
		self.lastcall=datetime.now()
		self.expires=3600

	def create(self, fresh: bool=False, target: str="pages/index.html") -> HttpResponse:
		if fresh:
			#fill cache with default values
			self.shimon.cache.load({
				"friends": [],
				"history": [],

				#hash for "123", can be changed in settings
				"sha512": "3c9909afec25354d551dae21590bb26e38d53f2173b8d3dc3eee4c047e7ab1c1eb8b85103e3be7ba613b31bb5c9c36214dc9f14a42fd7a2fdb84856bca5c44c2",

				"key": b64.b64encode(
					Kee(2048).private()
				).decode(),

				"expiration": 3600,
				"developer": False,

				"version": self.shimon.VERSION,

				"theme": "auto"
			})

			#save default cache right away
			self.shimon.storage.lock("123")

		res=make_response(render(
			self.shimon,
			target,
			preload=json.dumps(api_recent(self.shimon)),
			friends=json.dumps(api_friends(self.shimon))
		))

		self.session=b64.urlsafe_b64encode(os.urandom(32)).decode().replace("=","")
		res.set_cookie("session", self.session)
		self.keepalive()

		return res, 200

	def check(self, data: Dict) -> Optional[HttpResponse]:
		if "session" in data:
			if datetime.now() > (self.lastcall + timedelta(seconds=self.expires)):
				self.kill()

			elif self.session==data["session"]:
				self.keepalive()
				return None

		return error(
			401,
			render(
				self.shimon,
				"pages/login.html",
				msg="Session is no longer valid"
			),
			data["redirect"],
			True
		)

	def keepalive(self) -> None:
		self.lastcall=datetime.now()

	def kill(self) -> None:
		self.session=""
		self.shimon.cache.wipe()
		self.lastcall=datetime.min