from pathlib import Path
import shutil
import os

from SHIMON.api.fresh_css import fresh_css

from testing.base import BaseTest
from testing.util import assertHttpResponse

class TestFreshCSS(BaseTest):
	css_file="SHIMON/static/css/font.css"

	@BaseTest.request_context
	def test_always_returns_http_200(self):
		assertHttpResponse(
			self.fresh_css(True),
			200
		)

	@BaseTest.request_context
	def test_not_having_fresh_css_ignores_value(self):
		self.shimon.cache.mapper["fresh css"]=False

		if os.path.isfile(self.css_file):
			shutil.move(self.css_file, self.css_file + ".bak")

			self.fresh_css(True)

			shutil.move(self.css_file + ".bak", self.css_file)

		else:
			self.fresh_css(True)

		assert self.shimon.fresh_css==False
		assert self.shimon.cache["fresh css"]==False

	@BaseTest.request_context
	def test_having_fresh_css_respects_value(self):
		self.shimon.cache.mapper["fresh css"]=False

		if not os.path.isfile(self.css_file):
			Path(self.css_file).touch()

			self.fresh_css(True)

			os.remove(self.css_file)

		else:
			self.fresh_css(True)

		assert self.shimon.fresh_css==True
		assert self.shimon.cache["fresh css"]==True

	@BaseTest.request_context
	def test_disabled_when_set_to_false(self):
		self.shimon.cache.mapper["fresh css"]=False

		self.fresh_css(False)

		assert self.shimon.fresh_css==False
		assert self.shimon.cache["fresh css"]==False

	def fresh_css(self, enable: bool):
		return fresh_css(
			self.shimon,
			enable,
			False
		)
