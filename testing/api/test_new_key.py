from SHIMON.api.new_key import new_key

from testing.base import BaseTest
from testing.util import assertHttpResponse

class TestNewKey(BaseTest):
	@BaseTest.request_context
	@BaseTest.unlocked
	@BaseTest.allow_local
	def test_invalid_password_returns_http_401(self):
		assertHttpResponse(
			self.new_key("not the password"),
			401
		)

	@BaseTest.request_context
	@BaseTest.unlocked
	@BaseTest.allow_local
	def test_invalid_pwd_returns_html(self):
		resp=self.new_key("not the password")

		assert resp[0].startswith("<!DOCTYPE html>")

	@BaseTest.request_context
	@BaseTest.unlocked
	@BaseTest.allow_local
	def test_valid_pwd_returns_http_200(self):
		@BaseTest.use_cookie("session", self.shimon.session.session)
		def run(self):
			assertHttpResponse(
				self.new_key(self.pwd),
				200
			)

		run(self)

	@BaseTest.request_context
	@BaseTest.unlocked
	@BaseTest.allow_local
	def test_key_gets_changed(self):
		old_key=self.shimon.cache["key"]
		self.new_key(self.pwd)

		assert self.shimon.cache["key"]!=old_key

	def new_key(self, pwd: str):
		return new_key(self.shimon, pwd, False)
