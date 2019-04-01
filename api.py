from flask import render_template
from flask.json import jsonify

def api_handle(data): #handles all api requests
	return jsonify(data)