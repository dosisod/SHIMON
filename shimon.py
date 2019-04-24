from flask import Flask, request, render_template
from werkzeug.exceptions import HTTPException
from flask_restful import Resource, Api
from flask.json import jsonify
from datetime import datetime
from waitress import serve
import math
import json
import os

from security import check_local
from storage import unlock, lock
from api import api_handle

class Shimon:
	def __init__(self):
		self.cache=None #stores cached data after decryption

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

	def login(self): #handles login page
		check_local()
		return render_template("login.html")

	def api(self): #api method
		check_local()

		data=request.form.to_dict()
		out=api_handle(data, self.cache) #sends data to seperate method to handle

		if out["type"]=="cache":
			if out["fail"] or self.time()-self.start<self.cooldown or self.attempts>=self.maxtries: #if decryption failed
				self.attempts+=1

				if self.time()-self.start<self.cooldown:
					return render_template("login.html", msg="Try again in "+str(self.start-self.time()+self.cooldown)+" seconds")

				elif self.attempts>=self.maxtries:
					self.start=self.time() #start cooldown timer
					self.attempts=0 #reset attempt timer
					return render_template("login.html", msg="Try again in "+str(self.cooldown)+" seconds")

				elif out["data"]=="Cache doesnt exist":
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

		elif out["type"]=="ping":
			return jsonify({"ping":"pong"})

		#all elements in the array just return what the api returns
		elif out["type"] in ["friends", "recent", "status", "allfor"]:
			return jsonify(out["data"])

		else:
			return jsonify({"msg":"nothing happened"})

	def time(self):
		return math.ceil(datetime.today().timestamp())