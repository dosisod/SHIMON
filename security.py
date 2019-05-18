from flask import request, abort

def check_all(cache): #errors if any of the below tests fails
	check_local()
	check_allowed(cache)

def check_local(): #errors if inbound IP isnt localhost
	if not request.remote_addr=="127.0.0.1":
		abort(403)

def check_allowed(cache): #errors if cache is locked
	if cache=={} or not cache:
		abort(401)