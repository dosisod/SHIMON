from flask import make_response as _make_response
from flask import render_template, Response
from flask.json import jsonify as _jsonify

from typing import Any, cast
from .__init__ import Page

def render(self, filepath: str, **kwargs) -> Page:
	kwargs["developer"]=self.developer
	kwargs["theme"]=self.theme
	kwargs["fresh_js"]=self.fresh_js
	kwargs["fresh_css"]=self.fresh_css

	return render_template(filepath, **kwargs)

def make_response(*args: Any) -> Response:
	return cast(
		Response,
		_make_response(*args)
	)

#duplicate function of jsonify that returns Response type and not Any
def jsonify(*args: Any, **kwargs: Any) -> Response:
	return cast(
		Response,
		_jsonify(*args)
	)
