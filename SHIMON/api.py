from flask import make_response, abort, redirect, Response
from datetime import datetime, timedelta
from flask.json import jsonify
from copy import deepcopy
import base64 as b64
import json

from .session import session_start, session_check, session_keepalive, session_kill
from .api_external import api_recent, api_friends, api_allfor
from .security import correct_pwd, update_pwd
from .storage import unlock, lock
from .security import check_all
from .renderer import render
from .error import api_error
from .kee import kee

from typing import Union, Dict, Any, List
from .__init__ import Page, Json

def api_handle(self, data: Dict) -> Union[Page, Json]: #handles all api requests
	for attr in data: #loop through and convert to json
		data[attr]=api_decode(data[attr])

	if "unlock" in data and not self.cache: #try and unlock cache (if cache is not unlocked)
		plain=unlock(data["unlock"])
		if not time()-self.start<self.cooldown and plain: #if not in cooldown and the cache was decrypted
			self.cache=json.loads(plain) #cache decrypted, save to shimon
			self.expires=self.cache["expiration"]

			#if cache has developer set, override default
			#if not, put default value into cache
			if "developer" in self.cache:
				self.developer=self.cache["developer"]
			else:
				self.cache["developer"]=self.developer

			if "darkmode" in self.cache:
				self.darkmode=self.cache["darkmode"]
			else:
				self.cache["darkmode"]=self.darkmode

			#versions dont match, warn user of possible quirks
			if self.cache["version"]!=self.VERSION:
				self.cache["version"]=self.VERSION
				return session_start(self, target="warn.html")

			#if not, procceed like normal
			else:
				self.cache["version"]=self.VERSION
				return session_start(self)

		else:
			self.attempts+=1 #if there is an error, add one to attempts

			if time()-self.start<self.cooldown: #if user hasnt waited long enough let them know
				return render(self, "login.html", msg="Try again in "+str(round(self.start-time()+self.cooldown, 1))+" seconds")

			else: #restart timer if user has waited long enough
				self.start=0

			if self.attempts>=self.maxtries: #if the user has attempted too many times
				self.start=time() #start cooldown timer
				self.attempts=0 #reset attempt timer

				return render(self, "login.html", msg="Try again in "+str(self.cooldown)+" seconds")

			elif plain=="{}":
				return session_start(self, True)

			else:
				return render(self, "login.html", msg="Incorrect password")

	elif "unlock" in data and self.cache: #user requested unlock but the cache is unlocked
		#cache is logged in, handle as if the user is trying to access index
		return redirect("/")

	ret=check_all(self)
	if ret: return ret

	if "send msg" in data:
		message=data["send msg"]

		if type(message) is not dict:
			#message contains illegal characters if it was unable to be parsed
			return api_error_400()

		if "uname" in message and "msg" in message: #make sure data is set
			for friend in self.cache["friends"]:
				if message["uname"]==friend["id"]: #make sure friend is in friends list
					for i, hist in enumerate(self.cache["history"]):
						if hist["id"]==message["uname"]: #find friend in history
							self.cache["history"][i]["msgs"].append({
								"sending": True,
								"msg": message["msg"]
							})

							self.redraw=True
							return api_error(200, "OK", False, False)

		return api_error_400() #user didnt set something/made an invalid request

	elif "delete msg" in data:
		if type(data["delete msg"]) is not dict:
			#message contains illegal characters if it was unable to be parsed
			return api_error_400()

		if "id" in data["delete msg"] and "index" in data["delete msg"]:
			index=0
			if type(data["delete msg"]["index"]) is int:
				index=data["delete msg"]["index"]

			else:
				try:
					#try and get index of msg to be deleted
					index=int(data["delete msg"])

				except:
					return api_error_400("Index is not an integer")

			for friend in self.cache["friends"]:
				if friend["id"]==data["delete msg"]["id"]:
					for i, hist in enumerate(self.cache["history"]):
						if hist["id"]==data["delete msg"]["id"]:
							if index<0 or index>=len(hist["msgs"]):
								return api_error_400("Index is out of bounds")

							else:
								self.cache["history"][i]["msgs"].pop(index)

								self.redraw=True
								return api_error(200, "Message deleted", False, False)

		return api_error_400()

	elif "save" in data: #user only wants to encrypt cache
		ret=lock(self, data["save"])

		#if the lock returns an error, re-return it
		if ret:
			return ret

		#update settings if they were set since last save
		self.expires=self.cache["expiration"]
		self.developer=self.cache["developer"]
		self.darkmode=self.cache["darkmode"]

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

			res=make_response(render(self, "login.html", msg="Cache has been locked"))
			res.set_cookie("uname", "", expires=0) #clear uname cookie
			res.set_cookie("session", "", expires=0) #clear session cookie

			return res

		else:
			return api_error(303, "", False, True)

	elif "change pwd" in data:
		if type(data["change pwd"]) is not dict:
			#message contains illegal characters if it was unable to be parsed
			return api_error_400()

		if "old" in data["change pwd"] and "new" in data["change pwd"]:
			tmp=update_pwd(self, data["change pwd"]["old"], data["change pwd"]["new"])
			if tmp:
				return api_error_202() #password was updated successfull

			else:
				return api_error(401, "Password could not be updated", data["redirect"], False) #incorrect info was given

		else:
			return api_error_400(data=data) #invalid request

	elif "new key" in data:
		if data["new key"]:
			#password required to change key
			if correct_pwd(self, data["new key"]):
				self.cache["key"]=b64.b64encode(kee(2048).private()).decode()

				lock(self, data["new key"]) #makes sure changes are saved

				return render(self, "index.html")

			return api_error(401, "Incorrect password", False, False)

		return api_error_400()

	elif "expiration timer" in data:
		num=data["expiration timer"]
		#timer was within acceptable range
		if num.isdigit():
			num=int(num)
			if num>=900 and num<=86400:
				self.expires=num
				self.cache["expiration"]=num

				return api_error_202()

		return api_error_400()

	elif "darkmode" in data:
		#if darkmode is true, enable darkmode, else disable
		self.cache["darkmode"]=(data["darkmode"]=="true")
		self.darkmode=self.cache["darkmode"]

		return api_error_200()

	elif "devmode" in data:
		#if devmode is true, enable devmode, else disable
		self.cache["developer"]=(data["devmode"]=="true")
		self.developer=self.cache["developer"]

		return api_error_200()

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
		if data["data"]=="friends":
			return api_error(200, api_friends(self), False, False)

		elif data["data"]=="recent":

			return api_error(200, api_recent(self), False, False)

		#make sure that data is dict
		elif type(data["data"]) is dict:
			#returns all data for specified id
			if "allfor" in data["data"]:
				ret=api_allfor(self, data["data"]["allfor"])

				if ret or ret==[]:
					return api_error(200, ret, False, False)

		#if data is not set/other error happens, 400
		return api_error_400()

	elif "add friend" in data:
		if type(data["add friend"]) is not dict:
			#message contains illegal characters if it was unable to be parsed
			return api_error_400()

		if "name" in data["add friend"] and "id" in data["add friend"]:
			#make sure that name and id are not blank
			if data["add friend"]["name"] and data["add friend"]["id"]:
				#make sure id is not already taken
				for friend in self.cache["friends"]:
					if friend["id"]==data["add friend"]["id"]:
						return api_error(400, render(self, "index.html", error="Friend already exists"), True)

				#only append the names and ids, dont let user add extra data
				self.cache["friends"].append({
					"id": data["add friend"]["id"],
					"name": data["add friend"]["name"]
				})

				#add blank msg history to cache history
				self.cache["history"].append({
					"id": data["add friend"]["id"],
					"msgs": []
				})

				return api_error(200, render(self, "index.html"), True)

		return api_error(400, render(self, "index.html", error="Invalid request"), True)

	else:
		#if the call is not recognized, throw a 400 error
		return api_error_400()

	abort(500) #if anything above exits and gets to here, make sure the user knows of the error

def api_decode(s: str) -> Union[Dict, str]: #decodes json if possible
	try:
		if s.startswith("[") or s.startswith("{"):
			return json.loads(s) #potentialy json, try to parse

	except:
		pass

	return s #return if not json or if the json was malformed

def time() -> int:
	return round(datetime.today().timestamp(), 1)

#below is a bunch of api_error wrappers for common calls
#data stores default message for the given error type, it can be changed

def api_error_400(error: str="Invalid Request", data: Any=False) -> Page:
	return api_error(400, error, data, rethrow=False)

#usually used when the user needs to save/lock to fulfill request
def api_error_202(error: str="Lock or save to apply changes", data: Any=False) -> Page:
	return api_error(202, error, data, rethrow=False)

def api_error_200(error: str="OK", data: Any=False) -> Page:
	return api_error(200, error, data, rethrow=False)