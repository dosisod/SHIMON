import json

from SHIMON.api.status import status

from testing.base import BaseTest

class TestStatus(BaseTest):
	@BaseTest.request_context
	@BaseTest.unlocked
	def test_always_returns_http_200(self):
		assert self.status_wrapper("true")[1]==200

	@BaseTest.request_context
	@BaseTest.unlocked
	def test_that_redirect_flag_doesnt_change_output(self):
		assert self.status_wrapper("true")[0].json==json.loads(self.status_wrapper("false")[0].data)["msg"]

	def status_wrapper(self, redirect: str):
		return status(self.shimon, {"redirect": redirect})
