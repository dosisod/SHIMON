from flask import render_template
from flask.json import jsonify

from storage import unlock

def api_handle(data): #handles all api requests
	return jsonify(data)