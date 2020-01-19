from SHIMON.api.friends import friends

from testing.base import BaseTest

class TestFriends(BaseTest):
	@BaseTest.request_context
	@BaseTest.unlocked
	def test_always_returns_http_200(self):
		assert self.friends()[1]==200

	@BaseTest.request_context
	@BaseTest.unlocked
	def test_always_will_return_data(self):
		assert self.friends()[0].json

	def friends(self):
		return friends(self.shimon, None, False)
