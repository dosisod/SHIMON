from flask import Flask, request, render_template, make_response, abort
from werkzeug.exceptions import HTTPException
from flask_restful import Resource, Api
from flask.json import jsonify
from waitress import serve
import json
import os

from security import check_all, check_local, check_allowed
from storage import unlock, lock
from api import api_handle

class Shimon:
	def __init__(self):
		self.cache=None #stores cached data after decryption

		#stuff related to login timeouts
		self.attempts=0
		self.maxtries=3
		self.start=0
		self.cooldown=10

	def error(self, ex): #redirects after error msg
		err=500
		if isinstance(ex, HTTPException):
			err=ex.code
		return render_template("error.html", error=err)

	def index(self): #index page
		check_local()

		if self.cache: #load page if cache is open
			return render_template("index.html")

		elif not os.path.isfile("data.gpg"): #if cache doesnt exist create and then open page
			self.cache={}
			return render_template("index.html")

		else: #if cache isnt loaded, request unlock cache
			return render_template("login.html")

	def msg(self, uuid):
		check_all(self.cache)

		#make sure requested user is in friends list
		for friend in self.cache["friends"]:
			if friend["id"]==uuid:
				res=make_response(render_template("msg.html"))
				res.set_cookie("uname", uuid)

				return res

		#400 bad request
		abort(400)

	def login(self): #handles login page
		check_local()

		return render_template("login.html")

	def api(self): #api method
		check_local()

		return api_handle(self, request.form.to_dict()) #sends data to seperate method to handle