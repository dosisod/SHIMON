from flask.json import jsonify

from typing import Union, Any
from ..__init__ import Complex

Boolish=Union[bool, str]

def error(code: Union[int, str], data: Complex, redirect: Boolish, rethrow: bool=None) -> Complex:
	if type(redirect) is str:
		redirect=(redirect=="true") #convert JS true to python True

	if redirect:
		#if data is some json object then jsonify first
		if type(data) is dict or type(data) is list:
			return jsonify(data), code

		#data data was not needed to be jsonified before sending back, return it
		else:
			return data, code

	else:
		if rethrow: #force user to make the same call with redirect on
			return jsonify({"rethrow":""}), code

		else: #dont rethrow this error, let the user handle the error
			if type(data) is not dict and type(data) is not list and type(data) is not str:
				data="" #if data is not returnable (isnt json) then set data to blank

			return jsonify({
				"code": code,
				"msg": data
			}), code

#below is a bunch of error() wrappers for common calls
#data stores default message for the given error type, it can be changed

def error_200(msg: str="OK", redirect: Boolish=False) -> Complex:
	return error(200, msg, redirect, rethrow=False)

#usually used when the user needs to save/lock to fulfill request
def error_202(msg: str="Lock or save to apply changes", redirect: Boolish=False) -> Complex:
	return error(202, msg, redirect, rethrow=False)

def error_400(msg: str="Invalid Request", redirect: Boolish=False) -> Complex:
	return error(400, msg, redirect, rethrow=False)

def error_401(msg: str="Invalid Password", redirect: Boolish=False) -> Complex:
	return error(401, msg, redirect, rethrow=False)