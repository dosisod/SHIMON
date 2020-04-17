from SHIMON.api.new_key import ApiNewKey

from testing.base import BaseTest
from testing.http import assertHttpResponse

from SHIMON.__init__ import HttpResponse

class TestNewKey(BaseTest):
	@BaseTest.request_context
	@BaseTest.unlocked
	@BaseTest.allow_local
	def test_invalid_password_returns_http_401(self) -> None:
		assertHttpResponse(
			self.new_key("not the password"),
			401
		)

	@BaseTest.request_context
	@BaseTest.unlocked
	@BaseTest.allow_local
	def test_invalid_pwd_returns_html(self) -> None:
		resp=self.new_key("not the password")

		assert resp[0].data.startswith(b"<!DOCTYPE html>")

	@BaseTest.request_context
	@BaseTest.unlocked
	@BaseTest.allow_local
	def test_valid_pwd_returns_http_200(self) -> None:
		@BaseTest.use_cookie("session", self.shimon.session.session)
		def run(self: TestNewKey) -> None:
			assertHttpResponse(
				self.new_key(self.pwd),
				200
			)

		run(self)

	@BaseTest.request_context
	@BaseTest.unlocked
	@BaseTest.allow_local
	def test_key_gets_changed(self) -> None:
		old_key=self.shimon.cache["key"]
		self.new_key(self.pwd)

		assert self.shimon.cache["key"]!=old_key

	@BaseTest.request_context
	def test_non_str_input_returns_http_400(self) -> None:
		not_a_string=123

		assertHttpResponse(
			self.new_key(not_a_string), # type: ignore
			400
		)

	def new_key(self, pwd: str) -> HttpResponse:
		return ApiNewKey().entry(self.shimon, pwd, False)
