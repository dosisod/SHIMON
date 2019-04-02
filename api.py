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
		else:
			return api_return("cache", True, "Failed to open")

	return api_return("other", True, data)

def api_return(desc, fail, data): #creates json to be returned
	return {"type": desc, "fail": fail, "data": data}