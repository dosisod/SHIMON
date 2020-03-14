from SHIMON.renderer import jsonify

from typing import Union, Dict, List
from SHIMON.__init__ import HttpResponse, Page

ErrorData=Union[Dict, List, str, Page]

def error(code: int, data: ErrorData, redirect: bool, rethrow: bool=False) -> HttpResponse:
	if redirect:
		if isinstance(data, (Dict, List)):
			return jsonify(data), code

		else:
			return data, code

	else:
		#force user to make the same call with redirect on
		if rethrow:
			return jsonify({"rethrow": ""}), code

		if not isinstance(data, (Dict, List, str)):
			data=""

		return jsonify({
			"code": code,
			"msg": data
		}), code

def error_200(msg: ErrorData="OK", redirect: bool=False) -> HttpResponse:
	return error(200, msg, redirect, rethrow=False)

def error_202(msg: ErrorData="Lock or save to apply changes", redirect: bool=False) -> HttpResponse:
	return error(202, msg, redirect, rethrow=False)

def error_400(msg: ErrorData="Invalid Request", redirect: bool=False) -> HttpResponse:
	return error(400, msg, redirect, rethrow=False)

def error_401(msg: ErrorData="Invalid Password", redirect: bool=False) -> HttpResponse:
	return error(401, msg, redirect, rethrow=False)