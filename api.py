from flask import render_template, make_response, redirect
from datetime import datetime, timedelta
from base64 import b64encode as b64
from flask.json import jsonify
from hashlib import sha512
import json

from session import session_start, session_check, session_keepalive, session_kill
from security import correct_pwd, update_pwd
from storage import unlock, lock
from error import api_error
from kee import kee

def api_handle(self, data): #handles all api requests
	if "unlock" in data: #try and unlock cache
		plain=unlock(data["unlock"])
		if not time()-self.start<self.cooldown and plain: #if not in cooldown and the cache was decrypted
			self.cache=json.loads(plain) #cache decrypted, save to shimon
			self.expires=self.cache["expiration"]
			self.developer=self.cache["developer"]

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
				return session_start(self, True)

			else:
				return render_template("login.html", msg="Incorrect password")

	check=session_check(self, data)
	if check:
		return check #if session_check fails, redirect will be returned

	if "send msg" in data:
		message=api_decode(data["send msg"])

		if "uname" in message and "msg" in message: #make sure data is set
			for friend in self.cache["friends"]:
				if message["uname"]==friend["id"]: #make sure friend is in friends list
					for i, hist in enumerate(self.cache["history"]):
						if hist["id"]==message["uname"]: #find friend in history
							self.cache["history"][i]["msgs"].append({
								"sending": True,
								"msg": message["msg"]
							})

							return api_error(200, "OK", False, False)

		return api_error(400, "Message could not be sent", False, False) #user didnt set something/made an invalid request

	elif "save" in data: #user only wants to encrypt cache
		ret=lock(self, data["save"])

		#if the lock returns an error, re-return it
		if ret:
			return ret

		return api_error(200, "OK", False, False)

	elif "lock" in data: #user wants to encrypt cache and log out
		if data["redirect"]=="true": #dont kill session unless user will be directed to login
			ret=lock(self, data["lock"])

			#if the lock returns an error, goto error page
			if ret:
				return ret

			#allow user to unlock afterwards
			self.cache=None
			self.attempts=0
			self.start=0

			session_kill(self)

			res=make_response(render_template("login.html", msg="Cache has been locked"))
			res.set_cookie("uname", "", expires=0) #clear uname cookie
			res.set_cookie("session", "", expires=0) #clear session cookie

			return res

		else:
			return api_error(303, "", False, True)

	elif "change pwd" in data:
		data["change pwd"]=api_decode(data["change pwd"])

		if "old" in data["change pwd"] and "new" in data["change pwd"]:
			tmp=update_pwd(self, data["change pwd"]["old"], data["change pwd"]["new"])
			if tmp:
				return api_error(202, "Lock or save to apply changes", False, False) #password was updated successfull

			else:
				return api_error(401, "Password could not be updated", data["redirect"], False) #incorrect info was given

		else:
			return api_error(400, "Invalid Request", data["redirect"], False) #invalid request

	elif "new key" in data:
		if data["new key"]:
			#password required to change key
			if correct_pwd(self, data["new key"]):
				self.cache["key"]=str(b64(kee(2048).private()))

				lock(self, data["new key"]) #makes sure changes are saved

				return render_template("index.html")

			return api_error(401, "Incorrect password", False, False)

		return api_error(400, "Invalid request", False, False)

	elif "expiration timer" in data:
		num=data["expiration timer"]
		#timer was within acceptable range
		if num.isdigit():
			num=int(num)
			if num>=900 and num<=86400:
				self.expires=num
				self.cache["expiration"]=num

				return api_error(202, "Lock or save to apply changes", False, False)

		return api_error(400, "Invalid request", False, False)

	elif "devmode" in data:
		#if devmode is true, enable devmode, else disable
		self.cache["developer"]=(data["devmode"]=="true")

		return api_error(202, "Lock or save to apply changes", False, False)

	elif "nuke" in data: #user wants to delete cache
		if correct_pwd(self, data["nuke"]):
			#start a new session as if it is booting for the first time
			return session_start(self, True)

		return api_error(401, "Invalid password", False, False)

	elif "status" in data:
		return api_error(200, {
			"version": self.VERSION,
			"unlocked": bool(self.cache),
			"developer": self.developer
		}, data["redirect"], False)

	elif "ping" in data:
		return api_error(200, "pong", data["redirect"], False)

	elif "data" in data: #requesting data from cache
		data["data"]=api_decode(data["data"]) #if json was passed, try to decode it

		if data["data"]=="friends":
			return api_error(200, self.cache["friends"], False, False)

		elif data["data"]=="recent":
			ret=[]
			
			for user in self.cache["history"]:
				ret.append({
					"id": user["id"],
					"msgs": [user["msgs"][-1]] #only get most recent message
				})

			return api_error(200, ret, False, False)

		#returns all data for specified id
		elif "allfor" in data["data"]:
			for user in self.cache["history"]:
				if user["id"]==data["data"]["allfor"]:
					#return all messages from user
					return api_error(200, {"id":user["id"], "msgs":user["msgs"]}, False, False)

		return api_error(400, "Invalid request", False, False)

	elif "msg" in data: #if user requests msg, redirect to /msg/
		return redirect("/msg/"+data["msg"])

	return api_error(400, "Invalid request", False, False)

def api_decode(s): #decodes json if possible
	try:
		if s.startswith("[") or s.startswith("{"):
			return json.loads(s) #potentialy json, try to parse

	except:
		pass

	return s #return if invalid or not json

def time():
	return round(datetime.today().timestamp(), 1)