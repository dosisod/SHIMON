from SHIMON import api

from testing.base import BaseTest

class TestMsgPolict(BaseTest):
	@classmethod
	@BaseTest.request_context
	def setup_class(self):
		api.unlock.unlock(self.shimon, {"unlock": self.pwd})

	@BaseTest.app_context
	def test_num_too_high_causes_http_400(self):
		assert api.msg_policy.msg_policy(self.shimon, {"msg policy": "3"})[1]==400

	@BaseTest.app_context
	def test_num_too_low_causes_http_400(self):
		assert api.msg_policy.msg_policy(self.shimon, {"msg policy": "-1"})[1]==400

	@BaseTest.app_context
	def test_non_int_string_causes_http_400(self):
		assert api.msg_policy.msg_policy(self.shimon, {"msg policy": "not an int"})[1]==400

	@BaseTest.app_context
	def test_cache_msg_policy_is_set(self):
		self.shimon.cache["msg policy"]=0
		api.msg_policy.msg_policy(self.shimon, {"msg policy": "1"})
		assert self.shimon.cache["msg policy"]==1

	@BaseTest.app_context
	def test_shimon_msg_policy_is_set(self):
		self.shimon.msg_policy=0
		api.msg_policy.msg_policy(self.shimon, {"msg policy": "1"})
		assert self.shimon.msg_policy==1
