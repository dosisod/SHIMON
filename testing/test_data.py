from SHIMON.api._data import _data

from testing.base import BaseTest

class TestData(BaseTest):
	@classmethod
	@BaseTest.request_context
	@BaseTest.unlocked
	def setup_class(self):
		self.user=self.shimon.cache["friends"][0]

	@BaseTest.request_context
	@BaseTest.unlocked
	def test_invalid_string_option_returns_http_400(self):
		assert _data(self.shimon, {"data": "invalid option"})[1]==400

	@BaseTest.request_context
	@BaseTest.unlocked
	def test_invalid_option_in_dict_returns_http_400(self):
		assert _data(self.shimon, {"data": {"not valid": "either"}})[1]==400

	@BaseTest.request_context
	@BaseTest.unlocked
	def test_allfor_with_valid_id_always_returns_http_200(self):
		assert _data(self.shimon, {"data": {"allfor": self.user["id"]}})[1]==200

	@BaseTest.request_context
	@BaseTest.unlocked
	def test_allfor_with_invalid_id_always_returns_http_400(self):
		assert _data(self.shimon, {"data": {"allfor": "not a user id"}})[1]==400

	@BaseTest.request_context
	@BaseTest.unlocked
	def test_api_friends_always_returns_http_200(self):
		assert _data(self.shimon, {"data": "friends"})[1]==200

	@BaseTest.request_context
	@BaseTest.unlocked
	def test_api_recent_always_returns_http_200(self):
		assert _data(self.shimon, {"data": "recent"})[1]==200