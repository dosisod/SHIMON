from SHIMON.api.lock import lock

from testing.base import BaseTest

class TestLock(BaseTest):
	@BaseTest.request_context
	@BaseTest.unlocked
	def test_variables_cleared_after_lock(self):
		lock(self.shimon, {"lock": self.pwd, "redirect": "true"})

		assert self.shimon.cache==None
		assert self.shimon.login_limiter.attempts==0
		assert self.shimon.login_limiter.cooldown_start==0

	@BaseTest.request_context
	@BaseTest.unlocked
	def test_invalid_pwd_returns_http_401(self):
		assert lock(self.shimon, {"lock": "not the password", "redirect": "true"})[1]==401

	@BaseTest.request_context
	@BaseTest.unlocked
	def test_not_redirecting_returns_http_400(self):
		assert lock(self.shimon, {"lock": self.pwd, "redirect": "false"})[1]==400
