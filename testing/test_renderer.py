from flask import make_response as _make_response
from flask.json import jsonify as _jsonify

from SHIMON.renderer import render, make_response, jsonify

from testing.base import BaseTest

class TestRender(BaseTest):
	@BaseTest.request_context
	@BaseTest.unlocked
	def test_all_settings_added_automatically(self):
		template=render(self.shimon, "testing/render.html")

		def assertHasKeys(html: str) -> None:
			keys=[
				"developer",
				"theme",
				"fresh_js",
				"fresh_css"
			]

			for key in keys:
				assert html.find(
					key + "=" +
					str(self.shimon.__dict__[key])
				) > -1

		assertHasKeys(template.data.decode())

	@BaseTest.request_context
	@BaseTest.unlocked
	def test_make_response_is_same_as_calling_directly(self):
		make_resp_wrapper=make_response(render(
			self.shimon,
			"testing/hello.html"
		))

		make_resp=_make_response(render(
			self.shimon,
			"testing/hello.html"
		))

		assert make_resp.data==make_resp_wrapper.data
		assert make_resp.status==make_resp_wrapper.status

	@BaseTest.request_context
	def test_jsonify_is_same_as_calling_directly(self):
		json_wrapper=jsonify({"hello": "world!"})
		json_original=_jsonify({"hello": "world!"})

		assert json_wrapper.json==json_original.json
		assert json_wrapper.status==json_original.status