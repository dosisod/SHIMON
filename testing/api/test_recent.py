from SHIMON.api.recent import recent

from testing.base import BaseTest
from testing.util import assertHttpResponse

class TestRecent(BaseTest):
	@BaseTest.request_context
	@BaseTest.unlocked
	def test_always_returns_http_200(self):
		assertHttpResponse(
			self.recent(),
			200
		)

	@BaseTest.request_context
	@BaseTest.unlocked
	def test_always_returns_data(self):
		assert self.recent()[0].json

	def recent(self):
		return recent(self.shimon, None, False)
