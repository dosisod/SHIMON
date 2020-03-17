from base64 import urlsafe_b64encode as urlb64encode
from datetime import datetime, timedelta
from flask import Response
import base64 as b64
import json
import os

from SHIMON.api.external import api_friends, api_recent
from SHIMON.renderer import render, make_response
from SHIMON.api.error import error

from typing import Optional, Dict
from SHIMON.__init__ import HttpResponse

class Session:
	def __init__(self, shimon_ref) -> None:
		self.shimon=shimon_ref

		self.session=""
		self.lastcall=datetime.now()
		self.expires=3600

	def create(self, target: str="pages/index.html") -> HttpResponse:
		res=make_response(render(
			self.shimon,
			target,
			preload=json.dumps(api_recent(self.shimon)),
			friends=json.dumps(api_friends(self.shimon))
		))

		self.session=urlb64encode(
			os.urandom(32)
		).decode().replace("=", "")

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