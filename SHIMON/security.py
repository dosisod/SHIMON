from flask import request, abort, Response
from SHIMON.session import session_check
from hashlib import sha512

from typing import Union, Dict
from SHIMON.__init__ import Stringish, Page

#errors if any of the below tests fails
def check_all(self) -> Union[Page]:
	check_local()
	check_allowed(self.cache)
	return check_session(self)

def check_session(self) -> Union[Page]:
	#make sure session exists before setting it
	session=""
	if "session" in request.cookies:
		session=request.cookies["session"]

	return session_check(self, {
		"session": session, #grab cookie from page
		"redirect": True #true since the request is coming from a click (not fetch)
	})

#errors if inbound IP isnt localhost
def check_local() -> None:
	if not request.remote_addr=="127.0.0.1":
		abort(403)

#errors if cache is locked
def check_allowed(cache: Union[Dict]) -> None:
	if cache=={} or not cache:
		abort(401)

#returns true if plain matches cache hash
def correct_pwd(self, plain: str) -> bool:
	if type(plain) is str:
		plain=plain.encode()

	return self.cache["sha512"]==sha512(plain).hexdigest()

#updates hash to new if old is correct, else return false
def update_pwd(self, plain: str, new: Stringish) -> bool:
	if correct_pwd(self, plain):
		if type(new) is str:
			new=new.encode()

		self.cache["sha512"]=sha512(new).hexdigest()
		return True

	return False