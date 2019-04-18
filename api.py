from flask import render_template
from flask.json import jsonify
import json

from storage import unlock

VERSION="0.0.1"

"""
api_handle data is returned like this:
{
	"type": "descriptor of type",
	"fail": True or False,
	"data": "can be anything"
}
"""

def api_handle(data, cache=None): #handles all api requests
	if "unlock" in data: #try and unlock cache
		plain=unlock(data["unlock"])
		if plain: #if the cache was decrypted
			return api_return("cache", False, plain)

		elif plain=="{}": #if cache doesnt exist
			return api_return("cache", True, "Cache doesnt exist")

		else: #cache pwd is incorrect
			return api_return("cache", True, "Failed to open")

	elif "lock" in data: #user wants to encrypt cache
		return api_return("lock", False, "Lock cache")

	elif "status" in data:
		return api_return("status", False, {
			"version": VERSION
		})

	elif "ping" in data:
		return api_return("ping", False, "Pinged")

	elif "data" in data: #requesting data from cache
		data["data"]=api_decode(data["data"]) #if json was passed, try to decode it

		if data["data"]=="friends":
			return api_return("friends", False, cache["friends"])

		elif data["data"]=="recent":
			ret=[]
			
			for user in cache["history"]:
				ret.append({
					"id": user["id"],
					"msgs": [user["msgs"][0]] #only get most recent message
				})

			return api_return("recent", False, ret)

		#returns all data for specified id
		elif "allfor" in data["data"]:
			for user in cache["history"]:
				if user["id"]==data["data"]["allfor"]:
					#return all messages from user
					return api_return("allfor", False, {"id":user["id"], "msgs":user["msgs"]})

			return api_return("allfor", True, "User couldnt be found")

		else:
			
			return api_return("data", True, "data")

	return api_return("other", True, data)

def api_return(desc, fail, data): #creates json to be returned
	return {"type": desc, "fail": fail, "data": data}

def api_decode(s): #decodes json if possible
	try:
		if s.startswith("[") or s.startswith("{"):
			return json.loads(s) #potentialy json, try to parse

		else:
			return s #s is a string not object, return anyways
	except:
		return s #error, return original string