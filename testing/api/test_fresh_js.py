from SHIMON.api.fresh_js import ApiFreshJs

from testing.api.toggle import FreshToggle

from SHIMON import HttpResponse


class TestFreshJS(FreshToggle):
    path = "SHIMON/static/js/api.js"
    name = "fresh js"

    def func(self, enable: bool) -> HttpResponse:
        return ApiFreshJs().entry(self.shimon, enable, False)
