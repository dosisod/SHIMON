from flask import make_response

from ..renderer import render

from .error import error

from typing import Union, Dict
from ..__init__ import Page, Json

def lock(self, data: Dict) -> Union[Page, Json]:
	if data["redirect"]=="true": #dont kill session unless user will be directed to login
		returned_error=self.storage.lock(data["lock"])

		if returned_error: return returned_error

		#clean up object states
		self.cache=None

		self.login_limiter.reset()
		self.session.kill()

		res=make_response(render(self, "pages/login.html", error="Cache has been locked"))
		res.set_cookie("uname", "", expires=0) #clear uname cookie
		res.set_cookie("session", "", expires=0) #clear session cookie

		return res, 200

	else:
		return error(303, "", False), 303
