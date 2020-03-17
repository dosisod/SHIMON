from SHIMON.api.unlock import unlock
from SHIMON.renderer import jsonify
from SHIMON.api.theme import theme

from testing.base import BaseTest
from testing.util import assertHttpResponse

from SHIMON.__init__ import HttpResponse

class TestTheme(BaseTest):
	@BaseTest.request_context
	def test_valid_theme_returns_http_202(self):
		self.reset()
		assertHttpResponse(
			self.theme("auto"),
			202
		)

	@BaseTest.request_context
	def test_valid_theme_sets_new_theme(self):
		self.reset()
		self.theme("solarized dark")

		assert self.shimon.cache["theme"]=="solarized dark"
		assert self.shimon.theme=="solarized dark"

	@BaseTest.request_context
	def test_invalid_theme_returns_http_400(self):
		assertHttpResponse(
			self.theme("not a theme"),
			400
		)

	@BaseTest.request_context
	def test_invalid_theme_keeps_last_theme(self):
		self.reset()
		self.theme("not a theme")

		assert self.shimon.theme=="auto"
		assert self.shimon.cache["theme"]=="auto"

	@BaseTest.request_context
	def test_file_traversal_returns_http_400(self):
		self.reset()

		assertHttpResponse(
			self.theme("../auto"),
			400
		)

	def reset(self) -> None:
		self.shimon.cache.mapper["theme"]="auto"

	def theme(self, obj) -> HttpResponse:
		return theme(self.shimon, obj, True)