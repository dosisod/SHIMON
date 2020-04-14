from SHIMON.api.allfor import ApiAllfor

from testing.base import BaseTest
from testing.util import assertHttpResponse

from SHIMON.__init__ import HttpResponse

class TestAllfor(BaseTest):
	@BaseTest.request_context
	@BaseTest.unlocked
	def test_valid_id_always_returns_http_200(self) -> None:
		user=self.shimon.cache["friends"][0]
		assertHttpResponse(
			self.allfor(user["id"]),
			200
		)

	@BaseTest.request_context
	@BaseTest.unlocked
	def test_invalid_id_always_returns_http_400(self) -> None:
		assertHttpResponse(
			self.allfor("not a user id"),
			400
		)

	@BaseTest.request_context
	@BaseTest.unlocked
	def test_always_will_return_data(self) -> None:
		user=self.shimon.cache["friends"][0]

		raw=self.allfor(user["id"])[0].json
		assert raw or raw==[]

	def allfor(self, id: str) -> HttpResponse:
		return ApiAllfor().entry(self.shimon, id, False)
