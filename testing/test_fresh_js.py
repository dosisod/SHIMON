from SHIMON.api.fresh_js import fresh_js

from testing.base import BaseTest

class TestFreshCSS(BaseTest):
	@BaseTest.request_context
	@BaseTest.unlocked
	def test_always_returns_http_200(self):
		assert fresh_js(self.shimon, {"fresh js": "true"})[1]==200

	@BaseTest.request_context
	@BaseTest.unlocked
	def test_enabled_when_set_to_true(self):
		self.shimon.cache_mapper["fresh js"]=False

		fresh_js(self.shimon, {"fresh js": "true"})

		assert self.shimon.fresh_js==True
		assert self.shimon.cache["fresh js"]==True

	@BaseTest.request_context
	@BaseTest.unlocked
	def test_disabled_when_set_to_non_true(self):
		self.shimon.cache_mapper["fresh js"]=False

		fresh_js(self.shimon, {"fresh js": "false"})

		assert self.shimon.fresh_js==False
		assert self.shimon.cache["fresh js"]==False
