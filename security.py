from flask import request, abort

def check_local(): #returns false if inbound IP isnt localhost
	if not request.remote_addr=="127.0.0.1":
		abort(403)