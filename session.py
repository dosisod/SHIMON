from flask import render_template, make_response, abort
from datetime import datetime, timedelta
from flask.json import jsonify
import base64 as b64
import os

def session_start(self):
	res=make_response(render_template("index.html"))

	#creates session id
	self.session=b64.urlsafe_b64encode(os.urandom(32)).decode().replace("=","")
	res.set_cookie("session", self.session)

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

	return jsonify({"error":"401"})

def session_keepalive(self):
	self.lastcall=datetime.now()

def session_kill(self):
	self.session=None
	self.lastcall=datetime.min