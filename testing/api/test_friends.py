from SHIMON.api.friends import friends

from testing.base import BaseTest

class TestFriends(BaseTest):
	@BaseTest.request_context
	@BaseTest.unlocked
	def test_always_returns_http_200(self):
		assert friends(self.shimon, {"friends": ""})[1]==200

	@BaseTest.request_context
	@BaseTest.unlocked
	def test_always_will_return_data(self):
		assert friends(self.shimon, {"friends": ""})[0].json
