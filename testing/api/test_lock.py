from SHIMON.api.lock import lock

from testing.base import BaseTest
from testing.util import assertHttpResponse

class TestLock(BaseTest):
	@BaseTest.request_context
	@BaseTest.unlocked
	def test_cache_cleared_after_lock(self):
		self.lock(self.pwd, True)

		assert self.shimon.cache.is_empty()

	@BaseTest.request_context
	@BaseTest.unlocked
	def test_invalid_pwd_returns_http_401(self):
		assertHttpResponse(
			self.lock("not the password", True),
			401
		)

	@BaseTest.request_context
	@BaseTest.unlocked
	def test_not_redirecting_returns_http_400(self):
		assertHttpResponse(
			self.lock(self.pwd, False),
			400
		)

	def lock(self, pwd: str, redirect: bool):
		return lock(
			self.shimon,
			pwd,
			redirect
		)
