from SHIMON.api.fresh_css import fresh_css

from testing.base import BaseTest
from testing.util import assertHttpResponse

class TestFreshCSS(BaseTest):
	@BaseTest.request_context
	def test_always_returns_http_200(self):
		assertHttpResponse(
			self.fresh_css("true"),
			200
		)

	@BaseTest.request_context
	def test_enabled_when_set_to_true(self):
		self.shimon.cache.mapper["fresh css"]=False

		self.fresh_css("true")

		assert self.shimon.fresh_css==True
		assert self.shimon.cache["fresh css"]==True

	@BaseTest.request_context
	def test_disabled_when_set_to_non_true(self):
		self.shimon.cache.mapper["fresh css"]=False

		self.fresh_css("false")

		assert self.shimon.fresh_css==False
		assert self.shimon.cache["fresh css"]==False

	def fresh_css(self, enable: bool):
		return fresh_css(
			self.shimon,
			"true" if enable=="true" else "false",
			False
		)
