from SHIMON.api.devmode import devmode

from testing.base import BaseTest

class TestDevmode(BaseTest):
	@BaseTest.request_context
	@BaseTest.unlocked
	def test_true_enables_devmode(self):
		self.shimon.cache_mapper["developer"]=False

		devmode(self.shimon, {"devmode": "true"})

		assert self.shimon.cache["developer"]==True
		assert self.shimon.developer==True

	@BaseTest.request_context
	@BaseTest.unlocked
	def test_non_true_string_disables_devmode(self):
		self.shimon.cache_mapper["developer"]=False

		devmode(self.shimon, {"devmode": "false"})

		assert self.shimon.cache["developer"]==False
		assert self.shimon.developer==False	

	@BaseTest.request_context
	@BaseTest.unlocked
	def test_always_returns_http_200(self):
		assert devmode(self.shimon, {"devmode": "true"})[1]==200
