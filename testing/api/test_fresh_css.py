from SHIMON.api.fresh_css import fresh_css

from testing.api.toggle import FreshToggle

from SHIMON.__init__ import HttpResponse

class TestFreshCSS(FreshToggle):
	path="SHIMON/static/css/font.css"
	name="fresh css"

	def func(self, enable: bool) -> HttpResponse:
		return fresh_css(
			self.shimon,
			enable,
			False
		)
