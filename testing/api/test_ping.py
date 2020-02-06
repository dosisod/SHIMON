from SHIMON.api.error import error
from SHIMON.api.ping import ping

from testing.base import BaseTest
from testing.util import assertHttpResponse

class TestPing(BaseTest):
	@BaseTest.request_context
	def test_ping_with_redirect_returns_http_200(self):
		assertHttpResponse(
			self.ping(True),
			200
		)

	@BaseTest.request_context
	def test_ping_without_redirect_returns_http_200(self):
		assertHttpResponse(
			self.ping(False),
			200
		)

	@BaseTest.request_context
	def test_ping_with_redirect_returns_pong(self):
		assert self.ping(True)[0]=="pong"

	@BaseTest.request_context
	def test_ping_without_redirect_returns_pong(self):
		assert self.ping(False)[0].json["msg"]=="pong"

	def ping(self, redirect: bool):
		return ping(self.shimon, None, redirect)
