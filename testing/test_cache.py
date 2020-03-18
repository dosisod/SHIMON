import json

from testing.base import BaseTest

class TestCache(BaseTest):
	@BaseTest.request_context
	@BaseTest.unlocked
	def test_wipe_clears_cache(self) -> None:
		self.shimon.cache["temp"]="temp data"

		assert not self.shimon.cache.is_empty()

		self.shimon.cache.wipe()

		assert self.shimon.cache.is_empty()

	@BaseTest.request_context
	@BaseTest.unlocked
	def test_exporting_cache_returns_data(self) -> None:
		self.shimon.cache["temp"]="temp data"

		assert self.shimon.cache.export()["temp"]

	@BaseTest.request_context
	@BaseTest.unlocked
	def test_loading_cache_sets_data(self) -> None:
		#need to make copy so we can lock cache after test
		old_cache=self.shimon.cache._cache

		self.shimon.cache.load(
			json.loads('{"hello":"world"}')
		)

		assert self.shimon.cache._cache["hello"]=="world"

		self.shimon.cache._cache=old_cache