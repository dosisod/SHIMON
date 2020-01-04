from SHIMON.api.msg_policy import msg_policy
from SHIMON.api.unlock import unlock

from testing.base import BaseTest

class TestMsgPolict(BaseTest):
	@classmethod
	@BaseTest.request_context
	def setup_class(self):
		unlock(self.shimon, {"unlock": self.pwd})

	@BaseTest.app_context
	def test_num_too_high_causes_http_400(self):
		assert self.msg_policy_wrapper("3")[1]==400

	@BaseTest.app_context
	def test_num_too_low_causes_http_400(self):
		assert self.msg_policy_wrapper("-1")[1]==400

	@BaseTest.app_context
	def test_non_int_string_causes_http_400(self):
		assert self.msg_policy_wrapper("not an int")[1]==400

	@BaseTest.app_context
	def test_cache_msg_policy_is_set(self):
		self.shimon.cache["msg policy"]=0
		self.msg_policy_wrapper("1")
		assert self.shimon.cache["msg policy"]==1

	@BaseTest.app_context
	def test_shimon_msg_policy_is_set(self):
		self.shimon.cache_mapper["msg policy"]=1
		self.msg_policy_wrapper("1")

		assert self.shimon.msg_policy==1
		assert self.shimon.cache["msg policy"]==1

	def msg_policy_wrapper(self, policy: str):
		return msg_policy(self.shimon, {"msg policy": policy})
