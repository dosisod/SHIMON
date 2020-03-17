from SHIMON.api.friends import friends

from testing.base import BaseTest
from testing.util import assertHttpResponse

from SHIMON.__init__ import HttpResponse

class TestFriends(BaseTest):
	@BaseTest.request_context
	@BaseTest.unlocked
	def test_always_returns_http_200(self):
		assertHttpResponse(
			self.friends(),
			200
		)

	@BaseTest.request_context
	@BaseTest.unlocked
	def test_always_will_return_data(self):
		assert self.friends()[0].json

	def friends(self) -> HttpResponse:
		return friends(self.shimon, None, False)
