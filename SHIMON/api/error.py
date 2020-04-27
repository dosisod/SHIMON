from SHIMON.renderer import jsonify

from typing import Union, Dict, List
from SHIMON.__init__ import HttpResponse, Response

ErrorData=Union[Dict, List, str, Response]

http_codes={
	200: "OK",
	202: "Lock or save to apply changes",
	301: "Moved Permanently",
	400: "Invalid Request",
	401: "Unauthorized",
	403: "Forbidden",
	404: "Not Found",
	500: "Server Error"
}

def error(code: int, data: ErrorData, redirect: bool, rethrow: bool=False) -> HttpResponse:
	if redirect:
		return (jsonify(data) if isinstance(data, (Dict, List, str)) else data), code

	if rethrow:
		return jsonify({"rethrow": ""}), code

	return jsonify({
		"code": code,
		"msg": data if isinstance(data, (Dict, List, str)) else ""
	}), code

def error_200(msg: ErrorData=http_codes[200], redirect: bool=False) -> HttpResponse:
	return error(200, msg, redirect, rethrow=False)

def error_202(msg: ErrorData=http_codes[202], redirect: bool=False) -> HttpResponse:
	return error(202, msg, redirect, rethrow=False)

def error_400(msg: ErrorData=http_codes[400], redirect: bool=False) -> HttpResponse:
	return error(400, msg, redirect, rethrow=False)

def error_401(msg: ErrorData="Invalid Password", redirect: bool=False) -> HttpResponse:
	return error(401, msg, redirect, rethrow=False)