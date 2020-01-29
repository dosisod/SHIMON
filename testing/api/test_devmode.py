from SHIMON.api.devmode import devmode

from testing.base import BaseTest
from testing.util import assertHttpResponse

class TestDevmode(BaseTest):
	@BaseTest.request_context
	def test_true_enables_devmode(self):
		self.shimon.cache_mapper["developer"]=False

		self.devmode("true")

		assert self.shimon.cache["developer"]==True
		assert self.shimon.developer==True

	@BaseTest.request_context
	def test_non_true_string_disables_devmode(self):
		self.shimon.cache_mapper["developer"]=False

		self.devmode("false")

		assert self.shimon.cache["developer"]==False
		assert self.shimon.developer==False	

	@BaseTest.request_context
	def test_always_returns_http_200(self):
		assertHttpResponse(
			self.devmode("true"),
			200
		)

	def devmode(self, enable: bool):
		return devmode(
			self.shimon,
			"true" if enable=="true" else "false",
			False
		)
