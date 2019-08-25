from datetime import datetime, timedelta
from flask import make_response, abort
from flask.json import jsonify
from hashlib import sha256
from copy import deepcopy
import base64 as b64
import json

from session import session_start, session_check, session_keepalive, session_kill
from security import correct_pwd, update_pwd
from storage import unlock, lock
from security import check_all
from renderer import render
from error import api_error
from kee import kee

def api_handle(self, data): #handles all api requests
	for attr in data: #loop through and convert to json
		data[attr]=api_decode(data[attr])

	if "unlock" in data: #try and unlock cache
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

	ret=check_all(self)
	if ret: return ret

	if "send msg" in data:
		message=data["send msg"]

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

	elif "delete msg" in data:
		if "id" in data["delete msg"] and "index" in data["delete msg"]:
			index=0
			if type(data["delete msg"]["index"]) is int:
				index=data["delete msg"]["index"]

			else:
				try:
					#try and get index of msg to be deleted
					index=int(data["delete msg"])

				except:
					return api_error(400, "Index is not an integer", False, False)

			for friend in self.cache["friends"]:
				if friend["id"]==data["delete msg"]["id"]:
					for i, hist in enumerate(self.cache["history"]):
						if hist["id"]==data["delete msg"]["id"]:
							if index<0 or index>=len(hist["msgs"]):
								return api_error(400, "Index is out of bounds", False, False)

							else:
								self.cache["history"][i]["msgs"].pop(index)
								return api_error(200, "Message deleted", False, False)

		return api_error(400, "Invalid request", False, False)

	elif "save" in data: #user only wants to encrypt cache
		ret=lock(self, data["save"])

		#if the lock returns an error, re-return it
		if ret:
			return ret

		#update settings if they were set since last save
		self.expires=self.cache["expiration"]
		self.developer=self.cache["developer"]

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
				self.cache["key"]=b64.b64encode(kee(2048).private()).decode()

				lock(self, data["new key"]) #makes sure changes are saved

				return render(self, "index.html")

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
		if data["data"]=="friends":
			ret=deepcopy(self.cache["friends"])
			for i in ret:
				i["hash"]=sha256hex(i["id"])

			return api_error(200, ret, False, False)

		elif data["data"]=="recent":
			ret=[]

			for user in self.cache["history"]:
				tmp={
					"id": user["id"],
					"hash": sha256hex(user["id"]),
				}

				if len(user["msgs"]) > 0: #if there are msgs to get, get most recent one
					tmp["msgs"]=[user["msgs"][-1]]

				else: #if this is a new user, show must recent msg as blank
					tmp["msgs"]=[{
						"sending": False,
						"msg": ""
					}]

				ret.append(tmp)

			return api_error(200, ret, False, False)

		#returns all data for specified id
		elif "allfor" in data["data"]:
			for user in self.cache["history"]:
				if user["id"]==data["data"]["allfor"]:
					#return all messages from user
					return api_error(200, {
						"id": user["id"],
						"msgs": user["msgs"],
						"hash": sha256hex(user["id"])
					}, False, False)

		return api_error(400, "Invalid request", False, False)

	elif "add friend" in data:
		if "name" in data["add friend"] and "id" in data["add friend"]:
			#make sure that name and id are not blank
			if data["add friend"]["name"] and data["add friend"]["id"]:
				#make sure id is not already taken
				for friend in self.cache["friends"]:
					if friend["id"]==data["add friend"]["id"]:
						return api_error(400, render(self, "index.html", error="Friend already exists"), True, False)

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

				return api_error(200, render(self, "index.html"), True, False)

		return api_error(400, render(self, "index.html", error="Invalid request"), True, False)

	else:
		#if the call is not recognized, throw a 400 error
		return api_error(400, "Invalid request", False, False)

	abort(500) #if anything above exits and gets to here, make sure the user knows of the error

def api_decode(s): #decodes json if possible
	try:
		if s.startswith("[") or s.startswith("{"):
			return json.loads(s) #potentialy json, try to parse

	except:
		pass

	return s #return if not json or if the json was malformed

def time():
	return round(datetime.today().timestamp(), 1)

def sha256hex(data): #returns the sha256 hex digest for given data
	if type(data) is str:
		return sha256(data.encode()).hexdigest()

	else:
		return sha256(data).hexdigest()