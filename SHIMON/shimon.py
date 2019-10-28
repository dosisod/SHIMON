from flask import Flask, request, make_response, abort, Response
from werkzeug.exceptions import HTTPException
from datetime import datetime, timedelta
from flask_restful import Resource, Api
from flask.json import jsonify
from waitress import serve
import traceback
import json
import os

from .security import check_all, check_local, check_allowed, check_session
from .api_external import api_recent, api_friends, api_allfor
from .session import session_start
from .storage import unlock, lock
from .renderer import render
from .api import api_handle

from typing import Union
from .__init__ import Page, Json

class Shimon:
	def __init__(self) -> None:
		self.VERSION="0.0.23"

		self.cache=None #stores cached data after decryption

		#stuff related to login timeouts
		self.attempts=0
		self.maxtries=3
		self.start=0
		self.cooldown=10

		#session related vars
		self.session=None
		self.lastcall=datetime.now()
		self.expires=3600 #(default) time to expire in seconds

		self.redraw=False #stores whether or not the msg page should redraw

		#these are also stored in the cache, but are not available untill the cache is unlocked
		self.developer=False #(default) turns developer mode off
		self.darkmode=False #(default) turns darkmode off

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
			500: "Server Error"
		}

		err=500
		msg="Server Error"
		if isinstance(ex, HTTPException):
			#grabs error code name from class name, grabs http error code
			if ex.code in codes:
				msg=codes[ex.code]

			err=ex.code

		tb="" #if there was a traceback and user is a developer, show traceback on screen
		if isinstance(ex, BaseException) and self.developer:
			tb=traceback.format_exc()

		elif type(ex) is int:
			#error must be a valid user-defined int
			if 300<=ex and ex<=417:
				if ex in codes:
					msg=codes[ex]

				err=ex #handle self assigned error

			else:
				err=400 #handle invalid error
				msg=codes[400]

		return render(self, "error.html", error=err, url=request.url, traceback=tb, msg=msg)

	def index(self) -> Page: #index page
		check_local()

		if not os.path.isfile("data.gpg"): #if cache doesnt exist create and then open page
			return session_start(self, True)

		ret=check_session(self)
		if not self.cache or ret: #make sure that the user is allowed to see the index page
			return render(self, "login.html")

		res=make_response(render(
			self,
			"index.html",
			preload=json.dumps(api_recent(self)),
			friends=json.dumps(api_friends(self))
		))
		res.set_cookie("uname", "", expires=0) #uname not needed, clear it

		return res

	def settings(self) -> Page:
		ret=check_all(self)
		if ret: return ret

		themes=[] #finds and displays all available themes
		for file in os.listdir(os.getcwd()+"/templates/themes/"):
			if os.path.isfile(os.getcwd()+"/templates/themes/"+file) and file.endswith(".css"):
				#becaue of the way the dropdown renderer works, the value and the innertext will be the same
				themes.append((file[:-4], file[:-4]))

		return render(self, "settings.html",
			seconds=self.expires,
			darkmode=self.darkmode,
			msg_policy=self.msg_policy,
			themes=themes
		)

	def account(self) -> Page:
		ret=check_all(self)
		if ret: return ret

		return render(self, "account.html")

	def msg(self, uuid: str) -> Page:
		ret=check_all(self)
		if ret: return ret

		#make sure requested user is in friends list
		for friend in self.cache["friends"]:
			if friend["id"]==uuid:
				self.redraw=True

				res=make_response(render(
					self,
					"msg.html",
					preload=json.dumps(api_allfor(self, uuid)),
					friends=json.dumps(api_friends(self))
				))
				res.set_cookie("uname", uuid)

				self.redraw=True
				return res

		#400 bad request
		abort(400)

	def add(self) -> Page:
		ret=check_all(self)
		if ret: return ret

		return render(self, "add.html")

	def login(self) -> Page: #handles login page
		check_local()

		return render(self, "login.html")

	#api can return json, or an HTML page, it depends on the call made
	def api(self) -> Union[Json, Page]:
		check_local()

		return api_handle(self, request.form.to_dict()) #sends data to seperate method to handle