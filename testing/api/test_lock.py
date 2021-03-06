from SHIMON.api.lock import ApiLock

from testing.base import BaseTest
from testing.http import assertHttpResponse

from SHIMON import HttpResponse


class TestLock(BaseTest):
    @BaseTest.request_context
    @BaseTest.unlocked
    def test_cache_cleared_after_lock(self) -> None:
        self.lock(self.pwd, True)

        assert self.shimon.cache.is_empty()

    @BaseTest.request_context
    @BaseTest.unlocked
    def test_invalid_pwd_returns_http_401(self) -> None:
        assertHttpResponse(self.lock("not the password", True), 401)

    @BaseTest.request_context
    def test_non_str_input_returns_http_400(self) -> None:
        not_a_str = 123

        assertHttpResponse(
            self.lock(not_a_str, True),  # type: ignore
            400,
        )

    @BaseTest.request_context
    @BaseTest.unlocked
    def test_not_redirecting_returns_http_400(self) -> None:
        assertHttpResponse(self.lock(self.pwd, False), 400)

    def lock(self, pwd: str, redirect: bool) -> HttpResponse:
        return ApiLock().entry(self.shimon, pwd, redirect)
