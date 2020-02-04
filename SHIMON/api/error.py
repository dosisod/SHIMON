from ..renderer import jsonify

from typing import Union
from ..__init__ import Complex, HttpResponse

Boolish=Union[bool, str]

def error(code: int, data: Complex, redirect: Boolish, rethrow: bool=False) -> HttpResponse:
	if type(redirect) is str:
		#convert JS true to python True
		redirect=(redirect=="true")

	if redirect:
		if isinstance(data, (dict, list)):
			return jsonify(data), code

		else:
			return data, code

	else:
		#force user to make the same call with redirect on
		if rethrow:
			return jsonify({"rethrow": ""}), code

		if not isinstance(data, (dict, list, str)):
			data=""

		return jsonify({
			"code": code,
			"msg": data
		}), code

def error_200(msg: Complex="OK", redirect: Boolish=False) -> HttpResponse:
	return error(200, msg, redirect, rethrow=False)

def error_202(msg: Complex="Lock or save to apply changes", redirect: Boolish=False) -> HttpResponse:
	return error(202, msg, redirect, rethrow=False)

def error_400(msg: Complex="Invalid Request", redirect: Boolish=False) -> HttpResponse:
	return error(400, msg, redirect, rethrow=False)

def error_401(msg: Complex="Invalid Password", redirect: Boolish=False) -> HttpResponse:
	return error(401, msg, redirect, rethrow=False)