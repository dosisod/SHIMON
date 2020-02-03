import json

from SHIMON.api.status import status

from testing.base import BaseTest
from testing.util import assertHttpResponse

class TestStatus(BaseTest):
	@BaseTest.request_context
	def test_always_returns_http_200(self):
		assertHttpResponse(
			self.status("true"),
			200
		)

	@BaseTest.request_context
	def test_unlocked_false_when_locked(self):
		assert self.shimon.cache.is_empty() != \
			self.status("true")[0].json["unlocked"]

	@BaseTest.request_context
	@BaseTest.unlocked
	def test_unlocked_true_when_unlocked(self):
		assert self.shimon.cache.is_empty() != \
			self.status("true")[0].json["unlocked"]

	@BaseTest.request_context
	@BaseTest.unlocked
	def test_msg_policy_matches_status(self):
		self.assertStatus("msg policy")

	@BaseTest.request_context
	@BaseTest.unlocked
	def test_version_matches_status(self):
		self.assertStatus("version")

	@BaseTest.request_context
	@BaseTest.unlocked
	def test_developer_matches_status(self):
		self.assertStatus("developer")

	@BaseTest.request_context
	def test_that_redirect_flag_doesnt_change_output(self):
		assert self.status("true")[0].json== \
			json.loads(self.status("false")[0].data)["msg"]

	def status(self, redirect: str):
		return status(self.shimon, None, redirect)

	def assertStatus(self, key: str) -> None:
		assert self.shimon.__dict__[
				self.shimon.cache.mapper.cache_names[key]
			] == \
			self.shimon.cache[key] == \
			self.status("true")[0].json[key]
