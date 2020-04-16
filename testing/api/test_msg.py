from SHIMON.api.msg import history_id

from testing.base import BaseTest

class TestHistoryId(BaseTest):
	@BaseTest.request_context
	@BaseTest.unlocked
	def test_invalid_id_returns_negative_1(self) -> None:
		assert history_id(
			self.shimon,
			"not a valid id"
		) == -1

	@BaseTest.request_context
	@BaseTest.unlocked
	def test_valid_id_returns_non_negative(self) -> None:
		first_id=self.shimon.cache["history"][0]["id"]

		assert history_id(
			self.shimon,
			first_id
		) >= 0