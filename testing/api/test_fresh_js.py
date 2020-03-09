from SHIMON.api.fresh_js import fresh_js

from testing.api.toggle import FreshToggle

class TestFreshJS(FreshToggle):
	path="SHIMON/static/js/api.js"
	name="fresh js"

	def func(self, enable: bool):
		return fresh_js(
			self.shimon,
			enable,
			False
		)
