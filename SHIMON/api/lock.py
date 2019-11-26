from flask import make_response

from ..session import session_kill
from ..renderer import render
from .. import storage

from .error import error

from typing import Union, Dict
from ..__init__ import Page, Json

def lock(self, data: Dict) -> Union[Page, Json]:
	if data["redirect"]=="true": #dont kill session unless user will be directed to login
		ret=storage.lock(self, data["lock"])

		#if the lock returns an error, goto error page
		if ret:
			return ret

		#allow user to unlock afterwards
		self.cache=None
		self.attempts=0
		self.start=0

		session_kill(self)

		res=make_response(render(self, "login.html", error="Cache has been locked"))
		res.set_cookie("uname", "", expires=0) #clear uname cookie
		res.set_cookie("session", "", expires=0) #clear session cookie

		return res

	else:
		return error(303, "")
