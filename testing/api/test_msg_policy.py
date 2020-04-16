from SHIMON.api.msg_policy import ApiMsgPolicy
from SHIMON.api.unlock import ApiUnlock

from testing.base import BaseTest
from testing.http import assertHttpResponse

from SHIMON.__init__ import HttpResponse

class TestMsgPolict(BaseTest):
	@classmethod
	@BaseTest.request_context
	def setup_class(self) -> None:
		ApiUnlock().entry(self.shimon, self.pwd, False)

	@BaseTest.app_context
	def test_num_too_high_causes_http_400(self) -> None:
		assertHttpResponse(
			self.msg_policy("3"),
			400
		)

	@BaseTest.app_context
	def test_num_too_low_causes_http_400(self) -> None:
		assertHttpResponse(
			self.msg_policy("-1"),
			400
		)

	@BaseTest.app_context
	def test_non_int_string_causes_http_400(self) -> None:
		assertHttpResponse(
			self.msg_policy("not an int"),
			400
		)

	@BaseTest.app_context
	def test_cache_msg_policy_is_set(self) -> None:
		self.shimon.cache["msg policy"]=0
		self.msg_policy("1")
		assert self.shimon.cache["msg policy"]==1

	@BaseTest.app_context
	def test_shimon_msg_policy_is_set(self) -> None:
		self.shimon.cache.mapper["msg policy"]=1
		self.msg_policy("1")

		assert self.shimon.msg_policy==1
		assert self.shimon.cache["msg policy"]==1

	def msg_policy(self, policy: str) -> HttpResponse:
		return ApiMsgPolicy().entry(self.shimon, policy, False)
