from SHIMON.api.friends import ApiFriends

from testing.base import BaseTest
from testing.http import assertHttpResponse

from SHIMON import HttpResponse


class TestFriends(BaseTest):
    @BaseTest.request_context
    @BaseTest.unlocked
    def test_always_returns_http_200(self) -> None:
        assertHttpResponse(self.friends(), 200)

    @BaseTest.request_context
    @BaseTest.unlocked
    def test_always_will_return_data(self) -> None:
        assert self.friends()[0].json

    def friends(self) -> HttpResponse:
        return ApiFriends().entry(self.shimon, None, False)
