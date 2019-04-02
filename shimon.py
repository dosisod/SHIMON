from flask import Flask, request, render_template
from werkzeug.exceptions import HTTPException
from flask_restful import Resource, Api
from flask.json import jsonify
from waitress import serve

from security import check_local
from storage import unlock
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
		return render_template("index.html")

	def login(self): #handles login page
		check_local()
		return render_template("login.html")

	def api(self): #api method
		check_local()

		data=request.args.to_dict()
		return api_handle(data) #sends data to seperate method to handle