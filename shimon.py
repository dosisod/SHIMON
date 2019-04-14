from flask import Flask, request, render_template
from werkzeug.exceptions import HTTPException
from flask_restful import Resource, Api
from flask.json import jsonify
from waitress import serve
import json
import os

from security import check_local
from storage import unlock, lock
from api import api_handle

class Shimon:
	def __init__(self):
		self.cache=None #stores cached data after decryption

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

	def login(self): #handles login page
		check_local()
		return render_template("login.html")

	def api(self): #api method
		check_local()

		data=request.form.to_dict()
		out=api_handle(data) #sends data to seperate method to handle

		if out["type"]=="cache":
			if out["fail"]: #if decryption failed
				if out["data"]=="Cache doesnt exist":
					self.cache={}
					return render_template("index.html")
				else:
					return render_template("login.html", msg=out["data"])
			else:
				self.cache=json.loads(out["data"]) #cache decrypted, save to shimon
				return render_template("index.html")

		elif out["type"]=="lock":
			if self.cache or self.cache=={}: #if lock was sent and cache is open/never created
				lock(json.dumps(self.cache), "123") #uses "123" for testing only
				self.cache=None #clear cache
				return render_template("login.html", msg="Cache has been locked")
			else:
				return render_template("login.html", msg="Please re-open cache")

		elif out["type"]=="status":
			return jsonify(out["data"])

		elif out["type"]=="ping":
			return jsonify({"ping":"pong"})

		else:
			return jsonify({"msg":"nothing happened"})