from session import session_check
from flask import request, abort
from hashlib import sha512

def check_all(self): #errors if any of the below tests fails
	check_local()
	check_allowed(self.cache)
	return check_session(self)

def check_session(self):
	#make sure session exists before setting is
	session=""
	if "session" in request.cookies:
		session=request.cookies["session"]

	return session_check(self, {
		"session": session, #grab cookie from page
		"redirect": True #true since the request is coming from a click (not fetch)
	})

def check_local(): #errors if inbound IP isnt localhost
	if not request.remote_addr=="127.0.0.1":
		abort(403)

def check_allowed(cache): #errors if cache is locked
	if cache=={} or not cache:
		abort(401)

def correct_pwd(self, plain): #returns true if plain matches cache hash
	if type(plain) is str:
		plain=plain.encode()

	return self.cache["sha512"]==sha512(plain).hexdigest()

def update_pwd(self, plain, new): #updates hash to new if old is correct, else return false
	if correct_pwd(self, plain):
		if type(new) is str:
			new=new.encode()

		self.cache["sha512"]=sha512(new).hexdigest()
		return True

	return False