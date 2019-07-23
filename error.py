from flask import render_template
from flask.json import jsonify

def api_error(code, ret, redirect, rethrow):
	if type(redirect) is str:
		redirect=(redirect=="true") #convert JS true to python True
	
	if redirect:
		return ret

	else:
		if rethrow: #force user to make the same call with redirect on
			return jsonify({"rethrow":""})

		else: #dont rethrow this error, let the user handle the error
			return jsonify({
				"code": code,
				"msg": ret
			})