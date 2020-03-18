import json

from SHIMON.api.entry import api_entry

from testing.base import BaseTest
from testing.util import assertHttpResponse

class TestEntry(BaseTest):
	@BaseTest.request_context
	@BaseTest.allow_local
	@BaseTest.unlocked
	def test_unlocking_while_unlocked_returns_http_301(self) -> None:
		@BaseTest.use_cookie("session", self.shimon.session.session)
		def run(self: TestEntry) -> None:
			api_entry(self.shimon, {"unlock": self.pwd})

			assertHttpResponse(
				api_entry(
					self.shimon, {
						"unlock": self.pwd
					}),
				301
			)

		run(self)

	@BaseTest.request_context
	@BaseTest.allow_local
	@BaseTest.unlocked
	def test_invalid_call_returns_http_400(self) -> None:
		@BaseTest.use_cookie("session", self.shimon.session.session)
		def run(self: TestEntry) -> None:
			assertHttpResponse(
				api_entry(self.shimon, {
					"not a call": ""
				}),
				400
			)

		run(self)

	@BaseTest.request_context
	@BaseTest.allow_local
	def test_invalid_session_returns_http_401(self) -> None:
		assertHttpResponse(
			api_entry(self.shimon, {"ping": ""}),
			401
		)
