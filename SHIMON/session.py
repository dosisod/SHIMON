from flask import make_response, Response
from datetime import datetime, timedelta
from flask.json import jsonify
import base64 as b64
import json
import os

from .error import api_error
from .renderer import render
from .storage import lock
from .kee import kee

from typing import Union, Dict
from .__init__ import Page

def session_start(self, fresh: bool=False, target: str="index.html") -> Page:
	res=make_response(render(self, target))

	#creates session id
	self.session=b64.urlsafe_b64encode(os.urandom(32)).decode().replace("=","")
	res.set_cookie("session", self.session)

	if fresh: #if starting with a fresh (new) cache, set it up
		self.cache={ #fill cache with these default values
			"friends": [],
			"history": [],

			#sha512 for password "123", this will change when password is reset
			"sha512": "3c9909afec25354d551dae21590bb26e38d53f2173b8d3dc3eee4c047e7ab1c1eb8b85103e3be7ba613b31bb5c9c36214dc9f14a42fd7a2fdb84856bca5c44c2",

			#base64 encoded private key for user
			"key": b64.b64encode(kee(2048).private()).decode(),

			"expiration": 3600,
			"developer": False,

			"version": self.VERSION
		}
		lock(self, "123") #save default cache right away

	session_keepalive(self)

	return res

def session_check(self, data: Dict) -> Union[Page]:
	if "session" in data:
		if datetime.now()>(self.lastcall+timedelta(seconds=self.expires)):
			#if session has expired, clear it
			session_kill(self)

		elif self.session==data["session"]:
			session_keepalive(self)
			return

	#if the session is no longer valid go back to the login page
	return api_error(
		401,
		render(self, "login.html", msg="Session is no longer valid"),
		data["redirect"],
		True
	)

def session_keepalive(self) -> None:
	self.lastcall=datetime.now()

def session_kill(self) -> None:
	self.session=None
	self.cache=None
	self.lastcall=datetime.min