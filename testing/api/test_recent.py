from SHIMON.api.recent import ApiRecent

from testing.base import BaseTest
from testing.http import assertHttpResponse

from SHIMON.__init__ import HttpResponse

class TestRecent(BaseTest):
	@BaseTest.request_context
	@BaseTest.unlocked
	def test_always_returns_http_200(self) -> None:
		assertHttpResponse(
			self.recent(),
			200
		)

	@BaseTest.request_context
	@BaseTest.unlocked
	def test_always_returns_data(self) -> None:
		assert self.recent()[0].json

	def recent(self) -> HttpResponse:
		return ApiRecent().entry(self.shimon, None, False)
