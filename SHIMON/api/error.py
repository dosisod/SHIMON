from SHIMON.renderer import jsonify

from typing import Union
from SHIMON.__init__ import Complex, HttpResponse

def error(code: int, data: Complex, redirect: bool, rethrow: bool=False) -> HttpResponse:
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

def error_200(msg: Complex="OK", redirect: bool=False) -> HttpResponse:
	return error(200, msg, redirect, rethrow=False)

def error_202(msg: Complex="Lock or save to apply changes", redirect: bool=False) -> HttpResponse:
	return error(202, msg, redirect, rethrow=False)

def error_400(msg: Complex="Invalid Request", redirect: bool=False) -> HttpResponse:
	return error(400, msg, redirect, rethrow=False)

def error_401(msg: Complex="Invalid Password", redirect: bool=False) -> HttpResponse:
	return error(401, msg, redirect, rethrow=False)