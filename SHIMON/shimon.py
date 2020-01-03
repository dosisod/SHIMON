from flask import Flask, request, make_response, abort, Response
from werkzeug.exceptions import HTTPException
from datetime import datetime, timedelta
from flask_restful import Resource, Api
from flask.json import jsonify
from waitress import serve
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

from typing import Union
from .__init__ import Page, Json

class Shimon:
	def __init__(self) -> None:
		self.VERSION="0.0.26"

		self.login_limiter=LoginLimiter(self)
		self.session=Session(self)
		self.security=Security(self)
		self.storage=Storage(self)

		self.cache=None
		self.cache_mapper=CacheMapper(self, {
			"msg policy": "msg_policy",
			"expiration": (self.session, "expires"),
			"developer": "developer",
			"fresh js": "fresh_js",
			"fresh css": "fresh_css",
			"theme": "theme",
			"version": "VERSION"
		})

		self.redraw=False #stores whether or not the msg page should redraw

		#these are also stored in the cache, but are not available until the cache is unlocked
		self.developer=True #(default) turns developer mode off

		#when this flag is set, the fresh (TS compiled) js is used
		self.fresh_js=False

		#stores whether css should be taken from minified file or "fresh" files
		self.fresh_css=False

		#theme is current theme
		self.theme="default"

		#changes which method of deletion to use when deleting msgs
		#0 confirm before delete (default)
		#1 require password
		#2 never ask
		self.msg_policy=0

	def error(self, ex: Union[int, Exception]) -> str: #redirects after error msg
		codes={
			301: "Moved Permanently",
			400: "Invalid Request",
			401: "Unauthorized",
			404: "Not Found",
			403: "Forbidden",
			500: "Server Error"
		}

		code=500
		msg="Server Error"
		if isinstance(ex, HTTPException):
			#grabs error code name from class name, grabs http error code
			if ex.code in codes:
				msg=codes[ex.code]

			code=ex.code

		elif type(ex) is int:
			#error must be a valid user-defined int
			if 300<=ex and ex<=417:
				if ex in codes:
					msg=codes[ex]

				else:
					msg=""

				code=ex #handle self assigned error

			else:
				code=400 #handle invalid error
				msg=codes[400]

		tb="" #if there was a traceback and user is a developer, show traceback on screen
		if isinstance(ex, BaseException) and self.developer:
			tb=traceback.format_exc()

		return render(self, "pages/error.html", error=code, url=request.url, traceback=tb, msg=msg), code

	def index(self, error: str="", uuid: str="") -> Page: #index page
		self.security.check_local()

		if uuid:
			return self.msg(uuid)

		if not self.storage.cache_file_exists():
			return self.session.create(fresh=True)

		ret=self.security.check_session()
		if not self.cache or ret: #make sure that the user is allowed to see the index page
			return render(self, "pages/login.html")

		res=make_response(render(
			self,
			"pages/index.html",
			error=error,
			preload=json.dumps(api_recent(self)),
			friends=json.dumps(api_friends(self))
		))
		res.set_cookie("uname", "", expires=0) #uname not needed, clear it

		return res

	def settings(self) -> Page:
		ret=self.security.check_all()
		if ret: return ret

		themes=[] #finds and displays all available themes
		for file in os.listdir(os.getcwd()+"/SHIMON/templates/themes/"):
			if os.path.isfile(os.getcwd()+"/SHIMON/templates/themes/"+file) and file.endswith(".css"):
				#becaue of the way the dropdown renderer works, the value and the innertext will be the same
				themes.append((file[:-4], file[:-4]))

		return render(self, "pages/settings.html",
			seconds=self.session.expires,
			msg_policy=self.msg_policy,
			themes=themes
		)

	def account(self) -> Page:
		ret=self.security.check_all()
		if ret: return ret

		return render(self, "pages/account.html", version=self.VERSION)

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

		#user not in friends list, return 404
		abort(404)

	def add(self) -> Page:
		ret=self.security.check_all()
		if ret: return ret

		return render(self, "pages/add.html")

	def login(self) -> Page: #handles login page
		self.security.check_local()

		#if user is already logged in, return index
		if self.cache:
			return self.index(error="Already logged in"), 301

		else:
			return render(self, "pages/login.html")

	#api can return json, or an HTML page, it depends on the call made
	def api(self) -> Union[Json, Page]:
		self.security.check_local()

		return handler(self, request.form.to_dict()) #sends data to seperate method to handle