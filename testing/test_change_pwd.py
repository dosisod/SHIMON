from testing.base import BaseTest

from SHIMON.api.change_pwd import change_pwd

class TestChangePwd(BaseTest):
	@BaseTest.request_context
	def test_invalid_data_returns_http_400(self):
		assert change_pwd(self.shimon, {"change pwd": "invalid data"})[1]==400

	@BaseTest.request_context
	def test_missing_oldpwd_param_returns_http_400(self):
		assert change_pwd(self.shimon, {"change pwd": {"new": "321"}})[1]==400

	@BaseTest.request_context
	def test_missing_newpwd_param_returns_http_400(self):
		assert change_pwd(self.shimon, {"change pwd": {"old": "123"}})[1]==400

	@BaseTest.request_context
	@BaseTest.unlocked
	def test_invalid_pwd_returns_http_401(self):
		assert change_pwd(self.shimon, {"change pwd": {"old": "not the password", "new": "321"}, "redirect": "true"})[1]==401

	@BaseTest.request_context
	@BaseTest.unlocked
	def test_correct_pwd_returns_http_202(self):
		assert change_pwd(self.shimon, {"change pwd": {"old": "123", "new": "123"}})[1]==202

	@BaseTest.request_context
	@BaseTest.unlocked
	def test_correct_pwd_updates_cache_sha512(self):
		assert self.shimon.security.correct_pwd("new_pwd")==False
		change_pwd(self.shimon, {"change pwd": {"old": "123", "new": "new_pwd"}})
		assert self.shimon.security.correct_pwd("new_pwd")==True
