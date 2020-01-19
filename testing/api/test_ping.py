from SHIMON.api.error import error
from SHIMON.api.ping import ping

from testing.base import BaseTest

class TestPing(BaseTest):
	@BaseTest.request_context
	def test_ping_with_redirect_returns_http_200(self):
		assert self.ping("true")[1]==error(200, "pong", True, False)[1]

	@BaseTest.request_context
	def test_ping_without_redirect_returns_http_200(self):
		assert self.ping("false")[1]==error(200, "pong", False, False)[1]

	@BaseTest.request_context
	def test_ping_with_redirect_returns_pong(self):
		assert self.ping("true")[0]=="pong"

	@BaseTest.request_context
	def test_ping_without_redirect_returns_pong(self):
		assert self.ping("false")[0].json["msg"]=="pong"

	def ping(self, redirect: bool):
		return ping(self.shimon, None, redirect)
