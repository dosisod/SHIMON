from SHIMON.api.new_key import new_key

from testing.base import BaseTest

class TestNewKey(BaseTest):
	@BaseTest.request_context
	@BaseTest.unlocked
	def test_invalid_password_returns_http_401(self):
		assert self.new_key("not the password")[1]==401

	@BaseTest.request_context
	@BaseTest.unlocked
	@BaseTest.allow_local
	def test_valid_pwd_returns_http_200(self):
		assert self.new_key(self.pwd)[1]==200

	@BaseTest.request_context
	@BaseTest.unlocked
	@BaseTest.allow_local
	def test_key_gets_changed(self):
		old_key=self.shimon.cache["key"]
		self.new_key(self.pwd)

		assert self.shimon.cache["key"]!=old_key

	def new_key(self, pwd: str):
		return new_key(self.shimon, pwd, False)
