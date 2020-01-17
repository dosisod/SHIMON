from SHIMON.api.new_key import new_key

from testing.base import BaseTest

class TestNewKey(BaseTest):
	@BaseTest.request_context
	def test_missing_new_key_param_returns_http_400(self):
		assert new_key(self.shimon, {"not new key": ""})[1]==400

	@BaseTest.request_context
	@BaseTest.unlocked
	def test_invalid_password_returns_http_401(self):
		assert new_key(self.shimon, {"new key": "not the password"})[1]==401

	@BaseTest.request_context
	@BaseTest.unlocked
	@BaseTest.allow_local
	def test_valid_pwd_returns_http_200(self):
		assert new_key(self.shimon, {"new key": self.pwd})[1]==200

	@BaseTest.request_context
	@BaseTest.unlocked
	@BaseTest.allow_local
	def test_key_gets_changed(self):
		old_key=self.shimon.cache["key"]
		new_key(self.shimon, {"new key": self.pwd})

		assert self.shimon.cache["key"]!=old_key
