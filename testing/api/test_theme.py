from SHIMON.api.unlock import ApiUnlock
from SHIMON.api.theme import ApiTheme
from SHIMON.renderer import jsonify

from testing.base import BaseTest
from testing.http import assertHttpResponse

from SHIMON.__init__ import HttpResponse

class TestTheme(BaseTest):
	@BaseTest.request_context
	def test_valid_theme_returns_http_202(self) -> None:
		self.reset()
		assertHttpResponse(
			self.theme("auto"),
			202
		)

	@BaseTest.request_context
	def test_valid_theme_sets_new_theme(self) -> None:
		self.reset()
		self.theme("solarized dark")

		assert self.shimon.cache["theme"]=="solarized dark"
		assert self.shimon.theme=="solarized dark"

	@BaseTest.request_context
	def test_invalid_theme_returns_http_400(self) -> None:
		assertHttpResponse(
			self.theme("not a theme"),
			400
		)

	@BaseTest.request_context
	def test_invalid_theme_keeps_last_theme(self) -> None:
		self.reset()
		self.theme("not a theme")

		assert self.shimon.theme=="auto"
		assert self.shimon.cache["theme"]=="auto"

	@BaseTest.request_context
	def test_file_traversal_returns_http_400(self) -> None:
		self.reset()

		assertHttpResponse(
			self.theme("../auto"),
			400
		)

	def reset(self) -> None:
		self.shimon.cache.mapper["theme"]="auto"

	def theme(self, name: str) -> HttpResponse:
		return ApiTheme().entry(self.shimon, name, True)