from flask import render_template, make_response, redirect
from datetime import datetime, timedelta
from flask.json import jsonify
from hashlib import sha512
import json

from session import session_start, session_check, session_keepalive, session_kill
from storage import unlock, lock

VERSION="0.0.8"

def api_handle(self, data): #handles all api requests
	if "unlock" in data: #try and unlock cache
		plain=unlock(data["unlock"])
		if not time()-self.start<self.cooldown and plain: #if not in cooldown and the cache was decrypted
			self.cache=json.loads(plain) #cache decrypted, save to shimon
			return session_start(self)

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
				return session_start(self)

			else:
				return render_template("login.html", msg="Incorrect password")

	check=session_check(self, data)
	if check:
		return check #if session_check fails, redirect will be returned

	if "save" in data: #user only wants to encrypt cache
		ret=lock(self, json.dumps(self.cache), data["save"])

		#if if the lock returns an error, re-return it
		if ret:
			return ret

		return jsonify("OK")

	elif "lock" in data: #user wants to encrypt cache and log out
		ret=lock(self, json.dumps(self.cache), data["lock"])

		#if the lock returns an error, goto error page
		if ret:
			return render_template("error.html", error="401")

		#allow user to unlock afterwards
		self.cache=None
		self.attempts=0
		self.start=0

		session_kill(self)

		res=make_response(render_template("login.html", msg="Cache has been locked"))
		res.set_cookie("uname", "", expires=0) #clear uname cookie
		res.set_cookie("session", "", expires=0) #clear session cookie

		return res

	elif "change pwd" in data:
		data["change pwd"]=api_decode(data["change pwd"])

		#if old and new are set
		if "old" in data["change pwd"] and "new" in data["change pwd"]:
			#check if old password is correct
			if self.cache["sha512"]==sha512(data["change pwd"]["old"].encode()).hexdigest():
				#password matches, set new password
				self.cache["sha512"]=sha512(data["change pwd"]["new"].encode()).hexdigest()

				return jsonify("OK")

			else:
				return jsonify({"error":"401"})

		else:
			return jsonify({"error":"400"})

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

	return jsonify({"error":400})

def api_decode(s): #decodes json if possible
	try:
		if s.startswith("[") or s.startswith("{"):
			return json.loads(s) #potentialy json, try to parse

	except:
		pass

	return s #return if invalid or not json

def time():
	return round(datetime.today().timestamp(), 1)