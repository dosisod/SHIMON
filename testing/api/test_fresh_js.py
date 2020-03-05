from pathlib import Path
import shutil
import os

from SHIMON.api.fresh_js import fresh_js

from testing.base import BaseTest
from testing.util import assertHttpResponse

class TestFreshCSS(BaseTest):
	js_file="SHIMON/static/js/api.js"

	@BaseTest.request_context
	def test_always_returns_http_200(self):
		assertHttpResponse(
			self.fresh_js(True),
			200
		)

	@BaseTest.request_context
	def test_not_having_fresh_js_ignores_value(self):
		self.shimon.cache.mapper["fresh js"]=False

		if os.path.isfile(self.js_file):
			shutil.move(self.js_file, self.js_file + ".bak")

			self.fresh_js(True)

			shutil.move(self.js_file + ".bak", self.js_file)

		else:
			self.fresh_js(True)

		assert self.shimon.fresh_js==False
		assert self.shimon.cache["fresh js"]==False

	@BaseTest.request_context
	def test_having_fresh_js_respects_value(self):
		self.shimon.cache.mapper["fresh js"]=False

		js_file="SHIMON/static/js/api.js"
		if not os.path.isfile(js_file):
			Path(js_file).touch()

			self.fresh_js(True)

			os.remove(js_file)

		else:
			self.fresh_js(True)

		assert self.shimon.fresh_js==True
		assert self.shimon.cache["fresh js"]==True

	@BaseTest.request_context
	def test_disabled_when_set_to_false(self):
		self.shimon.cache.mapper["fresh js"]=False

		self.fresh_js(False)

		assert self.shimon.fresh_js==False
		assert self.shimon.cache["fresh js"]==False

	def fresh_js(self, enable: bool):
		return fresh_js(
			self.shimon,
			enable,
			False
		)
