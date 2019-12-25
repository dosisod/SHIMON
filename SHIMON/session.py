from flask import make_response, Response
from datetime import datetime, timedelta
from flask.json import jsonify
import base64 as b64
import json
import os

from .api.external import api_friends, api_recent
from .api.error import error
from .renderer import render
from .storage import lock
from .kee import kee

from typing import Union, Dict
from .__init__ import Page

class Session:
	def __init__(self):
		self.session=None
		self.lastcall=datetime.now()
		self.expires=3600

	def create(self, external_self, fresh: bool=False, target: str="pages/index.html") -> Page:
		if fresh: #if starting with a fresh (new) cache, set it up
			external_self.cache={ #fill cache with these default values
				"friends": [],
				"history": [],

				#sha512 for password "123", this will change when password is reset
				"sha512": "3c9909afec25354d551dae21590bb26e38d53f2173b8d3dc3eee4c047e7ab1c1eb8b85103e3be7ba613b31bb5c9c36214dc9f14a42fd7a2fdb84856bca5c44c2",

				#base64 encoded private key for user
				"key": b64.b64encode(kee(2048).private()).decode(),

				"expiration": 3600,
				"developer": False,

				"version": external_self.VERSION,

				#default theme is default (light) theme
				"theme": "default"
			}
			lock(self, "123") #save default cache right away

		res=make_response(render(
			external_self,
			target,
			preload=json.dumps(api_recent(external_self)),
			friends=json.dumps(api_friends(external_self))
		))

		#creates session id
		self.session=b64.urlsafe_b64encode(os.urandom(32)).decode().replace("=","")
		res.set_cookie("session", self.session)
		self.keepalive()

		return res

	def check(self, external_self, data: Dict) -> Union[Page]:
		if "session" in data:
			if datetime.now()>(self.lastcall+timedelta(seconds=self.expires)):
				self.kill()

			elif self.session==data["session"]:
				self.keepalive()
				return

		return error(
			401,
			render(
				external_self,
				"pages/login.html",
				msg="Session is no longer valid"
			),
			data["redirect"],
			True
		)

	def keepalive(self) -> None:
		self.lastcall=datetime.now()

	def kill(self) -> None:
		self.session=None
		self.cache=None
		self.lastcall=datetime.min