from flask import render_template, make_response, abort
from datetime import datetime, timedelta
import base64 as b64
import os

def session_start(self):
	res=make_response(render_template("index.html"))

	#creates session id
	self.session=b64.urlsafe_b64encode(os.urandom(32)).decode().replace("=","")
	res.set_cookie("session", self.session)

	return res

def session_check(self, data):
	if "session" in data:
		if self.session==data["session"]:
			return

	abort(403)