from flask import Flask, request, abort, Response
from werkzeug.exceptions import HTTPException
from datetime import datetime, timedelta
import traceback
import json
import os

from SHIMON.api.external import api_recent, api_friends, api_allfor
from SHIMON.renderer import render, make_response
from SHIMON.cache_map import CacheMapper
from SHIMON.api.entry import api_entry
from SHIMON.login import LoginLimiter
from SHIMON.security import Security
from SHIMON.session import Session
from SHIMON.storage import Storage
from SHIMON.cache import Cache

from typing import Union
from SHIMON.__init__ import HttpResponse

class Shimon:
	def __init__(self) -> None:
		self.VERSION="0.1.1"

		self.login_limiter=LoginLimiter()
		self.session=Session(self)
		self.security=Security(self)
		self.storage=Storage(self)

		self.cache=Cache()

		self.cache.mapper=CacheMapper(self, {
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

		self.theme="auto"

		#changes which method of deletion to use when deleting msgs
		#0 confirm before delete (default)
		#1 require password
		#2 never ask
		self.msg_policy=0

	def error(self, ex: Union[int, Exception]) -> HttpResponse:
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
			code=ex.code or 500

			if code in codes:
				msg=codes[code]

			return_code=code

		elif isinstance(ex, int):
			code=ex

			#client can only set certain http codes
			if 300 <= code <= 417:
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

	def index(self, error: str="", uuid: str="", code=200) -> HttpResponse:
		self.security.check_local()

		if uuid:
			return self.msg(uuid)

		if not self.storage.cache_file_exists():
			self.storage.resetCache()
			return self.session.create()

		had_error=self.security.check_session()

		if self.cache.is_empty() or had_error:
			return render(self, "pages/login.html"), 401

		res=make_response(render(
			self,
			"pages/index.html",
			error=error,
			preload=json.dumps(api_recent(self)),
			friends=json.dumps(api_friends(self))
		))

		#clear uname cookie if set
		res.set_cookie("uname", "", expires=0)

		return res, code

	def settings(self) -> HttpResponse:
		ret=self.security.check_all()
		if ret: return ret

		themes=[]

		theme_folder=os.getcwd() + "/SHIMON/templates/themes/"
		for filename in os.listdir(theme_folder):
			if os.path.isfile(theme_folder + filename) and filename.endswith(".css"):
				pretty_name=filename[:-4]

				themes.append((
					pretty_name,
					pretty_name
				))

		return render(self, "pages/settings.html",
			seconds=self.session.expires,
			msg_policy=self.msg_policy,
			themes=themes
		), 200

	def account(self) -> HttpResponse:
		ret=self.security.check_all()
		if ret: return ret

		return render(
			self,
			"pages/account.html",
			version=self.VERSION
		), 200

	def msg(self, uuid: str) -> HttpResponse:
		ret=self.security.check_all()
		if ret:
			return ret

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

				return res, 200

		abort(404)

	def add(self) -> HttpResponse:
		ret=self.security.check_all()
		if ret: return ret

		return render(self, "pages/add.html"), 200

	def login(self) -> HttpResponse:
		self.security.check_local()

		if self.cache.is_empty():
			return render(self, "pages/login.html"), 200

		else:
			return self.index(error="Already logged in", code=301)

	def api(self) -> HttpResponse:
		self.security.check_local()

		form=request.form.to_dict()

		if form:
			if "json" in form:
				return api_entry(
					self,
					json.loads(form["json"])
				)

			else:
				return api_entry(self, form)

		else:
			return api_entry(self, request.json)