from flask import render_template
from flask.json import jsonify

def api_error(code, ret, redirect, rethrow):
	if type(redirect) is str:
		redirect=(redirect=="true") #convert JS true to python True

	if redirect:
		return jsonify(ret)

	else:
		if rethrow: #force user to make the same call with redirect on
			return jsonify({"rethrow":""})

		else: #dont rethrow this error, let the user handle the error
			if type(ret) is not dict and type(ret) is not list and type(ret) is not str:
				ret="" #if ret is a string or json data, return blank

			return jsonify({
				"code": code,
				"msg": ret
			})