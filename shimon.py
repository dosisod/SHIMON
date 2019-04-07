from flask import Flask, request, render_template
from werkzeug.exceptions import HTTPException
from flask_restful import Resource, Api
from flask.json import jsonify
from waitress import serve

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
		if self.cache:
			return render_template("index.html")
		else: #if cache isnt loaded, unlock cache
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
				return render_template("login.html", msg=out["data"])
			else:
				self.cache=out["data"] #cache decrypted, save to shimon
				return render_template("index.html")

		elif out["type"]=="lock":
			if self.cache: #if lock was sent and cache is open
				lock(self.cache, "123") #uses "123" for testing only
				self.cache=None #clear cache
				return jsonify({"msg":"cache locked"})

		else:
			return jsonify({"msg":"nothing happened"})