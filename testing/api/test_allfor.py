from SHIMON.api.allfor import ApiAllfor

from testing.base import BaseTest
from testing.http import assertHttpResponse

from SHIMON import HttpResponse


class TestAllfor(BaseTest):
    @BaseTest.request_context
    @BaseTest.unlocked
    def test_valid_id_always_returns_http_200(self) -> None:
        user = self.shimon.cache["history"][0]
        assertHttpResponse(self.allfor(user["id"]), 200)

    @BaseTest.request_context
    @BaseTest.unlocked
    def test_invalid_id_always_returns_http_400(self) -> None:
        assertHttpResponse(self.allfor("not a user id"), 400)

    @BaseTest.request_context
    def test_non_str_input_returns_http_400(self) -> None:
        not_a_string = 123

        assertHttpResponse(
            self.allfor(not_a_string),  # type: ignore
            400,
        )

    @BaseTest.request_context
    @BaseTest.unlocked
    def test_always_will_return_data(self) -> None:
        user = self.shimon.cache["history"][0]

        raw = self.allfor(user["id"])[0].json
        assert raw or raw == []

    def allfor(self, id: str) -> HttpResponse:
        return ApiAllfor().entry(self.shimon, id, False)
