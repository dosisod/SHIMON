from flask import render_template
from flask.json import jsonify

from storage import unlock

"""
api_handle data is returned like this:
{
	"type": "descriptor of type",
	"fail": True or False,
	"data": "can be anything"
}
"""

def api_handle(data): #handles all api requests
	if "unlock" in data: #try and unlock cache
		cache=unlock(data["unlock"])
		if cache: #if the cache was decrypted
			return api_return("cache", False, cache)
		elif cache=="{}": #if cache doesnt exist
			return api_return("cache", True, "Cache doesnt exist")
		else: #cache pwd is incorrect
			return api_return("cache", True, "Failed to open")

	elif "lock" in data: #user wants to encrypt cache
		return api_return("lock", False, "Lock cache")

	return api_return("other", True, data)

def api_return(desc, fail, data): #creates json to be returned
	return {"type": desc, "fail": fail, "data": data}