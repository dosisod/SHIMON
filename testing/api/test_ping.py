from SHIMON.api.error import error
from SHIMON.api.ping import ping as _ping

from testing.base import BaseTest
from testing.util import assertHttpResponse

from SHIMON.__init__ import HttpResponse

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
		return _ping(self.shimon, None, redirect)
