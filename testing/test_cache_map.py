from SHIMON.cache_map import CacheMapper

from testing.base import BaseTest

class TestCacheMapper(BaseTest):
	@BaseTest.request_context
	@BaseTest.unlocked
	def test_setting_name_not_in_names_list_does_nothing(self):
		assert "invalid name" not in self.shimon.cache_mapper.cache_names

		self.shimon.cache_mapper["invalid name"]="testing 123"

		assert "invalid name" not in self.shimon.cache_mapper.cache_names

	@BaseTest.request_context
	@BaseTest.unlocked
	def test_setting_valid_name_updates_vars(self):
		self.shimon.msg_policy=0
		self.shimon.cache["msg policy"]=0

		self.shimon.cache_mapper["msg policy"]=1

		assert self.shimon.msg_policy==1
		assert self.shimon.cache["msg policy"]==1

		self.shimon.msg_policy=0
		self.shimon.cache["msg policy"]=0

	@BaseTest.request_context
	@BaseTest.unlocked
	def test_update_will_update_elements_in_list(self):
		self.shimon.msg_policy=0
		self.shimon.cache["msg policy"]=1

		self.shimon.cache_mapper.update([
			"msg policy",
			"msg policy"
		])

		assert self.shimon.msg_policy==1
		assert self.shimon.cache["msg policy"]==1

		self.shimon.msg_policy=0
		self.shimon.cache["msg policy"]=0