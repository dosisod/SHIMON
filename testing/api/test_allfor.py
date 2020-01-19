from SHIMON.api.allfor import allfor

from testing.base import BaseTest

class TestAllfor(BaseTest):
	@BaseTest.request_context
	@BaseTest.unlocked
	def test_valid_id_always_returns_http_200(self):
		user=self.shimon.cache["friends"][0]
		assert self.allfor(user["id"])[1]==200

	@BaseTest.request_context
	@BaseTest.unlocked
	def test_invalid_id_always_returns_http_400(self):
		assert self.allfor("not a user id")[1]==400

	@BaseTest.request_context
	@BaseTest.unlocked
	def test_always_will_return_data(self):
		user=self.shimon.cache["friends"][0]

		raw=self.allfor(user["id"])[0].json
		assert raw or raw==[]

	def allfor(self, id: str):
		return allfor(self.shimon, id, False)
