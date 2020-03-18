from testing.base import BaseTest

class TestCacheMapper(BaseTest):
	@BaseTest.request_context
	def test_setting_name_not_in_names_list_does_nothing(self) -> None:
		assert "invalid name" not in self.shimon.cache.mapper.cache_names

		self.shimon.cache.mapper["invalid name"]="testing 123"

		assert "invalid name" not in self.shimon.cache.mapper.cache_names

	@BaseTest.request_context
	def test_setting_valid_name_updates_vars(self) -> None:
		self.shimon.msg_policy=0
		self.shimon.cache["msg policy"]=0

		self.shimon.cache.mapper["msg policy"]=1

		assert self.shimon.msg_policy==1
		assert self.shimon.cache["msg policy"]==1

		self.shimon.msg_policy=0
		self.shimon.cache["msg policy"]=0

	@BaseTest.request_context
	def test_update_will_update_elements_in_list(self) -> None:
		self.shimon.msg_policy=0
		self.shimon.cache["msg policy"]=1

		self.shimon.cache.mapper.update([
			"msg policy",
			"msg policy"
		])

		assert self.shimon.msg_policy==1
		assert self.shimon.cache["msg policy"]==1

		self.shimon.msg_policy=0
		self.shimon.cache["msg policy"]=0