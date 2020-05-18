from SHIMON.api.fresh_css import ApiFreshCss

from testing.api.toggle import FreshToggle

from SHIMON import HttpResponse


class TestFreshCSS(FreshToggle):
    path = "SHIMON/static/css/font.css"
    name = "fresh css"

    def func(self, enable: bool) -> HttpResponse:
        return ApiFreshCss().entry(self.shimon, enable, False)
