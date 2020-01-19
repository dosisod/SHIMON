from flask import Flask, request, make_response, abort, Response
from werkzeug.exceptions import HTTPException
from datetime import datetime, timedelta
import traceback
import json
import os

from .api.external import api_recent, api_friends, api_allfor
from .cache_map import CacheMapper
from .api.handle import handler
from .login import LoginLimiter
from .security import Security
from .session import Session
from .storage import Storage
from .renderer import render

from typing import Union, Dict, Any, cast
from .__init__ import Page, Json

class Shimon:
	def __init__(self) -> None:
		self.VERSION="0.0.26"

		self.login_limiter=LoginLimiter(self)
		self.session=Session(self)
		self.security=Security(self)
		self.storage=Storage(self)

		self.empty_cache={"": None}

		self.cache: Dict[str, Any]=self.empty_cache

		self.cache_mapper=CacheMapper(self, {
			"msg policy": "msg_policy",
			"expiration": (self.session, "expires"),
			"developer": "developer",
			"fresh js": "fresh_js",
			"fresh css": "fresh_css",
			"theme": "theme",
			"version": "VERSION"
		})

		#stores whether or not the msg page should redraw
		self.redraw=False

		self.developer=True

		#when this flag is set, the fresh (TS compiled) js is used
		self.fresh_js=False

		#stores whether css should be taken from minified file or "fresh" files
		self.fresh_css=False

		self.theme="default"

		#changes which method of deletion to use when deleting msgs
		#0 confirm before delete (default)
		#1 require password
		#2 never ask
		self.msg_policy=0

	def error(self, ex: Union[int, Exception]) -> Page:
		codes={
			301: "Moved Permanently",
			400: "Invalid Request",
			401: "Unauthorized",
			403: "Forbidden",
			404: "Not Found",
			500: "Server Error"
		}

		return_code=500
		msg=""

		if isinstance(ex, HTTPException):
			code=cast(int, ex.code)

			if code in codes:
				msg=codes[code]

			return_code=code

		elif isinstance(ex, int):
			code=ex

			#client can only set certain http codes
			if 300<=code and code<=417:
				if code in codes:
					msg=codes[code]

				else:
					msg=""

				return_code=code

			else:
				return_code=400
				msg=codes[400]

		tb=""
		if isinstance(ex, BaseException) and self.developer:
			tb=traceback.format_exc()

		return render(
			self,
			"pages/error.html",
			error=return_code,
			url=request.url,
			traceback=tb,
			msg=msg
		), return_code

	def index(self, error: str="", uuid: str="") -> Page:
		self.security.check_local()

		if uuid:
			return self.msg(uuid)

		if not self.storage.cache_file_exists():
			return self.session.create(fresh=True)

		had_error=self.security.check_session()

		if self.cache==self.empty_cache or had_error:
			return render(self, "pages/login.html")

		res=make_response(render(
			self,
			"pages/index.html",
			error=error,
			preload=json.dumps(api_recent(self)),
			friends=json.dumps(api_friends(self))
		))

		#clear uname cookie if set
		res.set_cookie("uname", "", expires=0)

		return res

	def settings(self) -> Page:
		ret=self.security.check_all()
		if ret: return ret

		themes=[]

		theme_folder=os.getcwd()+"/SHIMON/templates/themes/"
		for filename in os.listdir(theme_folder):
			if os.path.isfile(theme_folder+filename) and filename.endswith(".css"):
				pretty_name=filename[:-4]

				themes.append((
					pretty_name,
					pretty_name
				))

		return render(self, "pages/settings.html",
			seconds=self.session.expires,
			msg_policy=self.msg_policy,
			themes=themes
		)

	def account(self) -> Page:
		ret=self.security.check_all()
		if ret: return ret

		return render(
			self,
			"pages/account.html",
			version=self.VERSION
		)

	def msg(self, uuid: str) -> Page:
		ret=self.security.check_all()
		if ret: return ret

		#make sure requested user is in friends list
		for friend in self.cache["friends"]:
			if friend["id"]==uuid:
				self.redraw=True

				res=make_response(render(
					self,
					"pages/msg.html",
					preload=json.dumps(api_allfor(self, uuid)),
					friends=json.dumps(api_friends(self))
				))
				res.set_cookie("uname", uuid)

				self.redraw=True
				return res

		abort(404)

	def add(self) -> Page:
		ret=self.security.check_all()
		if ret: return ret

		return render(self, "pages/add.html")

	def login(self) -> Page:
		self.security.check_local()

		if self.cache==self.empty_cache:
			return render(self, "pages/login.html")

		else:
			return self.index(error="Already logged in"), 301

	def api(self) -> Union[Json, Page]:
		self.security.check_local()

		return handler(self, request.form.to_dict())