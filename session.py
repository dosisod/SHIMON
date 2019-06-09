from flask import render_template, make_response, abort
from datetime import datetime, timedelta
from flask.json import jsonify
import base64 as b64
import json
import os

from storage import lock

def session_start(self, fresh=False):
	res=make_response(render_template("index.html"))

	#creates session id
	self.session=b64.urlsafe_b64encode(os.urandom(32)).decode().replace("=","")
	res.set_cookie("session", self.session)

	if fresh: #if starting with a fresh (new) cache, set it up
		self.cache={ #fill cache with these default values
			"friends": [],
			"history": [],
			#sha512 for password "123", this will change when password is reset
			"sha512": "3c9909afec25354d551dae21590bb26e38d53f2173b8d3dc3eee4c047e7ab1c1eb8b85103e3be7ba613b31bb5c9c36214dc9f14a42fd7a2fdb84856bca5c44c2",
			"expiration": 3600
		}
		lock(self, json.dumps(self.cache), "123") #save default cache right away

	session_keepalive(self)

	return res

def session_check(self, data):
	if "session" in data:
		if datetime.now()>(self.lastcall+timedelta(seconds=self.expires)):
			#if session has expired, clear it
			session_kill(self)

		elif self.session==data["session"]:
			session_keepalive(self)
			return

	if data["redirect"]=="true": #true is string not bool
		return render_template("error.html", error=401)
	else:
		return jsonify({"error":"401"})

def session_keepalive(self):
	self.lastcall=datetime.now()

def session_kill(self):
	self.session=None
	self.cache=None
	self.lastcall=datetime.min