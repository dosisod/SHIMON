from pathlib import Path
import shutil
import os

from testing.base import BaseTest
from testing.util import assertHttpResponse

from SHIMON.__init__ import HttpResponse

class FreshToggle(BaseTest):
	path=""
	name=""

	def func(self, enable: bool) -> HttpResponse:
		pass

	@BaseTest.request_context
	def test_always_returns_http_200(self) -> None:
		assertHttpResponse(
			self.func(True),
			200
		)

	@BaseTest.request_context
	def test_not_having_fresh_file_ignores_value(self) -> None:
		self.shimon.cache.mapper[self.name]=False

		if os.path.isfile(self.path):
			shutil.move(self.path, self.path + ".bak")

			self.func(True)

			shutil.move(self.path + ".bak", self.path)

		else:
			self.func(True)

		self.assertValue(False)

	@BaseTest.request_context
	def test_having_fresh_file_respects_value(self) -> None:
		self.shimon.cache.mapper[self.name]=False

		if not os.path.isfile(self.path):
			Path(self.path).touch()

			self.func(True)

			os.remove(self.path)

		else:
			self.func(True)

		self.assertValue(True)

	@BaseTest.request_context
	def test_disabled_when_set_to_false(self) -> None:
		self.shimon.cache.mapper[self.name]=False

		self.func(False)

		self.assertValue(False)

	def assertValue(self, value: bool) -> None:
		assert self.shimon.__dict__[
			self.shimon.cache.mapper.cache_names[self.name] # type: ignore
		]==value

		assert self.shimon.cache[self.name]==value
