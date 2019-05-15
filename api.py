from flask import render_template, make_response, redirect
from datetime import datetime, timedelta
from flask.json import jsonify
import json

from storage import unlock, lock

VERSION="0.0.4"

def api_handle(self, data): #handles all api requests
	if "unlock" in data: #try and unlock cache
		plain=unlock(data["unlock"])
		if not time()-self.start<self.cooldown and plain: #if not in cooldown and the cache was decrypted
			self.cache=json.loads(plain) #cache decrypted, save to shimon
			return render_template("index.html")

		else:
			self.attempts+=1 #if there is an error, add one to attempts

			if time()-self.start<self.cooldown: #if user hasnt waited long enough let them know
				return render_template("login.html", msg="Try again in "+str(round(self.start-time()+self.cooldown, 1))+" seconds")

			else: #restart timer if user has waited long enough
				self.start=0

			if self.attempts>=self.maxtries: #if the user has attempted too many times
				self.start=time() #start cooldown timer
				self.attempts=0 #reset attempt timer
				return render_template("login.html", msg="Try again in "+str(self.cooldown)+" seconds")

			elif plain=="{}":
				self.cache={}
				return render_template("index.html")

			else:
				return render_template("login.html", msg="Incorrect password")

	elif "lock" in data: #user wants to encrypt cache
		if self.cache or self.cache=={}: #if lock was sent and cache is open/never created
			lock(json.dumps(self.cache), "123") #uses "123" for testing only

			#allow user to unlock afterwards
			self.cache=None
			self.attempts=0
			self.start=0

			res=make_response(render_template("login.html", msg="Cache has been locked"))
			res.set_cookie("uname", "", expires=0)

			return res
		else:
			return render_template("login.html", msg="Please re-open cache")

	elif "status" in data:
		return jsonify({
			"version": VERSION,
			"unlocked": bool(self.cache)
		})

	elif "ping" in data:
		return jsonify({"ping":"pong"})

	elif "data" in data: #requesting data from cache
		data["data"]=api_decode(data["data"]) #if json was passed, try to decode it

		if data["data"]=="friends":
			return jsonify(self.cache["friends"])

		elif data["data"]=="recent":
			ret=[]
			
			for user in self.cache["history"]:
				ret.append({
					"id": user["id"],
					"msgs": [user["msgs"][-1]] #only get most recent message
				})

			return jsonify(ret)

		#returns all data for specified id
		elif "allfor" in data["data"]:
			for user in self.cache["history"]:
				if user["id"]==data["data"]["allfor"]:
					#return all messages from user
					return jsonify({"id":user["id"], "msgs":user["msgs"]})

			return api_return("allfor", True, "User couldnt be found")

		else:
			return api_return("data", True, "data")

	elif "msg" in data: #if user requests msg, redirect to /msg/
		return redirect("/msg/"+data["msg"])

	return api_return("other", True, data)

def api_decode(s): #decodes json if possible
	try:
		if s.startswith("[") or s.startswith("{"):
			return json.loads(s) #potentialy json, try to parse

	except:
		pass

	return s #return if invalid or not json

def time():
	return round(datetime.today().timestamp(), 1)