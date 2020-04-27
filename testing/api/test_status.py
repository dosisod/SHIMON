import json

from SHIMON.api.status import ApiStatus

from testing.base import BaseTest
from testing.http import assertHttpResponse

from SHIMON.__init__ import HttpResponse

class TestStatus(BaseTest):
	@BaseTest.request_context
	def test_always_returns_http_200(self) -> None:
		assertHttpResponse(
			self.status(True),
			200
		)

	@BaseTest.request_context
	def test_unlocked_false_when_locked(self) -> None:
		assert self.shimon.cache.is_empty() != \
			self.status(True)[0].json["unlocked"]

	@BaseTest.request_context
	@BaseTest.unlocked
	def test_unlocked_true_when_unlocked(self) -> None:
		assert self.shimon.cache.is_empty() != \
			self.status(True)[0].json["unlocked"]

	@BaseTest.request_context
	@BaseTest.unlocked
	def test_msg_policy_matches_status(self) -> None:
		self.assertStatus("msg policy")

	@BaseTest.request_context
	@BaseTest.unlocked
	def test_version_matches_status(self) -> None:
		self.assertStatus("version")

	@BaseTest.request_context
	@BaseTest.unlocked
	def test_developer_matches_status(self) -> None:
		self.assertStatus("developer")

	@BaseTest.request_context
	def test_that_redirect_flag_doesnt_change_output(self) -> None:
		assert self.status(True)[0].json== \
			json.loads(self.status(False)[0].data)["msg"]

	@BaseTest.request_context
	def test_msg_policy_is_none_when_locked(self) -> None:
		assert self.status(True)[0].json["msg policy"] is None

	def status(self, redirect: bool) -> HttpResponse:
		return ApiStatus().entry(self.shimon, None, redirect)

	def assertStatus(self, key: str) -> None:
		current_status=getattr(
			self.shimon,
			self.shimon.cache.mapper.cache_names[key] # type: ignore
		)

		assert current_status==self.shimon.cache[key]
		assert current_status==self.status(True)[0].json[key]
