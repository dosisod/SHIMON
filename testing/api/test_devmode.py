from SHIMON.api.devmode import ApiDevmode

from testing.base import BaseTest
from testing.http import assertHttpResponse

from SHIMON import HttpResponse


class TestDevmode(BaseTest):
    @BaseTest.request_context
    def test_true_enables_devmode(self) -> None:
        self.shimon.cache.mapper["developer"] = False

        self.devmode(True)

        assert self.shimon.cache["developer"] == True
        assert self.shimon.developer == True

    @BaseTest.request_context
    def test_false_disables_devmode(self) -> None:
        self.shimon.cache.mapper["developer"] = False

        self.devmode(False)

        assert self.shimon.cache["developer"] == False
        assert self.shimon.developer == False

    @BaseTest.request_context
    def test_non_bool_input_returns_http_400(self) -> None:
        not_a_bool = 123

        assertHttpResponse(
            self.devmode(not_a_bool),  # type: ignore
            400,
        )

    @BaseTest.request_context
    def test_always_returns_http_200(self) -> None:
        assertHttpResponse(self.devmode(True), 200)

    def devmode(self, enable: bool) -> HttpResponse:
        return ApiDevmode().entry(self.shimon, enable, False)
