from SHIMON.api.lock import lock

from testing.base import BaseTest

class TestLock(BaseTest):
	@BaseTest.request_context
	@BaseTest.unlocked
	def test_cache_cleared_after_lock(self):
		self.lock(self.pwd, True)

		assert self.shimon.cache==self.shimon.empty_cache

	@BaseTest.request_context
	@BaseTest.unlocked
	def test_invalid_pwd_returns_http_401(self):
		assert self.lock("not the password", True)[1]==401

	@BaseTest.request_context
	@BaseTest.unlocked
	def test_not_redirecting_returns_http_400(self):
		assert self.lock(self.pwd, False)[1]==400

	def lock(self, pwd: str, redirect: bool):
		return lock(
			self.shimon,
			pwd,
			redirect
		)
