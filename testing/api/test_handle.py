import json

from SHIMON.api.handle import handler, try_json_convert

from testing.base import BaseTest
from testing.util import assertHttpResponse

class TestHandler(BaseTest):
	@BaseTest.request_context
	@BaseTest.allow_local
	@BaseTest.unlocked
	def test_unlocking_while_unlocked_returns_http_301(self):
		@BaseTest.use_cookie("session", self.shimon.session.session)
		def run(self):
			handler(self.shimon, {"unlock": self.pwd})

			assertHttpResponse(
				handler(
					self.shimon, {
						"unlock": self.pwd
					}),
				301
			)

		run(self)

	@BaseTest.request_context
	@BaseTest.allow_local
	@BaseTest.unlocked
	def test_invalid_call_returns_http_400(self):
		@BaseTest.use_cookie("session", self.shimon.session.session)
		def run(self):
			assertHttpResponse(
				handler(self.shimon, {
					"not a call": ""
				}),
				400
			)

		run(self)

	@BaseTest.request_context
	@BaseTest.allow_local
	def test_invalid_session_returns_http_401(self):
		assertHttpResponse(
			handler(self.shimon, {"ping": ""}),
			401
		)

	def test_json_converter_returns_non_json_as_str(self):
		output=try_json_convert("testing 123")

		assert output=="testing 123"
		assert type(output)==str

	def test_json_converter_returns_malformed_json_as_str(self):
		def test_malformed(string):
			output=try_json_convert(string)

			assert output==string
			assert type(output)==str

		test_malformed("[bad json")
		test_malformed("{bad json")

	def test_json_converter_returns_proper_json_returned_as_obj(self):
		def test_proper(string):
			output=try_json_convert(string)

			assert output==json.loads(string)
			assert type(output)==type(json.loads(string))

		test_proper('{"testing":123}')
		test_proper("[1,2,3,4]")
