from flask import render_template
from flask.json import jsonify

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
		return api_return("data", False, ["stuff"])

	return api_return("other", True, data)

def api_return(desc, fail, data): #creates json to be returned
	return {"type": desc, "fail": fail, "data": data}