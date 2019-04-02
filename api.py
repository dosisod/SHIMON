from flask import render_template
from flask.json import jsonify

from storage import unlock

def api_handle(data): #handles all api requests
	if "unlock" in data: #try and unlock cache
		cache=unlock(data["unlock"])
		if cache:
			return {"type": "cache", "data": cache} #if successful, return it to shimon

	return {"type": "other", "data": data}