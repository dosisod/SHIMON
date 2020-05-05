from SHIMON.api.ping import ApiPing
from SHIMON.api.error import error

from testing.base import BaseTest
from testing.http import assertHttpResponse

from SHIMON import HttpResponse

class TestPing(BaseTest):
	@BaseTest.request_context
	def test_ping_with_redirect_returns_http_200(self) -> None:
		assertHttpResponse(
			self.ping(True),
			200
		)

	@BaseTest.request_context
	def test_ping_without_redirect_returns_http_200(self) -> None:
		assertHttpResponse(
			self.ping(False),
			200
		)

	@BaseTest.request_context
	def test_ping_with_redirect_returns_pong(self) -> None:
		assert self.ping(True)[0].data==b'"pong"\n'

	@BaseTest.request_context
	def test_ping_without_redirect_returns_pong(self) -> None:
		assert self.ping(False)[0].json["msg"]=="pong"

	def ping(self, redirect: bool) -> HttpResponse:
		return ApiPing().entry(self.shimon, None, redirect)
