import json

from SHIMON.api.handle import handler

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
