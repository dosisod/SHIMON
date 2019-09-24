from flask import Flask, request, make_response, abort
from werkzeug.exceptions import HTTPException
from datetime import datetime, timedelta
from flask_restful import Resource, Api
from flask.json import jsonify
from waitress import serve
import traceback
import json
import os

from security import check_all, check_local, check_allowed, check_session
from session import session_start
from storage import unlock, lock
from renderer import render
from api import api_handle

class Shimon:
	def __init__(self):
		self.VERSION="0.0.21"

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

		#these are also stored in the cache, but are not available untill the cache is unlocked
		self.developer=False #(default) turns developer mode off
		self.darkmode=False #(default) turns darkmode off

	def error(self, ex): #redirects after error msg
		err=500
		if isinstance(ex, HTTPException):
			err=ex.code #handle internal error

		tb="" #if there was a traceback and user is a developer, show traceback on screen
		if isinstance(ex, BaseException) and self.developer:
			tb=traceback.format_exc()

		elif type(ex) is int:
			#error must be a valid user-defined int
			if 300<=ex and ex<=417:
				err=ex #handle self assigned error

			else:
				err=400 #handle invalid error

		return render(self, "error.html", error=err, url=request.url, traceback=tb)

	def index(self): #index page
		check_local()

		if not os.path.isfile("data.gpg"): #if cache doesnt exist create and then open page
			return session_start(self, True)

		ret=check_session(self)
		if not self.cache or ret: #make sure that the user is allowed to see the index page
			return render(self, "login.html")

		res=make_response(render(self, "index.html"))
		res.set_cookie("uname", "", expires=0) #uname not needed, clear it

		return res

	def settings(self):
		ret=check_all(self)
		if ret: return ret

		return render(self, "settings.html", seconds=self.expires, darkmode=self.darkmode)

	def account(self):
		ret=check_all(self)
		if ret: return ret

		return render(self, "account.html", version=self.VERSION)

	def msg(self, uuid):
		ret=check_all(self)
		if ret: return ret

		#make sure requested user is in friends list
		for friend in self.cache["friends"]:
			if friend["id"]==uuid:
				res=make_response(render(self, "msg.html"))
				res.set_cookie("uname", uuid)

				return res

		#400 bad request
		abort(400)

	def add(self):
		ret=check_all(self)
		if ret: return ret

		return render(self, "add.html")

	def login(self): #handles login page
		check_local()

		return render(self, "login.html")

	def api(self): #api method
		check_local()

		return api_handle(self, request.form.to_dict()) #sends data to seperate method to handle