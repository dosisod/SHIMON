from flask.json import jsonify

def api_error(code, ret, redirect, rethrow):
	if type(redirect) is str:
		redirect=(redirect=="true") #convert JS true to python True

	if redirect:
		#ret is some json object or string, jsonify first
		if type(ret) is dict or type(ret) is list or type(ret) is str:
			return jsonify(ret)

		#ret is probably a render_template, just return
		else:
			return ret

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