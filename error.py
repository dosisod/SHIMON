from flask.json import jsonify

from typing import Union, Dict, List, Any

#Complex can be many things, including dict, list, str
#technically Complex could be anything, but preferably it is one of the above ones
Complex=Union[Dict, List, str, Any]

def api_error(code: Union[int, str], data: Complex, redirect: bool, rethrow: bool) -> Complex:
	if type(redirect) is str:
		redirect=(redirect=="true") #convert JS true to python True

	if redirect:
		#ret is some json object then jsonify first
		if type(data) is dict or type(data) is list:
			return jsonify(data)

		#ret is probably a render_template, just return (render returns a string)
		else:
			return data

	else:
		if rethrow: #force user to make the same call with redirect on
			return jsonify({"rethrow":""})

		else: #dont rethrow this error, let the user handle the error
			if type(data) is not dict and type(data) is not list and type(data) is not str:
				data="" #if ret is a string or json data, return blank

			return jsonify({
				"code": code,
				"msg": data
			})