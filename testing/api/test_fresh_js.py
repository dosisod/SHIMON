from SHIMON.api.fresh_js import fresh_js

from testing.base import BaseTest

class TestFreshCSS(BaseTest):
	@BaseTest.request_context
	def test_always_returns_http_200(self):
		assert self.fresh_js("true")[1]==200

	@BaseTest.request_context
	def test_enabled_when_set_to_true(self):
		self.shimon.cache_mapper["fresh js"]=False

		self.fresh_js("true")

		assert self.shimon.fresh_js==True
		assert self.shimon.cache["fresh js"]==True

	@BaseTest.request_context
	def test_disabled_when_set_to_non_true(self):
		self.shimon.cache_mapper["fresh js"]=False

		self.fresh_js("false")

		assert self.shimon.fresh_js==False
		assert self.shimon.cache["fresh js"]==False

	def fresh_js(self, enable: bool):
		return fresh_js(
			self.shimon,
			"true" if enable=="true" else "false",
			False
		)
