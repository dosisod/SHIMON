from SHIMON.api.recent import recent

from testing.base import BaseTest

class TestRecent(BaseTest):
	@BaseTest.request_context
	@BaseTest.unlocked
	def test_invalid_string_option_returns_http_400(self):
		assert recent(self.shimon, {"invalid option": ""})[1]==400

	@BaseTest.request_context
	@BaseTest.unlocked
	def test_always_returns_http_200(self):
		assert recent(self.shimon, {"recent": ""})[1]==200

	@BaseTest.request_context
	@BaseTest.unlocked
	def test_always_returns_data(self):
		assert recent(self.shimon, {"recent": ""})[0].json
