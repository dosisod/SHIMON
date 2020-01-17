from SHIMON.api.error import error
from SHIMON.api.ping import ping

from testing.base import BaseTest

class TestPing(BaseTest):
	@BaseTest.request_context
	def test_ping_with_redirect_returns_http_200(self):
		assert self.ping_wrapper("true")[1]==error(200, "pong", True, False)[1]

	@BaseTest.request_context
	def test_ping_without_redirect_returns_http_200(self):
		assert self.ping_wrapper("false")[1]==error(200, "pong", False, False)[1]

	@BaseTest.request_context
	def test_ping_with_redirect_returns_pong(self):
		assert self.ping_wrapper("true")[0]=="pong"

	@BaseTest.request_context
	def test_ping_without_redirect_returns_pong(self):
		assert self.ping_wrapper("false")[0].json["msg"]=="pong"

	def ping_wrapper(self, redirect: bool):
		return ping(self.shimon, {"redirect": redirect})
